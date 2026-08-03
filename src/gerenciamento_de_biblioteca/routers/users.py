from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gerenciamento_de_biblioteca.database import get_session
from gerenciamento_de_biblioteca.models import User
from gerenciamento_de_biblioteca.schemas import UserPublic, UserSchema
from gerenciamento_de_biblioteca.security import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])

Session = Annotated[AsyncSession, Depends(get_session)]


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
