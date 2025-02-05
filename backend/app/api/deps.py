from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    try:
        db = AsyncSessionLocal()
        yield db
    finally:
        await db.close()


# TODO: Add authentication dependencies here when implementing user management
