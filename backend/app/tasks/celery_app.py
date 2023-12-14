from celery import Celery

from app.config import get_config


def configure_redis_url() -> str:
    redis_config = get_config().redis
    if redis_config is None:
        raise RuntimeError("Redis connection configuration is undefined")

    broker_url = f"redis://{redis_config.host}:{redis_config.port}/{redis_config.db}"
    return broker_url


# redis_url = configure_redis_url()

celery_app = Celery(
    main="worker",
    broker="redis://localhost:6379/0 ",
    backend="redis://localhost:6379/0 ",
)
