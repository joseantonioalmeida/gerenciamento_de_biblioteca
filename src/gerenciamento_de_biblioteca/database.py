from typing import TYPE_CHECKING

from gerenciamento_de_biblioteca.settings import Settings

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

engine = create_async_engine(Settings().DATABASE_URL)  # type:ignore


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
