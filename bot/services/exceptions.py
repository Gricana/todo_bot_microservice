from aiogram.fsm.state import State


class APIError(Exception):
    def __init__(self, message: str, state: State = None):
        super().__init__(message, state)
        self.message = message
        self.state = state

    def __str__(self):
        return self.message
