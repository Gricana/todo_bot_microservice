import json
import redis.asyncio as redis
from schemas.comment import CommentResponse
from settings import settings


class CommentCache:
    """
    Class for working with caching comments in Redis.
    """

    @staticmethod
    async def get_redis():
        """
        Creates a connection to Redis.

        Returns:
            REDIS: Client Object Redis.
        """
        return await redis.from_url(settings.REDIS_URL, decode_responses=True)

    @staticmethod
    async def cache_comment(redis, task_id: str, comment_id: int, comment_data):
        """
        Cache the comment for the specified task in Redis.

        Args:
            REDIS (REDIS): an object of a client of a client.
            TASK_ID (str): the identifier of the task.
            Comment_id (int): Comment identifier.
            Comment_Data (DICT): Comment for caching.
        """
        comment_dict = CommentResponse.model_validate(comment_data).model_dump(
            mode='json'
        )

        await redis.hset(
            f"task:{task_id}:comments", comment_id, json.dumps(comment_dict)
        )

        await redis.expire(f"task:{task_id}:comments", settings.REDIS_TIMEOUT)

    @staticmethod
    async def get_cached_comments(redis, task_id: str):
        """
        Receives all the cache comments for the specified task.

        Args:
            REDIS (REDIS): an object of a client of a client.
            TASK_ID (str): the identifier of the task.

        Returns:
            dict: a dictionary with cache comments (Comment_id -> Commentresponse, or None if the comments have not been found.
        """
        cached_comments = await redis.hgetall(f"task:{task_id}:comments")

        if not cached_comments:
            return None

        parsed_comments = {}
        for key, value in cached_comments.items():
            if value:
                try:
                    data = json.loads(value.encode('utf-8'))
                    parsed_comments[key] = CommentResponse.model_validate(data)
                except json.JSONDecodeError:
                    print(f"Ошибка при декодировании JSON для ключа {key}")
            else:
                print(f"Пустое значение для ключа {key}")

        return parsed_comments

    @staticmethod
    async def delete_cached_comment(redis, task_id: str, comment_id: int):
        """
        Removes a specific comment from the cache.

        Args:
            REDIS (REDIS): an object of a client of a client.
            TASK_ID (str): the identifier of the task.
            Comment_id (int): Comment identifier for deleting.
        """
        await redis.hdel(f"task:{task_id}:comments", comment_id)

    @staticmethod
    async def delete_cached_comments_by_task(redis, task_id: str):
        """
        Removes all comments for the specified task from the cache.

        Args:
            REDIS (REDIS): an object of a client of a client.
            TASK_ID (str): the identifier of the task.
        """
        await redis.delete(f"task:{task_id}:comments")
