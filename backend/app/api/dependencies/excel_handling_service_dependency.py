from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.dependencies.db_session_dependency import get_db_session
from app.repositories.excel_handling_logs_repo import ExcelHandlingLogRepo
from app.services.excel_handling_service import ExcelHandlingService


def get_excel_handling_service(
    session: Session = Depends(get_db_session),
) -> ExcelHandlingService:
    excel_handling_service = ExcelHandlingService(
        repo=ExcelHandlingLogRepo(session=session)
    )
    return excel_handling_service
