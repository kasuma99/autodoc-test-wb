from sqlalchemy.orm import Session, Query

from app.db.models.excel_handling_logs import ExcelHandlingLog


class ExcelHandlingLogRepo:
    def __init__(self, session: Session):
        self._session = session
        self._object = ExcelHandlingLog

    def _query(self) -> Query:
        return self._session.query(self._object)
