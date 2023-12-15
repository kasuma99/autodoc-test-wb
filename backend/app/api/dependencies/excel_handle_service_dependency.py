from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.dependencies.db_session_dependency import get_db_session
from app.repositories.excel_handle_logs_repo import ExcelHandleLogRepo
from app.services.excel_handle_service import ExcelHandleService


def get_excel_handling_service(
    session: Session = Depends(get_db_session),
) -> ExcelHandleService:
    excel_handling_service = ExcelHandleService(
        repo=ExcelHandleLogRepo(session=session)
    )
    return excel_handling_service
