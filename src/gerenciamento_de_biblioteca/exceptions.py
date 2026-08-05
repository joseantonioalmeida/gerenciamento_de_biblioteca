import logging
from http import HTTPStatus

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("api")


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
):
    """Trata exceções HTTP disparadas manualmente na aplicação
    (ex: HTTPException)."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
        },
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    """Padroniza erros de validação do Pydantic (HTTP 422)."""
    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content={
            "status_code": HTTPStatus.UNPROCESSABLE_ENTITY,
            "detail": "Validation Error",
        },
    )


async def global_exception_handler(request: Request, exc: Exception):
    """Captura qualquer erro não tratado/inesperado (HTTP 500)
    ou erros de banco."""
    logger.error(
        f"Erro não tratado na rota {request.url.path}: {exc}",
        exc_info=True,
    )
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content={
            "status_code": HTTPStatus.INTERNAL_SERVER_ERROR,
            "detail": "Internal Server Error",
        },
    )
