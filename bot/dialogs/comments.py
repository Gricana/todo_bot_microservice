from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Jinja
from handlers.comments import list_comments, save_comment, edit_comment, remove_comment
from states.comments import CommentStates
from states.tasks import TaskStates


comments_dialog = Dialog(
    Window(
        Jinja("{{ text|safe }}"),
        Row(
            Button(
                Const("🔙 Назад"),
                id="back",
                on_click=lambda c, b, d: d.start(
                    TaskStates.DETAILS, {"task_id": d.start_data["task_id"]}
                ),
            ),
            Button(
                Const("➕ Добавить"),
                id="add_comment",
                on_click=lambda c, b, d: d.switch_to(CommentStates.ADD),
            ),
        ),
        state=CommentStates.LIST,
        getter=list_comments,
    ),
    Window(
        Const("Введите ваш новый комментарий:"),
        TextInput(
            id="comment_input",
            on_success=lambda m, w, d, text: save_comment(
                d, d.middleware_data["state"], text
            )
            or d.switch_to(CommentStates.LIST),
        ),
        state=CommentStates.ADD,
    ),
    Window(
        Const("✏️ Введите новый текст комментария:"),
        TextInput(
            id="edit_comment_input",
            on_success=lambda m, w, d, text: edit_comment(
                d, d.middleware_data["state"], text
            )
            or d.switch_to(CommentStates.LIST),
        ),
        state=CommentStates.EDIT,
    ),
    Window(
        Const("Вы уверены, что хотите удалить этот комментарий?"),
        Row(
            Button(
                Const("✅ Да"),
                id="confirm_delete",
                on_click=lambda c, b, d: remove_comment(d, d.middleware_data["state"]),
            ),
            Button(
                Const("❌ Нет"),
                id="cancel",
                on_click=lambda c, b, d: d.switch_to(CommentStates.LIST),
            ),
        ),
        state=CommentStates.CONFIRM_DELETE,
    ),
)
