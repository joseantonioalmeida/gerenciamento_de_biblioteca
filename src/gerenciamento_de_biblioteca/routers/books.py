from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select

from gerenciamento_de_biblioteca.cache import (
    get_cache,
    invalidate_books_cache,
    set_cache,
)
from gerenciamento_de_biblioteca.database import get_session
from gerenciamento_de_biblioteca.models import Book, User
from gerenciamento_de_biblioteca.schemas import (
    BookList,
    BookPublic,
    BookSchema,
    BookUpdate,
    FilterBook,
    Message,
)
from gerenciamento_de_biblioteca.security import get_current_user

router = APIRouter(prefix="/books", tags=["books"])


from sqlalchemy.ext.asyncio import AsyncSession  # noqa: E402

Current_user = Annotated[User, Depends(get_current_user)]
Session = Annotated[AsyncSession, Depends(get_session)]


MAX_BORROWED_BOOKS = 3


@router.post("/", status_code=HTTPStatus.CREATED, response_model=BookPublic)
async def create_livro(
    book: BookSchema, session: Session, current_user: Current_user
):
    db_book = await session.scalar(
        select(Book).where(
            Book.title == book.title, Book.user_id == current_user.id
        )
    )
    if db_book:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Book already registered."
        )

    db_book = Book(
        title=book.title,
        author=book.author,
        year=book.year,
        user_id=current_user.id,
        borrower_id=None,
    )

    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)

    await invalidate_books_cache()

    return db_book


@router.get("/", status_code=HTTPStatus.OK, response_model=BookList)
async def read_books(
    session: Session,
    book_filter: Annotated[FilterBook, Query()],
    current_user: Current_user,
):
    cache_key = (
        f"books:offset={book_filter.offset}:"
        f"limit={book_filter.limit}:title={book_filter.title}"
    )
    cached_books = await get_cache(cache_key)
    if cached_books is not None:
        return cached_books

    query = select(Book)

    if book_filter.title:
        query = query.filter(Book.title.ilike(f"%{book_filter.title}%"))

    result = await session.scalars(
        query.limit(book_filter.limit).offset(book_filter.offset)
    )
    books = result.all()
    response_data = {
        "books": [
            BookPublic.model_validate(book).model_dump(mode="json")
            for book in books
        ]
    }

    await set_cache(cache_key, response_data, expire=300)

    return response_data


@router.patch(
    "/{book_id}/", status_code=HTTPStatus.OK, response_model=BookPublic
)
async def patch_book(
    book_id: int,
    session: Session,
    book: BookUpdate,
    current_user: Current_user,
):
    db_book = await session.scalar(
        select(Book).where(Book.id == book_id, Book.user_id == current_user.id)
    )

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Book not found."
        )

    for key, value in book.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)

    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)
    await invalidate_books_cache()

    return db_book


@router.delete(
    "/{book_id}/", status_code=HTTPStatus.OK, response_model=Message
)
async def delete_book(
    book_id: int, session: Session, current_user: Current_user
):
    db_book = await session.scalar(
        select(Book).where(Book.id == book_id, Book.user_id == current_user.id)
    )
    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Book not found."
        )

    await session.delete(db_book)
    await session.commit()
    await invalidate_books_cache()
    return {"message": "Book has been deleted successfully."}


@router.post(
    "/{book_id}/borrow/", status_code=HTTPStatus.OK, response_model=BookPublic
)
async def borrow_book(
    book_id: int, current_user: Current_user, session: Session
):
    db_book = await session.scalar(select(Book).where(Book.id == book_id))

    # Primeiro verifica se o livro existe
    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Book not found.",
        )

    # Depois verifica se o livro está disponível
    if not db_book.available:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Book is already borrowed by another user.",
        )

    # Por fim, verifica se a quantidade de livros emprestados pelo user é maior
    #  que a quantidade máxima.
    if len(current_user.borrowed_books) >= MAX_BORROWED_BOOKS:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=(
                f"User cannot borrow more than {MAX_BORROWED_BOOKS} "
                "books at the same time."
            ),
        )

    db_book.available = False
    db_book.borrower_id = current_user.id

    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)

    await invalidate_books_cache()

    return db_book


@router.post(
    "/{book_id}/return/", status_code=HTTPStatus.OK, response_model=BookPublic
)
async def return_book(
    book_id: int, current_user: Current_user, session: Session
):
    # Busca o livro emprestado pelo próprio user
    db_book = await session.scalar(
        select(Book).where(
            Book.id == book_id, Book.borrower_id == current_user.id
        )
    )
    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Book not found or not borrowed by this user.",
        )

    # Devolve o livro
    db_book.available = True
    db_book.borrower_id = None

    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)

    await invalidate_books_cache()

    return db_book
