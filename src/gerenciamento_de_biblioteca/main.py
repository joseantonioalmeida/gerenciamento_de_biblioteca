from typing import TYPE_CHECKING

from sqlalchemy import select

from gerenciamento_de_biblioteca.database import get_session
from gerenciamento_de_biblioteca.models import Livro
from gerenciamento_de_biblioteca.utils import (
    ler_ano,
    ler_autor,
    ler_titulo,
    mostrar_livro,
    mostrar_menu,
    obter_livro,
)

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def menu(session: Session) -> None:
    acoes = {
        "1": cadastrar_livro,
        "2": listar_livros,
        "3": buscar_livro_pelo_titulo,
        "4": editar_livro,
        "5": remover_livro,
        "6": emprestar_livro,
        "7": devolver_livro,
        "8": mostrar_quantidade,
    }
    while True:
        mostrar_menu()

        opcao = input("Escolha: ").strip()

        if opcao == "99":
            print("Até logo!")
            break
        funcao_escolhida = acoes.get(opcao)

        if funcao_escolhida:
            # executa a função
            funcao_escolhida(session)
        else:
            print("Opção inválida.")


def cadastrar_livro(session: Session) -> None:
    titulo = ler_titulo()
    autor = ler_autor()
    ano = ler_ano()

    db_livro = session.scalar(select(Livro).where(Livro.titulo == titulo))

    if db_livro:
        print("Livro já cadastrado.")
        return

    db_livro = Livro(
        titulo=titulo,
        autor=autor,
        ano=ano,
    )

    session.add(db_livro)
    session.commit()

    print("Livro cadastrado com sucesso!")


def listar_livros(session: Session) -> None:
    livros = session.scalars(select(Livro)).all()
    if not livros:
        print("Nenhum livro cadastrado.")
        return
    print("=" * 30)
    print("=" * 11, "LIVROS", "=" * 11)
    for livro in livros:
        mostrar_livro(livro)
        print("-" * 30)
    print("=" * 30)


def buscar_livro_pelo_titulo(session: Session) -> None:
    titulo_digitado = input("Digite o titulo: ").strip()

    livros = session.scalars(
        select(Livro).where(Livro.titulo.ilike(f"{titulo_digitado}%"))
    ).all()

    if not livros:
        print("Livro não encontrado.")
        return

    print("-" * 30)
    for livro in livros:
        mostrar_livro(livro)

    print("-" * 30)


def editar_livro(session: Session) -> None:
    livro = obter_livro(session)
    if livro is None:
        return

    titulo = ler_titulo()
    titulo_existente = session.scalar(
        select(Livro).where(Livro.titulo == titulo, Livro.id != livro.id)
    )
    if titulo_existente:
        print("Já existe um livro com esse Título.")
        return

    autor = ler_autor()
    ano = ler_ano()

    livro.titulo = titulo
    livro.autor = autor
    livro.ano = ano

    session.commit()

    print("Livro atualizado com sucesso!")


def remover_livro(session: Session) -> None:
    livro = obter_livro(session)
    if livro is None:
        return

    session.delete(livro)
    session.commit()
    print("Livro deletado com sucesso.")


def emprestar_livro(session: Session) -> None:
    livro = obter_livro(session)
    if livro is None:
        return

    if livro.disponivel:
        livro.disponivel = False
        session.commit()
        print("Livro emprestado com sucesso.")
    else:
        print("Esse livro já está emprestado.")


def devolver_livro(session: Session) -> None:
    livro = obter_livro(session)
    if livro is None:
        return

    if not livro.disponivel:
        livro.disponivel = True
        session.commit()
        print("Livro devolvido com sucesso.")
    else:
        print("Esse livro está disponível.")


def mostrar_quantidade(session: Session) -> None:
    print("=" * 30)
    livros = session.scalars(select(Livro)).all()

    total_de_livros = len(livros)
    qtd_disponivel = sum(1 for livro in livros if livro.disponivel)
    qtd_emprestado = total_de_livros - qtd_disponivel

    print(
        f"""TOTAL DE LIVROS
        Total: {total_de_livros}
        Disponíveis: {qtd_disponivel}
        Emprestados: {qtd_emprestado}"""
    )
    print("=" * 30)


def main() -> None:
    with get_session() as session:
        menu(session)


if __name__ == "__main__":
    main()
