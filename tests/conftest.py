from typing import Any, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from gerenciamento_de_biblioteca.database import get_session
from gerenciamento_de_biblioteca.main import app
from gerenciamento_de_biblioteca.models import table_registry


@pytest.fixture
def client(session: AsyncSession) -> Generator[TestClient]:

    def get_session_override() -> AsyncSession:
        return session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def engine() -> Generator[AsyncEngine, Any, None]:
    with PostgresContainer("postgres:17", driver="psycopg") as postgres:
        yield create_async_engine(postgres.get_connection_url())


@pytest_asyncio.fixture
async def session(engine: Generator[AsyncEngine, Any, None]):
    async with engine.begin() as conn:  # type: ignore
        await conn.run_sync(table_registry.metadata.create_all)  # type: ignore

    async with AsyncSession(engine, expire_on_commit=False) as session:  # pyright: ignore[reportArgumentType]
        yield session

    async with engine.begin() as conn:  # type: ignore
        await conn.run_sync(table_registry.metadata.drop_all)  # type: ignore
