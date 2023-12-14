from typing import BinaryIO

from .celery_app import celery_app
from ..db.session import create_db_session
from ..repositories.excel_handle_logs_repo import ExcelHandleLogRepo
from ..services.excel_handle_service import ExcelHandleService


@celery_app.task
def process_excel_file(
    task_id: str,
    filename: str,
    file: BinaryIO,
    content_type: str,
):
    session = create_db_session()
    try:
        service = ExcelHandleService(repo=ExcelHandleLogRepo(session=session))

        service.process_file(
            file=file,
            filename=filename,
            content_type=content_type,
            task_id=task_id,
        )

    finally:
        session.close()
