from gerenciamento_de_biblioteca.utils import Biblioteca, ler_id, mostrar_livro


def menu(biblioteca: Biblioteca) -> None:
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

        if opcao == "99":
            print("Até logo!")
            break
        funcao_escolhida = acoes.get(opcao)

        if funcao_escolhida:
            # executa a função
            funcao_escolhida(biblioteca)
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
                "id": max((livro["id"] for livro in biblioteca), default=0) + 1,
                "titulo": titulo,
                "autor": autor,
                "ano": ano,
                "disponivel": True,
            }
        )
        print("Livro cadastrado com sucesso!")
        continuar = (
            input("Deseja cadastrar mais livros? (SIM ou NÃO): ").strip().upper()
        )
        if continuar.startswith("S"):
            continue

        break


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
    id_int = ler_id()
    if id_int is None:
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


def remover_livro(biblioteca: Biblioteca) -> None:
    id_int = ler_id()
    if id_int is None:
        return

    for livro in biblioteca:
        if livro["id"] == id_int:
            biblioteca.remove(livro)
            print("Livro deletado com sucesso.")
            return

    print("Livro não encontrado.")


def emprestar_livro(biblioteca: Biblioteca) -> None:
    id_int = ler_id()
    if id_int is None:
        return

    for livro in biblioteca:
        if livro["id"] == id_int:
            if livro["disponivel"]:
                livro["disponivel"] = False
                print("Livro emprestado com sucesso.")
            else:
                print("Esse livro já está emprestado.")
            return
    print("Livro não encontrado.")


def devolver_livro(biblioteca: Biblioteca) -> None:

    id_int = ler_id()
    if id_int is None:
        return

    for livro in biblioteca:
        if livro["id"] == id_int:
            if not livro["disponivel"]:
                livro["disponivel"] = True
                print("Livro devolvido com sucesso.")
            else:
                print("Esse livro está disponível.")
            return
    print("Livro não encontrado.")


def mostrar_quantidade(biblioteca: Biblioteca) -> None:
    print("=" * 30)
    total_de_livros = len(biblioteca)
    qtd_disponivel = sum(1 for livro in biblioteca if livro["disponivel"])
    qtd_emprestado = total_de_livros - qtd_disponivel

    print(
        f"""TOTAL DE LIVROS
        Total: {total_de_livros}
        Disponíveis: {qtd_disponivel}
        Emprestados: {qtd_emprestado}"""
    )
    print("=" * 30)


def main() -> None:
    biblioteca: Biblioteca = []
    menu(biblioteca)


if __name__ == "__main__":
    main()
