from collections.abc import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from gerenciamento_de_biblioteca.database import get_session


@pytest.mark.asyncio
async def test_get_session_should_yield_async_session() -> None:
    generator: AsyncGenerator[AsyncSession] = get_session()

    session = await anext(generator)

    assert isinstance(session, AsyncSession)

    await generator.aclose()
