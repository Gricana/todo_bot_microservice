from db import get_db
from sqlalchemy.ext.asyncio import AsyncSession


async def get_database() -> AsyncSession:
    return await get_db()
