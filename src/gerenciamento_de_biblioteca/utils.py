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


def mostrar_menu() -> None:
    print("""
=== Biblioteca ===
"1 - Cadastrar livros
"2 - Listar livros
"3 - Procurar livro pelo título
"4 - Editar livro
"5 - Remover livro
"6 - Emprestar livro
"7 - Devolver livro
"8 - Mostrar quantidade de livros
"99 - Sair""")


def ler_id() -> int | None:
    try:
        return int(input("Digite o id do livro:"))
    except ValueError:
        print("Digite um número inteiro.")
        return None


def buscar_livro_por_id(biblioteca: Biblioteca, livro_id: int) -> Livro | None:
    for livro in biblioteca:
        if livro["id"] == livro_id:
            return livro
    return None


def obter_livro(biblioteca: Biblioteca) -> Livro | None:
    id_int = ler_id()
    if id_int is None:
        return None

    livro = buscar_livro_por_id(biblioteca, id_int)

    if livro is None:
        print("Livro não encontrado.")
        return None

    return livro
