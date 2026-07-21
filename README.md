# Sistema de Gerenciamento de Biblioteca

Aplicação de linha de comando em Python para gerenciar um acervo de livros com persistência local usando SQLite, SQLAlchemy e Alembic.

## Visão Geral

Este projeto entrega um sistema de biblioteca simples e profissional, com persistência de dados em banco SQLite e controle de esquema por migrações Alembic.

A aplicação oferece cadastro, listagem, busca, edição, exclusão, empréstimo e devolução de livros em um ambiente de terminal.

## Funcionalidades

- Persistência de dados com SQLite
- Mapeamento ORM com SQLAlchemy
- Controle de esquema com Alembic
- Cadastro de livros
- Listagem de livros
- Busca por título
- Edição de informações do livro
- Remoção de livros
- Empréstimo e devolução
- Relatórios de livros totais, disponíveis e emprestados

## Tecnologias Utilizadas

- Python 3.14
- SQLite para armazenamento local
- SQLAlchemy para mapeamento objeto-relacional
- Alembic para migrações de banco de dados
- uv para gerenciamento de ambiente e execução
- Ruff para lint e formatação
- Pyright para análise estática de tipos
- Pytest para testes automatizados

## Requisitos

- Python 3.14 ou superior
- uv instalado no sistema

## Instalação

Clone o repositório e acesse a pasta do projeto:

```bash
git clone https://github.com/joseantonioalmeida/gerenciamento_de_biblioteca
cd gerenciamento_de_biblioteca
```

Instale as dependências do projeto:

```bash
uv sync
```

## Configuração do Banco de Dados

O projeto utiliza o arquivo de banco SQLite `biblioteca.db` na raiz do projeto.

Antes de executar a aplicação, aplique as migrações do Alembic:

```bash
uv run python -m alembic upgrade head
```

As migrações estão armazenadas em `migrations/versions/`.

## Execução

Execute a aplicação usando o entry point do projeto:

```bash
uv run biblioteca
```

ou diretamente:

```bash
uv run python -m gerenciamento_de_biblioteca.main
```

## Estrutura do Projeto

```text
.
├── alembic.ini
├── migrations/
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
│       └── 2c3839e674f5_create_livro_table.py
├── pyproject.toml
├── README.md
├── src/
│   └── gerenciamento_de_biblioteca/
│       ├── __init__.py
│       ├── database.py
│       ├── main.py
│       ├── models.py
│       └── utils.py
```

## Descrição dos arquivos

- `src/gerenciamento_de_biblioteca/main.py`: ponto de entrada da aplicação e lógica de menu.
- `src/gerenciamento_de_biblioteca/database.py`: configuração da conexão SQLite e criação de sessões SQLAlchemy.
- `src/gerenciamento_de_biblioteca/models.py`: definição do modelo `Livro` com mapeamento ORM.
- `src/gerenciamento_de_biblioteca/utils.py`: funções auxiliares de entrada e exibição.
- `migrations/`: arquivos de migração Alembic para versionamento do esquema.
- `alembic.ini`: configuração do Alembic.
- `pyproject.toml`: definição do pacote, dependências e ferramentas de desenvolvimento.

## Desenvolvimento

### Lint e formatação

```bash
uv run ruff check .
uv run ruff format .
```

### Verificação de tipos

```bash
uv run pyright
```

### Execução de testes

```bash
uv run pytest
```

## Autor

José Antônio Almeida
