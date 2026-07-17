from typing import TypedDict


class Livro(TypedDict):
    id: int
    titulo: str
    autor: str
    ano: int


def menu() -> None:
    biblioteca: list[Livro] = []
    while True:
        print("\n=== Biblioteca ===")
        print("1 - Cadastrar livros")
        print("2 - Listar livros")
        print("99 - Sair")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            cadastrar_livro(biblioteca)
        elif opcao == "2":
            listar_livros(biblioteca)
        elif opcao == "99":
            print("Até logo!")
            break
        else:
            print("Opção inválida.")


def cadastrar_livro(biblioteca: list[Livro]) -> None:
    while True:
        titulo = input("Digite o título do livro: ").strip()
        if not titulo:
            continue
        autor = input("Digite o autor do livro: ").strip()
        if not autor:
            continue

        try:
            ano = int(input("Digite o ano do livro: "))
        except ValueError:
            print("Digite um ano válido.")
            continue

        biblioteca.append(
            {
                "id": len(biblioteca) + 1,
                "titulo": titulo,
                "autor": autor,
                "ano": ano,
            }
        )
        continuar = (
            input("Deseja cadastrar mais livros? (SIM ou NÃO): ").strip().upper()
        )
        if continuar.startswith("S"):
            continue

        break


def listar_livros(biblioteca: list[Livro]) -> None:
    print("=" * 30)
    print("=" * 11, "LIVROS", "=" * 11)
    for livro in biblioteca:
        print("ID", livro["id"])
        print("titulo", livro["titulo"])
        print("autor", livro["autor"])
        print("ano", livro["ano"])
        print("-" * 30)
    print("=" * 30)


def main() -> None:
    menu()


if __name__ == "__main__":
    main()
