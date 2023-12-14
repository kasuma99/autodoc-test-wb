from typing import BinaryIO

from app.tasks.celery_app import celery_app
from app.db.session import create_db_session
from app.repositories.excel_handle_logs_repo import ExcelHandleLogRepo
from app.services.excel_handle_service import ExcelHandleService
