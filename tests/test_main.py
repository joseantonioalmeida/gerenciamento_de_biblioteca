from http import HTTPStatus

import pytest

from gerenciamento_de_biblioteca import cache as cache_module


def test_read_root_should_return_a_dictionary(client) -> None:
    response = client.get("/")

    assert response.json() == {
        "message": "Bem vindo a API de gerenciamento de biblioteca!"
    }


def test_health_check_should_return_ok_when_database_is_available(
    client,
) -> None:
    response = client.get("/health/")

    assert response.status_code == HTTPStatus.OK
    assert response.json()["status"] == "ok"


def test_metrics_endpoint_should_be_available(client) -> None:
    response = client.get("/metrics")

    assert response.status_code == HTTPStatus.OK
    assert response.headers["content-type"].startswith("text/plain")


@pytest.mark.asyncio
async def test_get_cache_returns_none_when_redis_is_unavailable(
    monkeypatch,
) -> None:
    async def raise_connection_error(*args, **kwargs):
        raise ConnectionError("redis unavailable")

    monkeypatch.setattr(
        cache_module.redis_client, "get", raise_connection_error
    )

    assert await cache_module.get_cache("books:test") is None


@pytest.mark.asyncio
async def test_cache_metrics_track_hits_and_misses(monkeypatch) -> None:
    cache_module.reset_cache_metrics()

    class FakeRedisClient:
        def __init__(self) -> None:
            self.store = {"books:cached": '{"books": []}'}

        async def get(self, key: str):
            return self.store.get(key)

    monkeypatch.setattr(cache_module, "redis_client", FakeRedisClient())

    await cache_module.get_cache("books:cached")
    await cache_module.get_cache("books:missing")

    metrics = cache_module.get_cache_metrics()

    assert metrics["hits"] == 1
    assert metrics["misses"] == 1
