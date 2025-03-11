from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Comment(Base):
    __tablename__ = "fastapi_comments"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<Comment id={self.id} task_id={self.task_id} user_id={self.user_id}>"
