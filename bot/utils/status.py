from enum import Enum


class TaskStatus(Enum):
    TODO = ("TODO", "⏳ Ожидание")
    IN_PROGRESS = ("IN_PROGRESS", "🟡 В процессе")
    DONE = ("DONE", "✅ Завершено")

    def __init__(self, api_value: str, human_readable: str):
        """
        Initializes the TaskStatus with the given API value and human-readable label.

        Args:
            api_value (str): The value representing the task status in the API.
            human_readable (str): The user-friendly label for the task status.
        """
        self.api_value = api_value
        self.human_readable = human_readable

    @classmethod
    def list(cls) -> list:
        """
        Returns a list of all API values for task statuses.

        Returns:
            list: A list containing the API values of all statuses.
        """
        return [status.api_value for status in cls]

    @classmethod
    def human_readable_list(cls) -> list:
        """
        Returns a list of tuples with the API value and the corresponding human-readable label.

        Returns:
            list: A list of tuples where each tuple contains the API value and the human-readable label.
        """
        return [(status.api_value, status.human_readable) for status in cls]

    @classmethod
    def from_api(cls, api_value: str) -> str:
        """
        Returns the human-readable label corresponding to the given API value.
        If the API value is not recognized, returns "Неизвестный статус".

        Args:
            api_value (str): The API value to be mapped.

        Returns:
            str: The human-readable label or "Неизвестный статус" if not found.
        """
        for status in cls:
            if status.api_value == api_value:
                return status.human_readable
        return "Неизвестный статус"
