from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Message(BaseModel):
    message: str


# --- BOOK SCHEMAS ---
class BookSchema(BaseModel):
    title: str
    author: str
    year: int


class BookUserPublic(BaseModel):
    """Schema do livro simplificado para ser exibido dentro do UserPublic."""

    id: int
    title: str
    author: str
    year: int
    user_id: int
    available: bool
    borrower_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


class BookPublic(BookUserPublic):
    """Herda de BookUserPublic e adiciona os campos de data/hora"""

    created_at: datetime
    updated_at: datetime


class BookList(BaseModel):
    books: list[BookPublic]


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    year: int | None = None
    available: bool | None = None


# --- USER SCHEMAS ---
class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    books: list[BookUserPublic]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None


# --- Token SCHEMAS ---
class Token(BaseModel):
    access_token: str
    token_type: str


# --- Filter SCHEMAS ---
class FilterPage(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, default=10)


class FilterBook(FilterPage):
    title: str | None = Field(default=None, min_length=3, max_length=20)
