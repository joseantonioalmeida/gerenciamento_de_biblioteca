import asyncio
import sys
from http import HTTPStatus
from typing import TYPE_CHECKING

from fastapi import FastAPI

from gerenciamento_de_biblioteca.routers import books
from gerenciamento_de_biblioteca.schemas import Message

if TYPE_CHECKING:
    pass

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(title="Gerenciamento de biblioteca API")

app.include_router(books.router)


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root() -> dict[str, str]:
    return {"message": "Bem vindo a API de gerenciamento de biblioteca!"}
