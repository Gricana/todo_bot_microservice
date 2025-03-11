from models.comment import Comment
from schemas.comment import CommentCreate
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession


class CommentRepository:

    @staticmethod
    async def create_comment(db: AsyncSession, comment: CommentCreate):
        """Creates a new comment in the database."""
        new_comment = Comment(**comment.dict())
        db.add(new_comment)
        await db.commit()
        await db.refresh(new_comment)
        return new_comment

    @staticmethod
    async def get_comments(db: AsyncSession, task_id: str):
        """Receives all the comments for the task."""
        result = await db.execute(select(Comment).where(Comment.task_id == task_id))
        return result.scalars().all()

    @staticmethod
    async def get_comment_by_id(db: AsyncSession, comment_id: int):
        """Receives a comment on ID."""
        return await db.get(Comment, comment_id)

    @staticmethod
    async def update_comment(db: AsyncSession, comment_id: int, new_content: str):
        """Updates the comment."""
        comment = await db.get(Comment, comment_id)
        if comment:
            comment.content = new_content
            await db.commit()
            await db.refresh(comment)
        return comment

    @staticmethod
    async def delete_comment(db: AsyncSession, comment_id: int):
        """Removes a comment on ID."""
        comment = await db.get(Comment, comment_id)
        if comment:
            await db.delete(comment)
            await db.commit()
            return True
        return False

    @staticmethod
    async def delete_all_comments_by_task(db: AsyncSession, task_id: str):
        """Deletes all comments on the task"""
        stmt = delete(Comment).where(Comment.task_id == task_id).returning(Comment.id)
        result = await db.execute(stmt)
        deleted_count = len(result.scalars().all())
        await db.commit()
        return deleted_count
