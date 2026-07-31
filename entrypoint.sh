#!/bin/sh
set -e

echo "Aplicando migrações..."
uv run alembic upgrade head

echo "Iniciando API..."
exec uv run uvicorn gerenciamento_de_biblioteca.main:app --host 0.0.0.0 --port 8000
