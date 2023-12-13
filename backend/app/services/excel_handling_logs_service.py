from uuid import UUID

from app.db.models.excel_handling_logs import ExcelHandlingLog
from app.repositories.excel_handling_logs_repo import ExcelHandlingLogRepo


class ExcelHandlingLogService:
    def __init__(self, repo: ExcelHandlingLogRepo):
        self._repo = repo

    def get(self, uuid: UUID) -> ExcelHandlingLog:
        pass

    def get_all(self) -> list[ExcelHandlingLog]:
        pass

    def create(
        self,
        uuid: UUID,
        filename: str,
        status: str,
        log: str,
        error_type: str,
    ) -> ExcelHandlingLog:
        pass

    def delete(self, uuid: UUID) -> None:
        pass
