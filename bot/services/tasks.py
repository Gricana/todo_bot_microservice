from aiogram.fsm.context import FSMContext
from services.base import api_request
from services.auth import _get_auth_headers


async def get_tasks(state: FSMContext):
    """
    Fetches the list of tasks for the user.

    Args:
        state (FSMContext): The FSM context to retrieve the token.

    Returns:
        dict: The response data from the API request.
    """
    headers = await _get_auth_headers(state)
    return await api_request(
        'GET',
        'api/tasks',
        headers=headers,
    )


async def get_task_details(state: FSMContext, task_id: str):
    """
    Fetches the details of a specific task by its ID.

    Args:
        state (FSMContext): The FSM context to retrieve the token.
        task_id (str): The ID of the task whose details are to be fetched.

    Returns:
        dict: The response data from the API request.
    """
    headers = await _get_auth_headers(state)
    return await api_request(
        'GET',
        f'api/tasks/{task_id}',
        headers=headers,
    )


async def create_task(state: FSMContext, field_data: dict):
    """
    Creates a new task with the provided field data.

    Args:
        state (FSMContext): The FSM context to retrieve the token.
        field_data (dict): A dictionary containing the task field data to create the task.

    Returns:
        dict: The response data from the API request.
    """
    headers = await _get_auth_headers(state)
    return await api_request(
        'POST',
        'api/tasks',
        payload=field_data,
        headers=headers,
    )


async def update_task(state: FSMContext, task_id: str, field_data: dict):
    """
    Updates an existing task with the provided field data.

    Args:
        state (FSMContext): The FSM context to retrieve the token.
        task_id (str): The ID of the task to be updated.
        field_data (dict): A dictionary containing the field data to update the task.

    Returns:
        dict: The response data from the API request.
    """
    headers = await _get_auth_headers(state)
    return await api_request(
        'PATCH',
        f'api/tasks/{task_id}',
        payload=field_data,
        headers=headers,
    )


async def delete_task(state: FSMContext, task_id: str):
    """
    Deletes a task by its ID.

    Args:
        state (FSMContext): The FSM context to retrieve the token.
        task_id (str): The ID of the task to delete.

    Returns:
        dict: The response data from the API request.
    """
    headers = await _get_auth_headers(state)
    return await api_request(
        'DELETE',
        f'api/tasks/{task_id}',
        headers=headers,
    )
