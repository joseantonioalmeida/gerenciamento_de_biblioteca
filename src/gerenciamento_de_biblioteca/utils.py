from typing import TypedDict


class Livro(TypedDict):
    id: int
    titulo: str
    autor: str
    ano: int
    disponivel: bool


Biblioteca = list[Livro]


def mostrar_livro(livro: Livro) -> None:
    print("ID: ", livro["id"])
    print("Titulo: ", livro["titulo"])
    print("Autor: ", livro["autor"])
    print("Ano: ", livro["ano"])
    print("Disponível: ", "Sim" if livro["disponivel"] else "Não")
