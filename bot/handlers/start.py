from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager
from services.auth import register_user, get_auth_token
from services.exceptions import APIError
from dialogs.tasks import TaskStates
from dialogs.comments import CommentStates

router = Router()


@router.message(Command("start"))
async def start(
    message: types.Message, state: FSMContext, dialog_manager: DialogManager
):
    """
    Handles the /start command. Registers the user, provides authentication, and
    navigates to appropriate dialog states based on the command parameters.
    """
    telegram_id = message.from_user.id
    username = message.from_user.username
    args = message.text.split()

    try:
        # Register user and retrieve authentication token
        user_data = await register_user(telegram_id, username)
        await state.update_data(username=username, user_id=user_data['id'])
        token = await get_auth_token(username)
        await state.update_data(access_token=token['access'])

        # Handle command parameters for specific actions
        if len(args) > 1:
            param = args[1]

            if param.startswith("task_"):
                await _handle_task_navigation(param, dialog_manager)
                return

            elif param.startswith("edit_comment_"):
                await _handle_comment_edit(param, dialog_manager)
                return

            elif param.startswith("delete_comment_"):
                await _handle_comment_delete(param, dialog_manager)
                return

        # Default message if no parameters are provided
        await _send_default_message(message)

    except APIError as e:
        await message.answer(str(e))


async def _handle_task_navigation(param: str, dialog_manager: DialogManager):
    """
    Handles navigation to a specific task's details state.
    """
    task_id = param.split("_")[1]
    await dialog_manager.start(TaskStates.DETAILS, data={"task_id": task_id})


async def _handle_comment_edit(param: str, dialog_manager: DialogManager):
    """
    Handles navigation to the comment editing state.
    """
    comment_id = param.split("_")[2]
    task_id = param.split("_")[4]
    await dialog_manager.start(
        CommentStates.EDIT, data={"comment_id": comment_id, 'task_id': task_id}
    )


async def _handle_comment_delete(param: str, dialog_manager: DialogManager):
    """
    Handles navigation to the comment delete confirmation state.
    """
    comment_id = param.split("_")[2]
    task_id = param.split("_")[4]
    await dialog_manager.start(
        CommentStates.CONFIRM_DELETE,
        data={"comment_id": comment_id, 'task_id': task_id},
    )


async def _send_default_message(message: types.Message):
    """
    Sends the default welcome message when no parameters are provided in the /start command.
    """
    await message.answer(
        "Привет! Со мной ты можешь управлять своим днём как тебе угодно ;)\n"
        "Начни с /tasks"
    )
