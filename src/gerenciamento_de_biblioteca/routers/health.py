from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from gerenciamento_de_biblioteca.cache import get_cache_metrics
from gerenciamento_de_biblioteca.database import get_session

router = APIRouter(prefix="/health", tags=["Health"])

Session = Annotated[AsyncSession, Depends(get_session)]


@router.get("/", status_code=HTTPStatus.OK)
async def health_check(session: Session):
    try:
        await session.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": "healthy",
            "cache": {
                **get_cache_metrics(),
                "backend": "redis",
            },
        }
    except Exception as exc:
        raise HTTPException(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            detail=f"Database connection error: {exc}",
        )
