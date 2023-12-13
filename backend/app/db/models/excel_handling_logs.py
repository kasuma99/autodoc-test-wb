from datetime import datetime

from sqlalchemy import Column, DateTime, String, Enum
from sqlalchemy_utils import UUIDType

from app.db import Base
from app.enum.excel_handling_errors import ExcelHandlingError
from app.enum.excel_handling_status import ExcelHandlingStatus


class ExcelHandlingLog(Base):
    __tablename__ = "excel_handling_log"

    uuid = Column(UUIDType(binary=False), primary_key=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    filename = Column(String, nullable=False)
    status = Column(Enum(ExcelHandlingStatus))
    log = Column(String, nullable=False)
    type = Column(Enum(ExcelHandlingError))
