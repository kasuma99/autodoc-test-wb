from pydantic import BaseModel


class CeleryTaskSchema(BaseModel):
    task_id: str
    status: str  # Could not find all possible celery task's statuses so will leave it as a string (not enum)
