from datetime import datetime

from sqlalchemy import Column, DateTime, String, Enum
from sqlalchemy_utils import UUIDType  # type: ignore

from app.db.models import Base
from app.enum.excel_handle_errors import ExcelHandleError
from app.enum.excel_handle_status import ExcelHandleStatus


class ExcelHandleLog(Base):
    __tablename__ = "excel_handle_logs"

    uuid = Column(UUIDType(binary=False), primary_key=True)  # type: ignore
    created_date = Column(DateTime, default=datetime.utcnow)  # type: ignore
    filename = Column(String, nullable=False)  # type: ignore
    status = Column(Enum(ExcelHandleStatus))  # type: ignore
    log = Column(String, nullable=False)  # type: ignore
    error_type = Column(Enum(ExcelHandleError))  # type: ignore
