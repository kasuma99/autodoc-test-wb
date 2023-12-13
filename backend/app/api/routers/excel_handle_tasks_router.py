from celery.result import AsyncResult
from fastapi import APIRouter, status, UploadFile, Depends

from app.api.dependencies.task_id_depenency import get_task_id
from app.schemas.celery_task_schema import CeleryTaskSchema
from app.tasks.celery_app import celery_app
from app.tasks.process_excel_file import process_excel_file

router = APIRouter(
    prefix="/task",
    tags=["Excel Files Process Tasks"],
)


@router.post(
    path="",
    response_model=CeleryTaskSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def upload_file_to_process(
    upload_file: UploadFile,
    task_id: str = Depends(get_task_id),
):
    """
    Handles the upload of an Excel file and initiates its processing as a background task.

    Args:
        upload_file (UploadFile): The Excel file to be processed.
        task_id (str): The unique identifier for the task, obtained through dependency injection.

    Returns:
        dict: A dictionary containing the 'task_id' and the current 'status' of the background task.
    """
    # Dispatch the background task that processes uploaded file
    task = process_excel_file.apply_async(
        args=[
            task_id,
            upload_file.content_type,
            upload_file.file,
        ],
        task_id=task_id,
    )
    # Create an AsyncResult instance using the task.id
    task_result = AsyncResult(task.id, app=celery_app)

    return {"task_id": task_id, "status": task_result.status}


@router.get(
    path="/{task_id}",
    response_model=CeleryTaskSchema,
    status_code=status.HTTP_200_OK,
)
async def get_processed_file(
    task_id: str,
):
    # return processed Excel file if it was processed, else ...
    pass


@router.get(
    path="/check_status/{task_id}",
    response_model=CeleryTaskSchema,
    status_code=status.HTTP_200_OK,
)
async def check_task_status(
    task_id: str,
):
    """
    Retrieves the current status of a background task using its task ID.

    Args:
        task_id (str): The unique identifier of the background task whose status is to be checked.

    Returns:
        dict: A dictionary containing the 'task_id' and the current 'status' of the background task.
    """
    # Create an AsyncResult instance using the task_id
    task_result = AsyncResult(task_id, app=celery_app)

    return {"task_id": task_id, "status": task_result.status}
