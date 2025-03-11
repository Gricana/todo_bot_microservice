import logging
from datetime import datetime

import pydantic
import pytz
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ErrorEvent
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.api.exceptions import NoContextError
from config import BOT_USERNAME, SERVER_TZ, USER_TZ
from services.comments import delete_comment_by_task
from services.exceptions import APIError
from services.tasks import (
    delete_task,
    create_task,
    update_task,
    get_task_details,
    get_tasks,
)
from states.tasks import TaskStates
from utils.status import TaskStatus
from utils.tasks import format_datetime, validate_time_format

router = Router()


@router.message(Command("tasks"))
async def show_tasks(message: types.Message, dialog_manager: DialogManager):
    """
    This handler starts the task list dialog.
    It starts the dialog in the `TaskStates.LIST` state.
    """
    try:
        await dialog_manager.start(TaskStates.LIST, mode=StartMode.RESET_STACK)
    except APIError as e:
        await message.answer(str(e))


@router.error()
async def global_error_handler(event: ErrorEvent, dialog_manager: DialogManager):
    """
    Handles any unhandled exceptions globally in the dialog.
    It processes errors like validation errors and API errors and informs the user.
    """
    exc = event.exception
    print(exc)

    message = _get_message_from_event(event)

    if not message:
        return True

    new_state = None
    dialog_data = _get_dialog_data(dialog_manager)

    if isinstance(exc, pydantic.ValidationError):
        await message.answer(exc.errors()[0]['input'])

    elif isinstance(exc, APIError):
        await message.answer(str(exc))
        new_state = exc.state
    else:
        await message.answer("Произошла неожиданная ошибка. Попробуйте позже.")

    await _handle_error_state(new_state, dialog_manager, dialog_data)


def _get_message_from_event(event: ErrorEvent):
    """Extracts the message object from the event."""
    if event.update:
        if event.update.message:
            return event.update.message
        elif event.update.callback_query:
            return event.update.callback_query.message
    return None


def _get_dialog_data(dialog_manager: DialogManager):
    """Tries to get dialog data from the current context."""
    try:
        return dialog_manager.current_context().dialog_data
    except NoContextError:
        return {}


async def _handle_error_state(new_state, dialog_manager, dialog_data):
    """
    Switches to the correct state or resets the dialog after an error.
    """
    if not new_state:
        await dialog_manager.start(new_state, data=dialog_data)
    else:
        await dialog_manager.switch_to(new_state)
        await dialog_manager.update(data=dialog_data)


async def list_tasks(state: FSMContext, **kwargs):
    """
    Retrieves all tasks and formats them for display.
    Returns a dictionary with the formatted text for the task list.
    """
    tasks = await get_tasks(state)

    if not tasks['tasks']:
        return {'text': 'У Вас нет задач'}

    return {"text": await _format_task_list(tasks['tasks'])}


async def _format_task_list(tasks):
    """
    Helper function to format a list of tasks into a message.
    """
    text = "\U0001f4cb <b>Ваши задачи:</b>\n\n"
    for idx, task in enumerate(tasks):
        task_url = f"https://t.me/{BOT_USERNAME}?start=task_{task['id']}"
        text += f"<b>{idx + 1}.</b> <a href='{task_url}'>{task['title']}</a>\n"
    return text


async def get_task_data(dialog_manager: DialogManager, **kwargs):
    """
    Fetches task details from the API and formats them for display.
    """
    state = dialog_manager.middleware_data["state"]

    task = dialog_manager.dialog_data.get("api_task", {})

    if not task:
        task = await _fetch_or_initialize_task(dialog_manager, state)

    return {"task": await _format_task_data(task) if task else None}


async def _fetch_or_initialize_task(dialog_manager, state):
    """
    Helper function to fetch task details or initialize a new task.
    """
    task_id = dialog_manager.start_data.get("task_id")

    if task_id:
        task = await get_task_details(state, task_id)
        dialog_manager.dialog_data.update({'api_task': task, 'is_new_task': False})
    else:
        dialog_manager.dialog_data.clear()
        dialog_manager.dialog_data.update({'api_task': {}, 'is_new_task': True})

    return dialog_manager.dialog_data.get("api_task", {})


async def _format_task_data(task):
    """
    Formats task data to a readable format.
    """
    formatted_task = task.copy()
    formatted_task['description'] = task.get('description') or 'Без описания'
    formatted_task['created_at'] = format_datetime(task['created_at'])
    formatted_task['due_date'] = format_datetime(task['due_date'])
    formatted_task["status"] = TaskStatus.from_api(task.get("status", TaskStatus.TODO))
    formatted_task["categories"] = (
        ", ".join(category["name"] for category in task.get("categories", []))
        or "Нет категорий"
    )

    return formatted_task


async def save_task_deadline_date(dialog_manager, date):
    """Save the dates of the deadline of the problem"""
    dialog_manager.dialog_data["due_date"] = date.isoformat()
    await dialog_manager.switch_to(TaskStates.EDIT_DEADLINE_TIME)


async def save_task_deadline_time(dialog_manager, time_str):
    """Conservation of the deadline of the task"""
    valid_time = validate_time_format(time_str)
    if valid_time:
        user_timezone = pytz.timezone(USER_TZ)
        server_timezone = pytz.timezone(SERVER_TZ)
        user_datetime_str = f"{dialog_manager.dialog_data['due_date']} {valid_time.strftime('%H:%M:%S')}"
        user_datetime = datetime.strptime(user_datetime_str, "%Y-%m-%d %H:%M:%S")
        user_datetime = user_timezone.localize(user_datetime)
        server_datetime = user_datetime.astimezone(server_timezone)
        server_datetime_iso = server_datetime.isoformat()
        await save_task_field(dialog_manager, "due_date", server_datetime_iso)
    else:
        await dialog_manager.switch_to(TaskStates.EDIT_DEADLINE_TIME)


async def save_task_field(dialog_manager: DialogManager, field: str, value):
    """
    Saves a single field of the task.
    If it's a new task and fields are missing, it navigates to edit fields selection.
    """
    dialog_manager.dialog_data[field] = value

    if dialog_manager.dialog_data.get("is_new_task", False):
        await _check_for_missing_fields(dialog_manager)
        return

    await submit_task(dialog_manager, dialog_manager.middleware_data["state"])


async def _check_for_missing_fields(dialog_manager: DialogManager):
    """
    Helper function to check for missing required fields in a new task.
    If any field is missing, switches to the field selection state.
    """
    missing_fields = [
        f for f in ["title", "due_date"] if not dialog_manager.dialog_data.get(f)
    ]
    if missing_fields:
        await dialog_manager.switch_to(TaskStates.EDIT_FIELD_SELECTION)
    else:
        await submit_task(dialog_manager, dialog_manager.middleware_data["state"])


async def create_new_task(dialog_manager: DialogManager):
    """
    Creates a new task and initializes the dialog for task creation.
    """
    existing_task = dialog_manager.dialog_data.get("api_task", {})

    new_task_data = {
        "title": existing_task.get("title", ""),
        "description": existing_task.get("description", ""),
        "status": TaskStatus.TODO.api_value,
        "categories": existing_task.get("categories", []),
    }

    dialog_manager.dialog_data.clear()
    dialog_manager.dialog_data.update(
        {
            "api_task": new_task_data,
            "is_new_task": True,
        }
    )

    await dialog_manager.switch_to(TaskStates.EDIT_FIELD_SELECTION)


async def submit_task(dialog_manager: DialogManager, state: FSMContext, **kwargs):
    """
    Submits the task either by creating a new one or updating an existing task.
    """
    task_id = dialog_manager.dialog_data.get("api_task", {}).get("id")
    is_new_task = dialog_manager.dialog_data.get("is_new_task", False)
    updated_data = {
        k: v
        for k, v in dialog_manager.dialog_data.items()
        if k not in ["api_task", "is_new_task"]
    }

    if task_id and not is_new_task:
        await _update_existing_task(dialog_manager, state, updated_data)
    else:
        await _create_new_task(dialog_manager, state, updated_data)


async def _update_existing_task(dialog_manager, state, updated_data):
    """Helper function to update an existing task."""
    task = await update_task(
        state, dialog_manager.dialog_data["api_task"]["id"], updated_data
    )
    dialog_manager.dialog_data["api_task"] = task
    await dialog_manager.switch_to(TaskStates.DETAILS)


async def _create_new_task(dialog_manager, state, updated_data):
    """Helper function to create a new task."""
    required_fields = {"title": "Название задачи", "due_date": "Дедлайн"}
    missing_fields = [
        name for field, name in required_fields.items() if not updated_data.get(field)
    ]

    if missing_fields:
        missing_text = "❌ Заполните обязательные поля: " + ", ".join(missing_fields)
        await dialog_manager.event.answer(missing_text)
        return

    task = await create_task(state, updated_data)

    dialog_manager.dialog_data.clear()
    dialog_manager.dialog_data["api_task"] = task
    dialog_manager.dialog_data["is_new_task"] = False

    if dialog_manager.start_data:
        dialog_manager.start_data.update({"task_id": task.get("id")})

    await dialog_manager.switch_to(TaskStates.DETAILS)


async def delete_task_data(dialog_manager: DialogManager, state: FSMContext, **kwargs):
    """
    Deletes a task and its associated comments.
    """
    task_id = dialog_manager.dialog_data.get("api_task", {}).get("id")
    await delete_comment_by_task(state, task_id)
    await delete_task(state, task_id)
    await dialog_manager.switch_to(TaskStates.LIST)
