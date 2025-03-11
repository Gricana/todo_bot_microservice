from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Row, Calendar, Radio
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.text import Jinja
from dialogs import comments
from handlers.tasks import (
    delete_task_data,
    get_task_data,
    list_tasks,
    create_new_task,
    save_task_field,
    save_task_deadline_time,
    save_task_deadline_date,
)
from states.tasks import TaskStates
from utils.categories import parse_categories
from utils.status import TaskStatus


tasks_dialog = Dialog(
    Window(
        Jinja("{{ text|safe }}"),
        Button(
            Const("➕ Новая задача"),
            id="new_task",
            on_click=lambda c, b, d: create_new_task(d),
        ),
        state=TaskStates.LIST,
        getter=list_tasks,
    ),
    Window(
        Jinja(
            "\U0001f4cc <b>{{ task.title }}</b>\n\n"
            "Дата создания: <b>{{ task.created_at }}</b>\n\n"
            "\U0001f4dd Описание: {{ task.description }}\n"
            "Дэдлайн: <b>{{ task.due_date }}</b>\n"
            "Статус: <b>{{ task.status }}</b>\n"
            "🏷 Категории: {{ task.categories }}",
        ),
        Row(
            Button(
                Const("✏️ Изменить"),
                id="edit",
                on_click=lambda c, b, d: d.switch_to(TaskStates.EDIT_FIELD_SELECTION),
            ),
            Button(
                Const("🗑 Удалить"),
                id="delete",
                on_click=lambda c, b, d: d.switch_to(TaskStates.CONFIRM_DELETE),
            ),
        ),
        Button(
            Const("💬 Посмотреть комментарии"),
            id="view_comments",
            on_click=lambda c, b, d: d.start(
                comments.CommentStates.LIST, {"task_id": d.start_data["task_id"]}
            ),
        ),
        Button(
            Const("🔙 Назад"),
            id="back",
            on_click=lambda c, b, d: d.switch_to(TaskStates.LIST),
        ),
        state=TaskStates.DETAILS,
        getter=get_task_data,
    ),
    Window(
        Const("Выберите, что хотите изменить:"),
        Row(
            Button(
                Const("✏️ Название"),
                id="edit_title",
                on_click=lambda c, b, d: d.switch_to(TaskStates.EDIT_TITLE),
            ),
            Button(
                Const("✏️ Описание"),
                id="edit_desc",
                on_click=lambda c, b, d: d.switch_to(TaskStates.EDIT_DESCRIPTION),
            ),
        ),
        Row(
            Button(
                Const("📅 Дедлайн"),
                id="edit_deadline",
                on_click=lambda c, b, d: d.switch_to(TaskStates.EDIT_DEADLINE_DATE),
            ),
            Button(
                Const("🔄 Статус"),
                id="edit_status",
                on_click=lambda c, b, d: d.switch_to(TaskStates.EDIT_STATUS),
            ),
        ),
        Row(
            Button(
                Const("🏷 Категории"),
                id="edit_categories",
                on_click=lambda c, b, d: d.switch_to(TaskStates.EDIT_CATEGORIES),
            ),
        ),
        state=TaskStates.EDIT_FIELD_SELECTION,
    ),
    # Editing window for the task
    Window(
        Const("Введите название задачи:"),
        TextInput(
            id="edit_title_input",
            on_success=lambda m, w, d, text: save_task_field(d, "title", text),
        ),
        state=TaskStates.EDIT_TITLE,
    ),
    # Editing window descriptions
    Window(
        Const("Введите описание задачи:"),
        TextInput(
            id="edit_desc_input",
            on_success=lambda m, w, d, text: save_task_field(d, "description", text),
        ),
        state=TaskStates.EDIT_DESCRIPTION,
    ),
    # Editing window status
    Window(
        Const("Выберите новый статус:"),
        Radio(
            checked_text=Format("{item[1]}"),
            unchecked_text=Format("{item[1]}"),
            item_id_getter=lambda item: item[0],
            items=TaskStatus.human_readable_list(),
            id="status_select",
            on_click=lambda m, w, d, status: save_task_field(d, "status", status),
        ),
        state=TaskStates.EDIT_STATUS,
    ),
    # Window for editing the dedeline date
    Window(
        Const("Выберите дату дедлайна:"),
        Calendar(
            id="edit_deadline_date_picker",
            on_click=lambda c, b, d, date: save_task_deadline_date(d, date),
        ),
        state=TaskStates.EDIT_DEADLINE_DATE,
    ),
    # Window for editing deadline time
    Window(
        Const("Введите время дедлайна (в формате HH:MM):"),
        TextInput(
            id="edit_deadline_time_input",
            on_success=lambda m, w, d, text: save_task_deadline_time(d, text),
        ),
        state=TaskStates.EDIT_DEADLINE_TIME,
    ),
    # Editing Problem Editing Window
    Window(
        Const("Введите категории через запятую (например: Работа, Личное):"),
        TextInput(
            id="edit_categories_input",
            on_success=lambda m, w, d, text: save_task_field(
                d, "categories", parse_categories(text)
            ),
        ),
        state=TaskStates.EDIT_CATEGORIES,
    ),
    Window(
        Const("Вы уверены, что хотите удалить задачу?"),
        Row(
            Button(
                Const("✅ Да"),
                id="confirm_delete",
                on_click=lambda c, b, d: delete_task_data(
                    d, d.middleware_data["state"]
                ),
            ),
            Button(
                Const("❌ Нет"),
                id="cancel",
                on_click=lambda c, b, d: d.switch_to(TaskStates.DETAILS),
            ),
        ),
        state=TaskStates.CONFIRM_DELETE,
    ),
)
