import asyncio
import json
import logging
from threading import Lock

import redis.asyncio as aioredis
from redis.exceptions import (
    ConnectionError as RedisConnectionError,
)
from redis.exceptions import (
    TimeoutError as RedisTimeoutError,
)

from gerenciamento_de_biblioteca.settings import Settings

settings = Settings()  # type:ignore
redis_client = aioredis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    socket_connect_timeout=0.2,
    socket_timeout=0.2,
)
logger = logging.getLogger("api.cache")

_cache_metrics_lock = Lock()
_cache_metrics = {"hits": 0, "misses": 0}


def _is_cache_unavailable_error(exc: Exception) -> bool:
    if isinstance(
        exc,
        (
            RedisConnectionError,
            RedisTimeoutError,
            OSError,
            TimeoutError,
            asyncio.CancelledError,
        ),
    ):
        return True
    if isinstance(exc, RuntimeError) and "Event loop is closed" in str(exc):
        return True
    return False


def reset_cache_metrics() -> None:
    with _cache_metrics_lock:
        _cache_metrics["hits"] = 0
        _cache_metrics["misses"] = 0


def get_cache_metrics() -> dict[str, int]:
    with _cache_metrics_lock:
        return {
            "hits": _cache_metrics["hits"],
            "misses": _cache_metrics["misses"],
        }


async def get_cache(key: str):
    try:  # noqa: PLW0717
        data = await redis_client.get(key)
        if data is None:
            with _cache_metrics_lock:
                _cache_metrics["misses"] += 1
            return None

        with _cache_metrics_lock:
            _cache_metrics["hits"] += 1

        return json.loads(data) if data else None
    except Exception as exc:  # noqa: BLE001
        if _is_cache_unavailable_error(exc):
            with _cache_metrics_lock:
                _cache_metrics["misses"] += 1
            logger.warning(
                "Redis cache unavailable while reading %s: %s", key, exc
            )
            return None
        raise


async def set_cache(key: str, value: dict | list, expire: int = 300):
    try:
        await redis_client.set(key, json.dumps(value), ex=expire)
    except Exception as exc:  # noqa: BLE001
        if _is_cache_unavailable_error(exc):
            logger.warning(
                "Redis cache unavailable while writing %s: %s", key, exc
            )
            return
        raise


async def invalidate_books_cache():
    try:
        keys = [key async for key in redis_client.scan_iter("books:*")]
        if keys:
            await redis_client.delete(*keys)
    except Exception as exc:  # noqa: BLE001
        if _is_cache_unavailable_error(exc):
            logger.warning(
                "Redis cache unavailable while invalidating books: %s", exc
            )
            return
        raise
