import httpx
from config import DJANGOAPI_URL, BOT_TOKEN
from services.errors import ERRORS
from services.exceptions import APIError


async def api_request(
    method: str,
    endpoint: str,
    host: str = DJANGOAPI_URL,
    payload: dict = None,
    headers: dict = None,
):
    """
    Makes an HTTP request to the given endpoint and returns the response.

    Args:
        method (str): The HTTP method (GET, POST, etc.)
        endpoint (str): The endpoint of the API.
        host (str): The base URL of the API (defaults to DJANGOAPI_URL).
        payload (dict): The data to send in the request body (defaults to None).
        headers (dict): Additional headers to send with the request (defaults to None).

    Returns:
        dict or None: The JSON response if successful, or None if there is no content.

    Raises:
        APIError: If the API returns an error or fails to respond.
    """
    headers = headers or {}
    headers.setdefault("x-telegram-bot-api-secret-token", BOT_TOKEN)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method, f"{host}{endpoint}", json=payload, headers=headers
            )
            response.raise_for_status()

            return response.json() if response.status_code != 204 else None

        except httpx.HTTPStatusError as e:
            return await _handle_http_error(e.response)

        except httpx.RequestError as e:
            raise _handle_request_error(e)


async def _handle_http_error(response):
    """
    Handles HTTP errors based on the response status code.

    Args:
        response (httpx.Response): The HTTP response object.

    Raises:
        APIError: If the status code is not in the predefined error mapping.
    """
    status_code = response.status_code
    error_data = response.json() if response.content != 204 else {}

    if status_code in ERRORS:
        error_entry = ERRORS[status_code]

        if isinstance(error_entry, dict):
            for field, error_info in error_entry.items():
                if field in error_data:
                    raise error_info["error"]

        raise error_entry["error"]

    raise APIError(message=f"Ошибка {status_code}: {response.text}")


def _handle_request_error(e: httpx.RequestError):
    """
    Handles errors that occur during the request process (e.g., connection issues).

    Args:
        e (httpx.RequestError): The exception raised during the request.

    Raises:
        APIError: A general API error with a message describing the issue.
    """
    return ERRORS[500]['error']
