from cache.comments import CommentCache
from repositories.comments import CommentRepository
from schemas.comment import CommentCreate, CommentUpdate
from sqlalchemy.ext.asyncio import AsyncSession


class CommentService:
    """
    Service for working with comments, including creating, updating, deleting and caching.
    """

    @staticmethod
    async def create_comment(db: AsyncSession, redis, comment: CommentCreate):
        """
        Creates a new comment and saves it in the database and cache.

        Args:
            DB (AsyncSession): Database session.
            Redis: Client Redis for caching.
            Comment (CommentCreate): Data for creating a comment.

        Returns:
            New_comment (Comment): New comment.
        """
        new_comment = await CommentRepository.create_comment(db, comment)
        await CommentCache.cache_comment(
            redis, new_comment.task_id, new_comment.id, new_comment
        )
        return new_comment

    @staticmethod
    async def get_comments_by_task(db: AsyncSession, redis, task_id: str):
        """
        Receives all the comments for the task. Checks the cache, if there is no data, requests from the database.

        Args:
            DB (AsyncSession): Database session.
            Redis: Client Redis for caching.
            TASK_ID (str): the identifier of the task.

        Returns:
            List [comment]: a list of comments for the task.
        """
        cached_comments = await CommentCache.get_cached_comments(redis, task_id)
        if cached_comments:
            return [comment for comment in cached_comments.values()]

        comments = await CommentRepository.get_comments(db, task_id)
        for comment in comments:
            await CommentCache.cache_comment(redis, task_id, comment.id, comment)
        return comments

    @staticmethod
    async def delete_comment(
        db: AsyncSession, redis, comment_id: int, task_id: str
    ) -> bool:
        """
        Removes a comment from the database and cache.

        Args:
            DB (AsyncSession): Database session.
            Redis: Client Redis for caching.
            Comment_id (int): Comment identifier.
            TASK_ID (str): the identifier of the task.

        Returns:
            Bool: Success of commentary removal.
        """
        deleted = await CommentRepository.delete_comment(db, comment_id)
        if deleted:
            await CommentCache.delete_cached_comment(redis, task_id, comment_id)
            return True
        return False

    @staticmethod
    async def delete_comments_by_task(db: AsyncSession, redis, task_id: str):
        """
        Removes all comments for the task from the database and cache.

        Args:
            DB (AsyncSession): Database session.
            Redis: Client Redis for caching.
            TASK_ID (str): the identifier of the task.

        Returns:
            Int: The number of remote comments.
        """
        deleted_count = await CommentRepository.delete_all_comments_by_task(db, task_id)
        await CommentCache.delete_cached_comments_by_task(redis, task_id)
        return deleted_count

    @staticmethod
    async def update_comment(
        db: AsyncSession, redis, comment_id: int, comment: CommentUpdate
    ):
        """
        Updates the contents of the comment and retains changes in the database and cache.

        Args:
            DB (AsyncSession): Database session.
            Redis: Client Redis for caching.
            Comment_id (int): Comment identifier.
            Comment (CommentPdate): Data for updating the comment.

        Returns:
            Updated_comment (Comment): updated comment.
        """
        updated_comment = await CommentRepository.update_comment(
            db, comment_id, comment.content
        )
        if updated_comment:
            await CommentCache.cache_comment(
                redis, updated_comment.task_id, updated_comment.id, updated_comment
            )
        return updated_comment
