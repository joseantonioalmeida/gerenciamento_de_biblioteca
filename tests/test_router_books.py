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
    user_id = None
    available = True
    borrower_id = None


def test_create_book(client, mock_db_time, user, token):
    with mock_db_time(model=Book) as time:
        response = client.post(
            "/books/",
            json={
                "title": "Title Teste",
                "author": "Jose Teste",
                "year": 2026,
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {
            "id": 1,
            "title": "Title Teste",
            "author": "Jose Teste",
            "year": 2026,
            "user_id": user.id,
            "available": True,
            "borrower_id": None,
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
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == HTTPStatus.CONFLICT
        assert response.json() == {"detail": "Book already registered."}


@pytest.mark.asyncio
async def test_read_books(client, session, token, user):
    # Arrange
    expected_book = 1
    year = 2026
    book = BookFactory(title="FastAPI", author="Jose", user_id=user.id)

    session.add(book)
    await session.commit()

    # ACT
    response = client.get(
        "/books/?title=FastAPI", headers={"Authorization": f"Bearer {token}"}
    )

    # Assert
    assert len(response.json()["books"]) == expected_book
    assert response.json()["books"][0]["title"] == "FastAPI"
    assert response.json()["books"][0]["author"] == "Jose"
    assert response.json()["books"][0]["year"] == year
    assert response.json()["books"][0]["id"] == expected_book
    assert response.json()["books"][0]["user_id"] == user.id


@pytest.mark.asyncio
async def test_read_books_without_filter(client, session, token, user):
    expected_books = 3
    books = BookFactory.create_batch(3, user_id=user.id)
    session.add_all(books)
    await session.commit()

    response = client.get(
        "/books/", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["books"]) == expected_books


@pytest.mark.asyncio
async def test_update_book(client, session, user, token):
    book = BookFactory(user_id=user.id)
    session.add(book)
    await session.commit()

    response = client.patch(
        "/books/1/",
        json={
            "title": "Title Patch",
            "author": "Jose Patch",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["title"] == "Title Patch"
    assert response.json()["author"] == "Jose Patch"


def test_patch_book_not_db_book(client, token):
    response = client.patch(
        "/books/999/", json={}, headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Book not found."}


@pytest.mark.asyncio
async def test_delete_book(client, session, user, token):
    book = BookFactory(user_id=user.id)
    session.add(book)
    await session.commit()

    response = client.delete(
        "/books/1/", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "message": "Book has been deleted successfully."
    }


def test_delete_book_not_db_book(client, token):
    response = client.delete(
        "/books/999/", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Book not found."}


@pytest.mark.asyncio
async def test_borrow_book(client, user, token, session):
    book: Book = BookFactory(user_id=user.id)
    session.add(book)
    await session.commit()
    await session.refresh(book)

    response = client.post(
        f"/books/{book.id}/borrow/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert not response.json()["available"]
    assert response.json()["borrower_id"] == user.id


def test_book_not_found_for_loan(client, token):
    response = client.post(
        "/books/999/borrow/", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Book not found."}


@pytest.mark.asyncio
async def test_book_is_already_borrowed_another_user(
    client, session, other_user, token
):
    book = BookFactory(
        available=False, user_id=other_user.id, borrower_id=other_user.id
    )
    session.add(book)
    await session.commit()
    await session.refresh(book)

    response = client.post(
        f"/books/{book.id}/borrow/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        "detail": "Book is already borrowed by another user."
    }


@pytest.mark.asyncio
async def test_the_number_of_books_borrowed_by_user_exceeds_the_maximum_limit(
    client, user, other_user, session, token
):
    MAX_BORROWED_BOOKS = 3

    books = BookFactory.create_batch(
        3,
        user_id=other_user.id,
        borrower_id=user.id,
        available=False,
    )

    session.add_all(books)
    await session.commit()

    book = BookFactory(user_id=user.id)
    session.add(book)
    await session.commit()
    await session.refresh(book)

    # Expira o cache do 'user' para forçar o sqlalchemy a recarregar
    # 'borrowed_books' na requisição
    await session.refresh(user)

    response = client.post(
        f"/books/{book.id}/borrow/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        "detail": (
            f"User cannot borrow more than {MAX_BORROWED_BOOKS} "
            "books at the same time."
        )
    }


@pytest.mark.asyncio
async def test_return_book(client, token, session, user, other_user):
    book = BookFactory(
        user_id=other_user.id,
        borrower_id=user.id,
        available=False,
    )
    session.add(book)
    await session.commit()
    await session.refresh(book)
    await session.refresh(user)

    response = client.post(
        f"/books/{book.id}/return/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["available"]
    assert response.json()["borrower_id"] is None


def test_return_book_not_found(client, token):
    response = client.post(
        "/books/999/return/", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        "detail": "Book not found or not borrowed by this user."
    }


@pytest.mark.asyncio
async def test_return_book_borrowed_another_user(
    client, token, session, user, other_user
):
    book = BookFactory(
        user_id=user.id,
        borrower_id=other_user.id,
        available=False,
    )
    session.add(book)
    await session.commit()
    await session.refresh(book)
    await session.refresh(user)

    response = client.post(
        f"/books/{book.id}/return/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        "detail": "Book not found or not borrowed by this user."
    }
