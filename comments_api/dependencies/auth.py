import httpx
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer
from settings import settings

security = HTTPBearer()

# Standard errors
ERRORS = {
    401: HTTPException(
        status_code=401, detail="Неверный токен для доступа к Django REST API"
    ),
    404: HTTPException(status_code=404, detail="У Вас нет задачи с таким id"),
    429: HTTPException(
        status_code=429, detail="Слишком много запросов. Попробуйте позже."
    ),
    500: HTTPException(status_code=500, detail="Ошибка связи с Django API."),
}


async def check_task_ownership(task_id: str, user_token: str = Security(security)):
    """
    Checks whether the task belongs to the current user.

    Args:
        TASK_ID (str): ID Tasks for verification.
        user_token (str): user token for authorization.

    RAISES:
        Httpexception: In case of communication error with the Django API or incorrect token.

    Returns:
        Bool: True, if the task belongs to the user.
    """
    headers = {"Authorization": f"Bearer {user_token.credentials}"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.DJANGO_BACKEND_URL}tasks/{task_id}", headers=headers
            )
        except httpx.ConnectError:
            raise ERRORS.get(500)

    if response.status_code == 200:
        return True

    raise ERRORS.get(response.status_code, ERRORS.get(500))
