import traceback
from typing import BinaryIO

from celery import Celery  # type: ignore

from app.config import get_config
from app.db.session import create_db_session
from app.db.setup import db_setup
from app.repositories.excel_handle_logs_repo import ExcelHandleLogRepo
from app.services.excel_handle_service import ExcelHandleService


def configure_redis_url() -> str:
    redis_config = get_config().redis
    if redis_config is None:
        raise RuntimeError("Redis connection configuration is undefined")

    broker_url = f"redis://{redis_config.host}:{redis_config.port}/{redis_config.db}"
    return broker_url


redis_url = configure_redis_url()

celery_app = Celery(main="worker", broker=redis_url, backend=redis_url)
db_setup()


@celery_app.task
def process_excel_file_task(
    task_id: str,
    filename: str,
    content_type: str,
    file: BinaryIO,
):
    session = create_db_session()
    try:
        service = ExcelHandleService(repo=ExcelHandleLogRepo(session=session))

        service.process_file(
            task_id=task_id,
            filename=filename,
            content_type=content_type,
            file=file,
        )
        session.commit()

    except Exception as e:
        traceback.print_exc()
        session.rollback()

    finally:
        session.close()
