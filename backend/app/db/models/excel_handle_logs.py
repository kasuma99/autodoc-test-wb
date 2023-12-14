from datetime import datetime

from sqlalchemy import Column, DateTime, String, Enum
from sqlalchemy_utils import UUIDType

from app.db.models import Base
from app.enum.excel_handle_errors import ExcelHandleError
from app.enum.excel_handle_status import ExcelHandleStatus


class ExcelHandleLog(Base):
    __tablename__ = "excel_handle_logs"

    uuid = Column(UUIDType(binary=False), primary_key=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    filename = Column(String, nullable=False)
    status = Column(Enum(ExcelHandleStatus))
    log = Column(String, nullable=False)
    error_type = Column(Enum(ExcelHandleError))
