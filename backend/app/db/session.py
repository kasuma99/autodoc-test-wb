from sqlalchemy.orm import Session

from .setup import SessionLocal


def create_db_session() -> Session:
    return SessionLocal()
