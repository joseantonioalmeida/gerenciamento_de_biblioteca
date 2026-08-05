# Gerenciamento de Biblioteca API

API REST assíncrona para gerenciamento de usuários e livros construída com FastAPI, Pydantic, SQLAlchemy Async e PostgreSQL.

## Visão Geral

Este projeto é uma API moderna desenvolvida em Python 3.14 com foco em async, autenticação JWT e deploy via Docker. A aplicação oferece cadastro e gerenciamento de usuários e livros, com todas as operações protegidas por token JWT quando necessário.

## Tecnologias Utilizadas

- FastAPI
- Pydantic / Pydantic Settings
- SQLAlchemy Async
- Alembic
- PostgreSQL
- Docker / Docker Compose
- Uvicorn via `uv`
- Pytest para testes
- Ruff para lint e formatação
- Pyright para análise estática de tipos
- GitHub Actions para CI

## Arquitetura e Recursos

- Aplicação 100% assíncrona
- JWT Bearer para proteção de endpoints
- CRUD completo para usuários e livros
- API estruturada em routers (`auth`, `users`, `books`)
- Migrações de banco com Alembic
- Containerização com Docker e Docker Compose
- Workflow de CI em `.github/workflows/main.yaml`

## Middleware e Tratamento de Exceções

- Logging middleware centralizado para registrar método, rota, status e tempo de processamento
- Manipulação customizada de `HTTPException` com resposta JSON uniforme
- Padronização de erros de validação de request (`422 Unprocessable Entity`)
- Captura global de exceções não tratadas, com log de stack trace e resposta `500 Internal Server Error`
- Registro dos handlers em `main.py` para manter o aplicativo robusto e consistente

## Endpoints principais

### Autenticação

- `POST /auth/token/`
  - Gera token de acesso JWT a partir de email e senha
  - Retorna `access_token` e `token_type`
- `POST /auth/refresh-token/`
  - Atualiza o `access_token` para o usuário autenticado
  - Retorna um novo `access_token` e `token_type`

### Usuários

- `POST /users/`
  - Cria um novo usuário
  - Não exige autenticação
- `GET /users/`
  - Lista usuários com paginação `offset` e `limit`
  - Requer JWT
- `GET /users/{user_id}/`
  - Retorna os dados do usuário autenticado
  - Requer JWT
- `PATCH /users/{user_id}/`
  - Atualiza o usuário autenticado
  - Requer JWT
- `DELETE /users/{user_id}/`
  - Remove o usuário autenticado
  - Requer JWT

### Livros

- `POST /books/`
  - Cria um livro associado ao usuário autenticado
  - Requer JWT
- `GET /books/`
  - Lista livros com filtro opcional por `title`, `offset` e `limit`
  - Requer JWT
- `PATCH /books/{book_id}/`
  - Atualiza um livro do usuário autenticado
  - Requer JWT
- `DELETE /books/{book_id}/`
  - Exclui um livro do usuário autenticado
  - Requer JWT
- `POST /books/{book_id}/borrow/`
  - Empresta um livro para o usuário autenticado
  - Valida se o livro existe, está disponível e se o usuário não ultrapassou o limite de empréstimos
  - Requer JWT
- `POST /books/{book_id}/return/`
  - Devolve um livro emprestado pelo usuário autenticado
  - Requer JWT

## Segurança

- Autenticação via JWT usando o cabeçalho `Authorization: Bearer <token>`.
- O token JWT contém o campo `sub` com o email do usuário.
- A expiração do token é configurada por `ACCESS_TOKEN_EXPIRE_MINUTES`.
- `POST /users/` é o único endpoint de usuários acessível sem autenticação.
- Operações de `users` e `books` exigem o usuário autenticado e restringem atualizações/exclusões ao próprio usuário ou aos próprios livros.

## Estrutura do projeto

```text
.
├── .github/workflows/main.yaml
├── Dockerfile
├── compose.yaml
├── entrypoint.sh
├── pyproject.toml
├── README.md
├── .env-example
├── alembic.ini
├── migrations/
│   ├── env.py
│   ├── README
│   └── versions/
├── src/
│   └── gerenciamento_de_biblioteca/
│       ├── database.py
│       ├── main.py
│       ├── models.py
│       ├── routers/
│       │   ├── auth.py
│       │   ├── books.py
│       │   └── users.py
│       ├── schemas.py
│       ├── security.py
│       └── settings.py
└── tests/
```

## Configuração de environment variables

O projeto carrega variáveis de ambiente a partir de `.env` usando `pydantic-settings`.

Variáveis obrigatórias:

- `DATABASE_URL`
- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`

## Executando com Docker Compose

```bash
docker compose up --build
```

O serviço expõe a API em `http://0.0.0.0:8000`.

O `entrypoint.sh` aplica as migrações Alembic automaticamente e inicia o servidor Uvicorn.

## Executando localmente

1. Crie um arquivo `.env` a partir de `.env-example`
2. Instale as dependências:

```bash
uv sync
```

3. Execute o servidor:

```bash
uv run uvicorn gerenciamento_de_biblioteca.main:app --host 0.0.0.0 --port 8000
```

## Alembic e migrações

- Migrações estão em `migrations/versions`
- Para aplicar migrações localmente:

```bash
uv run alembic upgrade head
```

## Testes e qualidade

- Linter e formatação: `uv run ruff check .` e `uv run ruff format .`
- Verificação de tipos: `uv run pyright`
- Testes: `uv run pytest`

## CI / GitHub Actions

O pipeline de CI está configurado em `.github/workflows/main.yaml` para:

- instalar Python 3.14
- instalar `uv`
- instalar dependências via `uv sync --frozen`
- executar lint com `uv run task lint`
- executar testes com `uv run task test`

## Observações

- A API usa PostgreSQL como banco de dados.
- Todo o acesso a recursos protegidos passa por autenticação JWT.
- A arquitetura é baseada em rotas FastAPI com injeção de dependências Async SQLAlchemy.
