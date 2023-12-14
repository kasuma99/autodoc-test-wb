from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ExcelHandleLogSchema(BaseModel):
    uuid: UUID | str
    created_date: datetime
    filename: str
    status: str
    log: str
    error_type: str