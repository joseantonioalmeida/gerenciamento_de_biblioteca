from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select

from gerenciamento_de_biblioteca.database import get_session
from gerenciamento_de_biblioteca.models import Book
from gerenciamento_de_biblioteca.schemas import (
    BookList,
    BookPublic,
    BookSchema,
    BookUpdate,
    FilterBook,
    Message,
)

router = APIRouter(prefix="/livros", tags=["livros"])


from sqlalchemy.ext.asyncio import AsyncSession  # noqa: E402

Session = Annotated[AsyncSession, Depends(get_session)]


@router.post("/", status_code=HTTPStatus.CREATED, response_model=BookPublic)
async def create_livro(book: BookSchema, session: Session):
    db_book = await session.scalar(
        select(Book).where(Book.title == book.title)
    )
    if db_book:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Book already registered."
        )

    db_book = Book(
        title=book.title,
        author=book.author,
        year=book.year,
    )

    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)

    return db_book


@router.get("/", status_code=HTTPStatus.OK, response_model=BookList)
async def read_books(
    session: Session, book_filter: Annotated[FilterBook, Query()]
):
    query = select(Book)

    if book_filter.title:
        query = query.filter(Book.title.ilike(f"%{book_filter.title}%"))

    books = await session.scalars(
        query.limit(book_filter.limit).offset(book_filter.offset)
    )

    return {"books": books}


@router.patch(
    "/{book_id}/", status_code=HTTPStatus.OK, response_model=BookPublic
)
async def patch_book(book_id: int, session: Session, book: BookUpdate):
    db_book = await session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Book not found."
        )

    for key, value in book.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)

    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)

    return db_book


@router.delete(
    "/{book_id}/", status_code=HTTPStatus.OK, response_model=Message
)
async def delete_book(book_id: int, session: Session):
    db_book = await session.scalar(select(Book).where(Book.id == book_id))
    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Book not found."
        )

    await session.delete(db_book)
    await session.commit()

    return {"message": "Book has been deleted successfully."}
