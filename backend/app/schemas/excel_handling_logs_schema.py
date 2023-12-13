from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ExcelHandlingLogsSchema(BaseModel):
    uuid: UUID
    created_date: datetime
    filename: str
    status: str
    log: str
    error_type: str