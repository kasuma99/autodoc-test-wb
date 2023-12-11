from functools import cache

from pydantic_settings import BaseSettings


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


class AppConfig(BaseSettings):
    db: DbConfig | None = None
    redis: RedisConfig | None = None


def _get_config():
    return AppConfig(_env_nested_delimiter="__")


@cache
def get_config():
    return _get_config()
