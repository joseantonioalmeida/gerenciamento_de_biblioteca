# Sistema de Gerenciamento de biblitoteca

**É um projeto utilizando apenas python**

## Sobre

Este projeto serve como um esqueleto moderno para projetos Python utilizando:

- Python 3.14
- Ambiente virtual ([uv](https://docs.astral.sh/uv/getting-started/))
- Lint e formatação com [Ruff](https://github.com/astral-sh/ruff)
- Tipagem estática e Lint com Pylance e [Pyright](https://github.com/microsoft/pyright)

---
## Gerenciando tudo com o uv

[uv](https://docs.astral.sh/uv/getting-started/) é uma ferramenta que promete bastante. Sua intenção é substituir praticamente todas as outras ferramentas: pip, pip-tools, pipx, poetry, pyenv, twine, virtualenv, e outras... Até agora tem cumprido tudo com perfeição. Além disso, é uma ferramenta extremamente rápida, escrita em Rust.

```sh
# Instalação do uv (Windows, Linux, Mac)
# Windows PowerShell:
iwr https://astral.sh/uv/install.ps1 -useb | iex

# Linux/macOS (curl)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```sh
# Cria o projeto completo
diretório: uv init nome-do-projeto

# Ou inicializa dentro de um projeto existente:
uv init
```

```sh
# Instala Python, cria venv e instala dependências em 1 comando
uv sync
```

```sh
# Instala pacotes
uv add requests ruff pyright

# Remove pacotes
uv remove requests

# Requerimentos via requirements.txt
uv add -r requirements.txt
```

```sh
# Executa scripts Python sem ativar venv
uv run src/main.py

# Instala ferramentas como ruff ou pyright globalmente
uv tool install ruff
uvx ruff
uv tool uninstall ruff
```
---

## Configuração do Git

```bash
# Inicia o repositório
git init # Não precisa fazer isso se a uv já fez

# Configura usuário global
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"

# Padroniza branches para 'main'
git config --global init.defaultBranch main
git branch -m main

# Padroniza finais de linha para multiplataforma
git config --global core.autocrlf input
git config --global core.eol lf

git config --list --global

# Primeiro commit
git add .
git commit -m "initial"

# Configurar o repositório
git remote add origin URL_REPO_SSH
git push origin main -u

# Nos próximos
git add .
git commit -m "MENSAGEM"
git push
```

---