from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager

from config import BOT_USERNAME
from services.comments import update_comment, add_comment, get_comments, delete_comment
from states.comments import CommentStates


def get_task_and_comment_ids(dialog_manager: DialogManager):
    """Receives Task_id and Comment_id from dialogue data."""
    task_id = dialog_manager.start_data.get("task_id")
    comment_id = dialog_manager.start_data.get("comment_id")
    return task_id, comment_id


async def list_comments(dialog_manager: DialogManager, state: FSMContext, **kwargs):
    """Receives a list of comments for the specified task."""
    task_id, _ = get_task_and_comment_ids(dialog_manager)
    comments = await get_comments(state, task_id)

    if not comments['comments']:
        return {"text": "💬 У этой задачи пока нет комментариев."}

    base_url = f"https://t.me/{BOT_USERNAME}?start="
    comments_text = "\n".join(
        [
            "───────────────────────────────────\n"
            f"{comment['content']}\n\n"
            f"✏️ <a href='{base_url}edit_comment_{comment['id']}_task_{task_id}'>Изменить</a> | "
            f"🗑 <a href='{base_url}delete_comment_{comment['id']}_task_{task_id}'>Удалить</a>"
            for comment in comments['comments']
        ]
    )
    return {"text": f"🗒 <b>Комментарии:</b>\n\n{comments_text}"}


async def save_comment(dialog_manager: DialogManager, state: FSMContext, text: str):
    """Saves a new comment for the task."""
    task_id, _ = get_task_and_comment_ids(dialog_manager)
    text = text.strip()
    if not text:
        return

    await add_comment(state, task_id, text)
    await dialog_manager.switch_to(CommentStates.LIST)


async def edit_comment(dialog_manager: DialogManager, state: FSMContext, text: str):
    """Editing an existing comment."""
    task_id, comment_id = get_task_and_comment_ids(dialog_manager)

    text = text.strip()
    if not text or not comment_id:
        return

    await update_comment(state, task_id, comment_id, text)
    await dialog_manager.switch_to(CommentStates.LIST)


async def remove_comment(dialog_manager: DialogManager, state: FSMContext):
    """Removes comment"""
    task_id, comment_id = get_task_and_comment_ids(dialog_manager)
    if not comment_id or not task_id:
        return

    await delete_comment(state, task_id, comment_id)
    await dialog_manager.switch_to(CommentStates.LIST)
