from sqlalchemy import create_engine
from sqlalchemy.orm import Session

DATABASE_URL = "sqlite:///biblioteca.db"

engine = create_engine(DATABASE_URL)


def get_session() -> Session:
    return Session(engine)
