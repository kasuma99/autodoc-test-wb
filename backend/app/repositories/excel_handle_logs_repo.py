from uuid import UUID

from sqlalchemy import asc
from sqlalchemy.orm import Session, Query

from app.db.models.excel_handle_logs import ExcelHandleLog


class ExcelHandleLogRepo:
    def __init__(self, session: Session):
        self._session = session
        self._object = ExcelHandleLog

    def _query(self) -> Query:
        return self._session.query(self._object)

    def get(self, uuid: UUID) -> ExcelHandleLog | None:
        return self._query().filter(self._object.uuid == uuid).first()

    def get_all(self, order_by="created_date", desc=True) -> list[ExcelHandleLog]:
        return self._query().order_by(order_by if desc else asc(order_by)).all()

    def create(self, model: ExcelHandleLog) -> ExcelHandleLog:
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return model

    def delete(self, model: ExcelHandleLog | None) -> None:
        if model is not None:
            self._session.delete(model)
