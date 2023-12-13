from uuid import uuid4


def get_task_id() -> str:
    return str(uuid4())
