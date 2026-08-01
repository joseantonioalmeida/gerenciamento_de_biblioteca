from gerenciamento_de_biblioteca.models import Book


def test_book_uses_the_migration_table_name() -> None:
    assert Book.__tablename__ == "book"
