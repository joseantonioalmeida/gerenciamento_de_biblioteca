from typing import TYPE_CHECKING

from sqlalchemy import select

from gerenciamento_de_biblioteca.models import Livro

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def mostrar_livro(livro: Livro) -> None:
    print("ID: ", livro.id)
    print("Titulo: ", livro.titulo)
    print("Autor: ", livro.autor)
    print("Ano: ", livro.ano)
    print("Disponível: ", "Sim" if livro.disponivel else "Não")


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


def buscar_livro_por_id(session: Session, livro_id: int) -> Livro | None:
    livro = session.scalar(select(Livro).where(Livro.id == livro_id))

    if not livro:
        return None

    return livro


def obter_livro(session: Session) -> Livro | None:
    id_int = ler_id()
    if id_int is None:
        return None

    livro = buscar_livro_por_id(session, id_int)

    if livro is None:
        print("Livro não encontrado.")
        return None

    return livro


def ler_titulo() -> str:
    while True:
        titulo = input("Título: ").strip()
        if titulo:
            return titulo
        print("Digite o título.")


def ler_autor() -> str:
    while True:
        autor = input("Autor: ").strip()
        if autor:
            return autor
        print("Digite o autor.")


def ler_ano() -> int:
    while True:
        try:
            return int(input("Ano: "))
        except ValueError:
            print("Somente um ano válido.")
