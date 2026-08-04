from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gerenciamento_de_biblioteca.database import get_session
from gerenciamento_de_biblioteca.models import User
from gerenciamento_de_biblioteca.schemas import (
    FilterPage,
    Message,
    UserList,
    UserPublic,
    UserSchema,
    UserUpdate,
)
from gerenciamento_de_biblioteca.security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter(prefix="/users", tags=["users"])

Session = Annotated[AsyncSession, Depends(get_session)]
Current_user = Annotated[User, Depends(get_current_user)]


@router.post("/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(session: Session, user: UserSchema):
    db_user = await session.scalar(
        select(User).where(
            (User.email == user.email) | (User.username == user.username)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Username already exists.",
            )

        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Email already exists."
        )

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@router.get("/", status_code=HTTPStatus.OK, response_model=UserList)
async def read_users(
    session: Session,
    current_user: Current_user,
    filter_page: Annotated[FilterPage, Query()],
):
    db_users = await session.scalars(
        select(User).offset(filter_page.offset).limit(filter_page.limit)
    )

    return {"users": db_users}


@router.get(
    "/{user_id}/", status_code=HTTPStatus.OK, response_model=UserPublic
)
async def detail_user(
    user_id: int, session: Session, current_user: Current_user
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Not enough permissions.",
        )
    return current_user


@router.patch(
    "/{user_id}/", status_code=HTTPStatus.OK, response_model=UserPublic
)
async def update_user(
    user_id: int,
    user: UserUpdate,
    session: Session,
    current_user: Current_user,
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Not enough permissions.",
        )

    for key, value in user.model_dump(exclude_unset=True).items():
        if key == "password":
            setattr(current_user, key, get_password_hash(value))
            continue
        setattr(current_user, key, value)

    session.add(current_user)
    await session.commit()
    await session.refresh(current_user)

    return current_user


@router.delete(
    "/{user_id}/", status_code=HTTPStatus.OK, response_model=Message
)
async def delete_user(
    user_id: int, current_user: Current_user, session: Session
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Not enough permissions.",
        )

    await session.delete(current_user)
    await session.commit()

    return {"message": "User deleted successfully."}
