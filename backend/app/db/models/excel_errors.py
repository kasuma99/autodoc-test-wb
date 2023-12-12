from datetime import datetime

from sqlalchemy import Column, DateTime, String, Enum

from app.db import Base
from app.db.models.base_model import DBModel
from app.enum.excel_error_types import ExcelErrorType


class ExcelError(Base, DBModel):
    __tablename__ = "excel_errors"

    created_date = Column(DateTime, default=datetime.utcnow)
    filename = Column(String, nullable=False)
    log = Column(String, nullable=False)
    type = Column(Enum(ExcelErrorType))
