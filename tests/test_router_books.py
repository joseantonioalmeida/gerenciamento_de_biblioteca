from http import HTTPStatus

from gerenciamento_de_biblioteca.models import Book


def test_create_book(client, mock_db_time):
    with mock_db_time(model=Book) as time:
        response = client.post(
            "/books/",
            json={
                "title": "Title Teste",
                "author": "Jose Teste",
                "year": 2026,
            },
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {
            "id": 1,
            "title": "Title Teste",
            "author": "Jose Teste",
            "year": 2026,
            "available": True,
            "created_at": time.isoformat(),
            "updated_at": time.isoformat(),
        }

        # Testar o title igual do que já está criado
        response = client.post(
            "/books/",
            json={
                "title": "Title Teste",
                "author": "Jose Teste 2",
                "year": 2027,
            },
        )

        assert response.status_code == HTTPStatus.CONFLICT
        assert response.json() == {"detail": "Book already registered."}
