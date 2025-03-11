from aiogram.fsm.context import FSMContext
from config import FASTAPI_URL
from services.auth import _get_auth_headers
from services.base import api_request


async def get_comments(state: FSMContext, task_id: str):
    """
    Fetches the comments for a specific task.

    Args:
        state (FSMContext): The FSM context to retrieve the token.
        task_id (str): The task ID for which to fetch comments.

    Returns:
        dict: The response data from the API request.
    """
    headers = await _get_auth_headers(state)
    return await api_request(
        'GET',
        f'comments/{task_id}',
        headers=headers,
        host=FASTAPI_URL,
    )


async def add_comment(state: FSMContext, task_id: str, text: str):
    """
    Adds a comment to a specific task.

    Args:
        state (FSMContext): The FSM context to retrieve the user ID and token.
        task_id (str): The task ID to which the comment will be added.
        text (str): The content of the comment.

    Returns:
        dict: The response data from the API request.
    """
    user_id = await _get_user_id(state)
    headers = await _get_auth_headers(state)

    payload = {'task_id': task_id, 'user_id': user_id, 'content': text}
    return await api_request(
        'POST',
        f'comments/{task_id}',
        payload=payload,
        headers=headers,
        host=FASTAPI_URL,
    )


async def update_comment(state: FSMContext, task_id: str, comment_id: int, text: str):
    """
    Updates an existing comment on a specific task.

    Args:
        state (FSMContext): The FSM context to retrieve the user ID and token.
        task_id (str): The task ID on which the comment exists.
        comment_id (int): The ID of the comment to update.
        text (str): The updated content of the comment.

    Returns:
        dict: The response data from the API request.
    """
    user_id = await _get_user_id(state)
    headers = await _get_auth_headers(state)

    payload = {'task_id': task_id, 'user_id': user_id, 'content': text}
    return await api_request(
        'PUT',
        f'comments/{task_id}/{comment_id}',
        payload=payload,
        headers=headers,
        host=FASTAPI_URL,
    )


async def delete_comment(state: FSMContext, task_id: str, comment_id: int):
    """
    Deletes a specific comment from a task.

    Args:
        state (FSMContext): The FSM context to retrieve the token.
        task_id (str): The task ID from which the comment will be deleted.
        comment_id (int): The comment ID to delete.

    Returns:
        dict: The response data from the API request.
    """
    headers = await _get_auth_headers(state)
    return await api_request(
        'DELETE',
        f'comments/{task_id}/{comment_id}',
        headers=headers,
        host=FASTAPI_URL,
    )


async def delete_comment_by_task(state: FSMContext, task_id: str):
    """
    Deletes all comments associated with a specific task.

    Args:
        state (FSMContext): The FSM context to retrieve the token.
        task_id (str): The task ID whose comments will be deleted.

    Returns:
        dict: The response data from the API request.
    """
    headers = await _get_auth_headers(state)
    return await api_request(
        'DELETE',
        f'comments/{task_id}',
        headers=headers,
        host=FASTAPI_URL,
    )


async def _get_user_id(state: FSMContext):
    """
    Helper function to retrieve the user ID from the FSM context.

    Args:
        state (FSMContext): The state context to retrieve user data.

    Returns:
        int: The user ID retrieved from the state.
    """
    data = await state.get_data()
    return data.get('user_id')
