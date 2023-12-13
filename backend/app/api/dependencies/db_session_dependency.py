from typing import Iterator

from sqlalchemy.orm import Session

from app.db.session import create_db_session


def get_db_session() -> Iterator[Session]:
    session = create_db_session()
    try:
        yield session
    finally:
        session.close()
