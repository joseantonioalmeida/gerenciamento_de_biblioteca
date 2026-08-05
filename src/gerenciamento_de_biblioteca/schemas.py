from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


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
    user_id: int
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


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    updated_at: datetime


class UserList(BaseModel):
    users: list[UserPublic]


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str
