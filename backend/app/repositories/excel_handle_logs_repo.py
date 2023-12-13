from sqlalchemy.orm import Session, Query

from app.db.models.excel_handle_logs import ExcelHandlingLog


class ExcelHandleLogRepo:
    def __init__(self, session: Session):
        self._session = session
        self._object = ExcelHandlingLog

    def _query(self) -> Query:
        return self._session.query(self._object)
