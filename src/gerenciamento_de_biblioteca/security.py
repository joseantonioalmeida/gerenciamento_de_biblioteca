from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gerenciamento_de_biblioteca.database import get_session
from gerenciamento_de_biblioteca.models import User
from gerenciamento_de_biblioteca.settings import Settings

SECRET_KEY = Settings().SECRET_KEY  # type:ignore
ALGORITHM = Settings().ALGORITHM  # type:ignore
ACCESS_TOKEN_EXPIRED_MINUTES = Settings().ACCESS_TOKEN_EXPIRE_MINUTES  # type:ignore

pwd_context = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token/")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    # Adiciona um tempo de expiração
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRED_MINUTES
    )

    to_encode.update({"exp": expire})

    encode_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt


async def get_current_user(
    session: Annotated[AsyncSession, Depends(get_session)],
    token: str = Depends(oauth2_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode(token, SECRET_KEY, ALGORITHM)
        subject_email = payload.get("sub")
        if not subject_email:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception
    except ExpiredSignatureError:
        raise credentials_exception

    user = await session.scalar(
        select(User).where(User.email == subject_email)
    )

    if not user:
        raise credentials_exception

    return user
