from http import HTTPStatus

from fastapi import FastAPI

from gerenciamento_de_biblioteca.routers import auth, books, users
from gerenciamento_de_biblioteca.schemas import Message

app = FastAPI(title="Gerenciamento de biblioteca API")

app.include_router(users.router)
app.include_router(books.router)
app.include_router(auth.router)


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root() -> dict[str, str]:
    return {"message": "Bem vindo a API de gerenciamento de biblioteca!"}
