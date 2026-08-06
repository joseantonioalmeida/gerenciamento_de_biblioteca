from http import HTTPStatus
from typing import cast

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from slowapi import _rate_limit_exceeded_handler  # noqa: PLC2701
from slowapi.errors import RateLimitExceeded
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request

from gerenciamento_de_biblioteca.exceptions import (
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from gerenciamento_de_biblioteca.middleaware import LoggingMiddleware
from gerenciamento_de_biblioteca.routers import auth, books, health, users
from gerenciamento_de_biblioteca.schemas import Message
from gerenciamento_de_biblioteca.security import limiter

app = FastAPI(title="Gerenciamento de biblioteca API")

# 1. Adicionar o Middleware de Logging
app.add_middleware(LoggingMiddleware)


async def _rate_limit_exception_handler(request: Request, exc: Exception):
    return _rate_limit_exceeded_handler(request, cast(RateLimitExceeded, exc))


async def _starlette_http_exception_handler(request: Request, exc: Exception):
    return await http_exception_handler(
        request, cast(StarletteHTTPException, exc)
    )


async def _request_validation_exception_handler(
    request: Request, exc: Exception
):
    return await validation_exception_handler(
        request, cast(RequestValidationError, exc)
    )


# 2. Registrar Handlers de Exceção
app.add_exception_handler(
    StarletteHTTPException, _starlette_http_exception_handler
)
app.add_exception_handler(
    RequestValidationError, _request_validation_exception_handler
)
app.add_exception_handler(Exception, global_exception_handler)

# Registra o Limiter no estado da aplicação
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exception_handler)

app.include_router(users.router)
app.include_router(books.router)
app.include_router(auth.router)
app.include_router(health.router)


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root() -> dict[str, str]:
    return {"message": "Bem vindo a API de gerenciamento de biblioteca!"}
