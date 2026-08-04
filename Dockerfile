FROM python:3.14-slim

WORKDIR /app

COPY . .

ENV PYTHONUNBUFFERED=1 \
PYTHONDONTWRITEBYTECODE=1 \
UV_COMPILE_BYTECODE=1 \
UV_SYSTEM_PYTHON=1 \
PYTHONPATH=/app/src

RUN chmod +x entrypoint.sh

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Instala apenas dependências de produção
RUN uv sync --frozen --no-dev

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]