from http import HTTPStatus
from typing import cast

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request

from gerenciamento_de_biblioteca.exceptions import (
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from gerenciamento_de_biblioteca.middleaware import LoggingMiddleware
from gerenciamento_de_biblioteca.routers import auth, books, users
from gerenciamento_de_biblioteca.schemas import Message

app = FastAPI(title="Gerenciamento de biblioteca API")

# 1. Adicionar o Middleware de Logging
app.add_middleware(LoggingMiddleware)


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

app.include_router(users.router)
app.include_router(books.router)
app.include_router(auth.router)


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root() -> dict[str, str]:
    return {"message": "Bem vindo a API de gerenciamento de biblioteca!"}
