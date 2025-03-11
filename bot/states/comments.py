from aiogram.fsm.state import State, StatesGroup


class CommentStates(StatesGroup):
    LIST = State()
    ADD = State()
    EDIT = State()
    CONFIRM_DELETE = State()
    DELETE = State()
