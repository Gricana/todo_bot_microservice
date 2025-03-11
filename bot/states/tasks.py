from aiogram.fsm.state import StatesGroup, State


class TaskStates(StatesGroup):
    EDIT_DEADLINE_TIME = State()
    EDIT_DEADLINE_DATE = State()
    EDIT_STATUS = State()
    LIST = State()
    DETAILS = State()
    EDIT_FIELD_SELECTION = State()
    EDIT_TITLE = State()
    EDIT_DESCRIPTION = State()
    EDIT_CATEGORIES = State()
    CONFIRM_DELETE = State()
    EDIT_TASK = State()
