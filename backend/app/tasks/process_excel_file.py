from typing import BinaryIO

from .celery_app import celery_app


@celery_app.task
def process_excel_file(
    task_id: str,
    file: BinaryIO,
    content_type: str,
):
    pass
