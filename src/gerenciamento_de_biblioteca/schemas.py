from datetime import datetime

from pydantic import BaseModel, Field


class Message(BaseModel):
    message: str


class BookSchema(BaseModel):
    title: str
    author: str
    year: int


class BookPublic(BaseModel):
    id: int
    title: str
    author: str
    year: int
    available: bool
    created_at: datetime
    updated_at: datetime


class BookList(BaseModel):
    books: list[BookPublic]


class FilterPage(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, default=10)


class FilterBook(FilterPage):
    title: str | None = Field(default=None, min_length=3, max_length=20)


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    year: int | None = None
    available: bool | None = None
