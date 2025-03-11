from services.exceptions import APIError
from states.tasks import TaskStates
from states.comments import CommentStates


ERRORS = {
    400: {
        "title": {
            "error": APIError(
                "У Вас уже есть задача с таким именем", state=TaskStates.EDIT_TITLE
            ),
        },
        "due_date": {
            "error": APIError(
                "Вы указали дату выполнения раньше сегодняшней даты или даты создания задачи",
                state=TaskStates.EDIT_DEADLINE_DATE,
            ),
        },
    },
    401: {
        "error": APIError("Авторизуйтесь в боте командой /start", None),
    },
    404: {
        "error": APIError("Такой задачи мы у Вас не нашли", state=TaskStates.LIST),
        "detail": {
            "error": APIError(
                "Комментарии / задачи с переданным ID не существует",
                state=CommentStates.LIST,
            ),
        },
    },
    429: {
        "detail": {
            "error": APIError("Слишком много запросов. Попробуйте позже.", None),
        }
    },
    500: {
        "error": APIError("Сервис временно недоступен. Мы скоро вернёмся ;)", None),
    },
}
