from pydantic import BaseModel


class CeleryTaskSchema(BaseModel):
    task_id: str
    status: str


class CeleryTaskNoExcelSchema(CeleryTaskSchema):
    message: str
