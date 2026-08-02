from http import HTTPStatus

import factory
import pytest

from gerenciamento_de_biblioteca.models import Book


class BookFactory(factory.Factory):  # type:ignore
    class Meta:  # type: ignore
        model = Book

    title = factory.Faker("text")  # type:ignore
    author = factory.Faker("text")  # type:ignore
    year = 2026
    available = True


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


@pytest.mark.asyncio
async def test_read_books(client, session):
    # Arrange
    expected_book = 1
    year = 2026
    book = BookFactory(title="FastAPI", author="Jose")

    session.add(book)
    await session.commit()

    # ACT
    response = client.get("/books/?title=FastAPI")

    # Assert
    assert len(response.json()["books"]) == expected_book
    assert response.json()["books"][0]["title"] == "FastAPI"
    assert response.json()["books"][0]["author"] == "Jose"
    assert response.json()["books"][0]["year"] == year
    assert response.json()["books"][0]["id"] == expected_book


@pytest.mark.asyncio
async def test_read_books_without_filter(client, session):
    expected_books = 3
    books = BookFactory.create_batch(3)
    session.add_all(books)
    await session.commit()

    response = client.get("/books/")

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["books"]) == expected_books


@pytest.mark.asyncio
async def test_update_book(client, session):
    book = BookFactory()
    session.add(book)
    await session.commit()

    response = client.patch(
        "/books/1/",
        json={
            "title": "Title Patch",
            "author": "Jose Patch",
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["title"] == "Title Patch"
    assert response.json()["author"] == "Jose Patch"


def test_patch_book_not_db_book(client):
    response = client.patch("/books/999/", json={})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Book not found."}


@pytest.mark.asyncio
async def test_delete_book(client, session):
    book = BookFactory()
    session.add(book)
    await session.commit()

    response = client.delete("/books/1/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "message": "Book has been deleted successfully."
    }


def test_delete_book_not_db_book(client):
    response = client.delete("/books/999/")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Book not found."}
