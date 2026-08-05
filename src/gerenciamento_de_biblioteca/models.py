from datetime import datetime  # noqa: TC003

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    books: Mapped[list["Book"]] = relationship(
        init=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


@table_registry.mapped_as_dataclass
class Book:
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    author: Mapped[str]
    year: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    available: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
