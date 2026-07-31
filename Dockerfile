FROM python:3.14-slim

# instala o uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_SYSTEM_PYTHON=1 \
    PYTHONPATH=/app/src

# Copia os arquivos mínimos necessários para o build do pacote
COPY pyproject.toml uv.lock README.md ./
COPY src ./src

# Instala apenas dependências de produção
RUN uv sync --frozen --no-dev

# Agora copia o restante
COPY . .

RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]