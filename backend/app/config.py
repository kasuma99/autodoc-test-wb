import os
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


class AppConfig(BaseConfig):
    db: DbConfig | None
    redis: RedisConfig | None


@cache
def _get_config():
    return AppConfig(_env_file=[".env"])


def get_config():
    return _get_config()
