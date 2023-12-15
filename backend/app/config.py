from functools import cache

from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_nested_delimiter = "__"


class DbConfig(BaseSettings):
    host: str
    port: int

    name: str
    user: str
    password: str


class RedisConfig(BaseSettings):
    host: str
    port: int
    db: int = 0


class ExcelConfig(BaseSettings):
    folder_path: str
    mime_xlsx: str
    mime_xls: str
    column_date: str
    column_sales: str


class AppConfig(BaseConfig):
    db: DbConfig | None
    redis: RedisConfig | None
    excel: ExcelConfig | None


@cache
def _get_config():
    return AppConfig(_env_file=[".env"])


def get_config():
    return _get_config()
