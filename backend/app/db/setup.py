from sqlalchemy import create_engine
from sqlalchemy.future import Engine
from sqlalchemy.orm import sessionmaker

from app.config import DbConfig, get_config

SessionLocal = sessionmaker()


def configure_db_session(engine: Engine):
    SessionLocal.configure(bind=engine)


def get_db_url(db_config: DbConfig):
    return f"postgresql://{db_config.user}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.name}"


def db_setup(db_config: DbConfig | None = None):
    if db_config is None:
        config = get_config()
        db_config = config.db

    if db_config is None:
        raise RuntimeError("Database connection configuration is undefined")

    db_url = get_db_url(db_config=db_config)
    engine = create_engine(url=db_url)
    configure_db_session(engine=engine)
