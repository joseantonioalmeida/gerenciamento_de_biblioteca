from typing import TypedDict


class Livro(TypedDict):
    id: int
    titulo: str
    autor: str
    ano: int


Biblioteca = list[Livro]


def menu(biblioteca: Biblioteca) -> None:
    while True:
        print("\n=== Biblioteca ===")
        print("1 - Cadastrar livros")
        print("2 - Listar livros")
        print("3 - Procurar livro pelo título")
        print("4 - Editar livro")
        print("5 - Remover livro")
        print("6 - Emprestar livro")
        print("7 - Devolver livro")
        print("8 - Mostrar quantidade de livros")
        print("99 - Sair")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            cadastrar_livro(biblioteca)
        elif opcao == "2":
            listar_livros(biblioteca)
        elif opcao == "3":
            buscar_livro_pelo_titulo(biblioteca)
        elif opcao == "4":
            editar_livro(biblioteca)
        elif opcao == "99":
            print("Até logo!")
            break
        else:
            print("Opção inválida.")


def cadastrar_livro(biblioteca: Biblioteca) -> None:
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
        print("Livro cadastrado com sucesso!")
        continuar = (
            input("Deseja cadastrar mais livros? (SIM ou NÃO): ").strip().upper()
        )
        if continuar.startswith("S"):
            continue

        break


def mostrar_livro(livro: Livro) -> None:
    print("ID", livro["id"])
    print("titulo", livro["titulo"])
    print("autor", livro["autor"])
    print("ano", livro["ano"])


def listar_livros(biblioteca: Biblioteca) -> None:
    if not biblioteca:
        print("Nenhum livro cadastrado.")
        return
    print("=" * 30)
    print("=" * 11, "LIVROS", "=" * 11)
    for livro in biblioteca:
        mostrar_livro(livro)
        print("-" * 30)
    print("=" * 30)


def buscar_livro_pelo_titulo(biblioteca: Biblioteca) -> None:
    titulo_digitado = input("Digite o titulo: ").strip()

    encontrado = False
    for livro in biblioteca:
        if titulo_digitado.lower() in livro["titulo"].lower():
            encontrado = True

            print("-" * 30)
            mostrar_livro(livro)

    print("-" * 30)
    if not encontrado:
        print("Livro não encontrado.")


def editar_livro(biblioteca: Biblioteca) -> None:
    try:
        id_int = int(input("Digite o id do livro: "))
    except ValueError:
        print("Digite número inteiro.")
        return

    for livro in biblioteca:
        if id_int == livro["id"]:
            titulo = input("Digite o novo título: ").strip()
            autor = input("Digite o novo autor: ").strip()

            while True:
                try:
                    ano = int(input("Digite o novo ano: "))
                    break
                except ValueError:
                    print("Digite número inteiro.")

            livro["titulo"] = titulo
            livro["autor"] = autor
            livro["ano"] = ano

            print("Livro atualizado com sucesso!")
            return
    print("Livro não encontrado.")


def main() -> None:
    biblioteca: list[Livro] = []
    menu(biblioteca)


if __name__ == "__main__":
    main()
