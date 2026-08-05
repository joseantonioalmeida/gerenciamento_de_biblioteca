import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Configuração simples e limpa com o logging padrão do Python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger("api.requests")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        response = await call_next(request)

        process_time = (time.perf_counter() - start_time) * 1000  # em ms
        status_code = response.status_code
        middleware_name = self.__class__.__name__

        logger.info(
            f"{middleware_name} | {request.method} {request.url.path} "
            f"-> Status: {status_code} | Processed in {process_time:.2f}ms"
        )

        return response
