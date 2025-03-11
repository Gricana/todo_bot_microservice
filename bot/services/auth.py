from aiogram.fsm.context import FSMContext
from services.base import api_request


async def register_user(telegram_id: int, username: str):
    """
    Registers a user with the provided telegram ID and username.

    Args:
        telegram_id (int): The unique Telegram user ID.
        username (str): The Telegram username.

    Returns:
        dict: The response data from the API after user registration.
    """
    return await api_request(
        "POST",
        "auth/register/",
        payload={"telegram_id": telegram_id, "username": username},
    )


async def get_auth_token(username: str):
    """
    Retrieves an authentication token for the user by their username.

    Args:
        username (str): The Telegram username.

    Returns:
        dict: The response data containing new access & refresh authentication token.
    """
    return await api_request("POST", "auth/token/", payload={"username": username})


async def get_token(state: FSMContext):
    """
    Retrieves the authentication token from the FSM context, or fetches it if not available.

    Args:
        state (FSMContext): The finite state machine context to get the data from.

    Returns:
        dict: The authentication token.
    """
    data = await state.get_data()
    token = data.get('access_token')

    if not token:
        token = await _fetch_and_store_token(state, data.get('username'))

    return token


async def _fetch_and_store_token(state: FSMContext, username: str):
    """
    Fetches the authentication token and stores it in the FSM context.

    Args:
        state (FSMContext): The finite state machine context to store the token.
        username (str): The Telegram username.

    Returns:
        dict: The authentication token response.
    """
    token = await get_auth_token(username)
    await state.update_data(access_token=token)
    return token


async def _get_auth_headers(state: FSMContext):
    """
    Helper function to retrieve the Authorization header for API requests.

    Args:
        state (FSMContext): The state context, used to fetch the token.

    Returns:
        dict: A dictionary containing the Authorization header.
    """
    token = await get_token(state)
    return {"Authorization": f"Bearer {token}"}
