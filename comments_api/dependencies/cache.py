from cache.comments import CommentCache


async def get_redis_client():
    return await CommentCache.get_redis()
