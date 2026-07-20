# Sistema de Gerenciamento de Biblioteca

Aplicação em linha de comando desenvolvida em Python para gerenciar um acervo de livros de forma simples, organizada e eficiente.

## Visão Geral

Este projeto foi criado para oferecer um sistema básico de biblioteca com funcionalidades de cadastro, listagem, busca, edição, remoção, empréstimo e devolução de livros. A interface é interativa e executada diretamente no terminal.

## Funcionalidades

- Cadastrar novos livros
- Listar todos os livros cadastrados
- Buscar livros por título
- Editar informações de um livro existente
- Remover livros do acervo
- Emprestar livros
- Devolver livros
- Exibir quantidade total, disponível e emprestada

## Tecnologias Utilizadas

- Python 3.14
- [uv](https://docs.astral.sh/uv/) para gerenciamento do ambiente virtual e dependências
- [Ruff](https://github.com/astral-sh/ruff) para lint e formatação
- [Pyright](https://github.com/microsoft/pyright) para análise estática de tipos
- [Pytest](https://pytest.org/) para testes

## Requisitos

- Python 3.14 ou superior
- [uv](https://docs.astral.sh/uv/getting-started/) instalado no sistema

## Instalação

Clone o repositório e acesse a pasta do projeto:

```bash
git clone <https://github.com/joseantonioalmeida/gerenciamento_de_biblioteca>
cd gerenciamento_de_biblioteca
```

Crie e configure o ambiente virtual com o comando abaixo:

```bash
uv sync
```

Isso irá instalar as dependências definidas no projeto e preparar o ambiente para execução.

## Execução

Você pode executar a aplicação de duas formas:

```bash
uv run biblioteca
```

ou

```bash
uv run python -m gerenciamento_de_biblioteca.main
```

Ao iniciar, o sistema exibirá um menu com as opções disponíveis.

## Menu da Aplicação

As principais opções do sistema são:

1. Cadastrar livro
2. Listar livros
3. Procurar livro por título
4. Editar livro
5. Remover livro
6. Emprestar livro
7. Devolver livro
8. Mostrar quantidade de livros
99. Sair

## Estrutura do Projeto

```text
.
├── pyproject.toml
├── README.md
├── src/
│   └── gerenciamento_de_biblioteca/
│       ├── __init__.py
│       ├── main.py
│       └── utils.py
```

### Descrição dos arquivos

- [src/gerenciamento_de_biblioteca/main.py](src/gerenciamento_de_biblioteca/main.py): contém a lógica principal do menu e as operações da aplicação.
- [src/gerenciamento_de_biblioteca/utils.py](src/gerenciamento_de_biblioteca/utils.py): reúne funções utilitárias para entrada de dados, validação e exibição de informações.
- [src/gerenciamento_de_biblioteca/__init__.py](src/gerenciamento_de_biblioteca/__init__.py): arquivo de inicialização do pacote.
- [pyproject.toml](pyproject.toml): configurações do projeto, dependências, scripts e ferramentas de qualidade.

## Desenvolvimento

### Verificar lint e formatação

```bash
uv run ruff check .
uv run ruff format .
```

### Verificar tipos

```bash
uv run pyright
```

### Executar testes

```bash
uv run pytest
```

## Autor

José Antônio Almeida