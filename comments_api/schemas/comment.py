import datetime
from pydantic import BaseModel


class CommentCreate(BaseModel):
    """
    Model for creating a new comment.

    Attributes:
    - TASK_ID (str): the identifier of the task.
    - user_id (int): user identifier.
    - Content (str): Comment contents.
    """

    task_id: str
    user_id: int
    content: str

    class Config:
        orm_mode = True


class CommentResponse(BaseModel):
    """
    Model for presenting a commentary in the answers of the API.

    Attributes:
    - ID (int): Comment identifier.
    - TASK_ID (str): the identifier of the task.
    - user_id (int): user identifier.
    - Content (str): Comment contents.
    - Creed_at (Datetime): Date and time of creating a comment.
    """

    id: int
    task_id: str
    user_id: int
    content: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class CommentsResponse(BaseModel):
    """
    Model for presenting a list of comments.

    Attributes:
    - Comments (List [commentRasponse]): List of comment objects.
    """

    comments: list[CommentResponse]


class CommentUpdate(BaseModel):
    """
    Model for updating the contents of the comment.

    Attributes:
    - Content (str): updated contents of the comment.
    """

    content: str

    class Config:
        orm_mode = True
