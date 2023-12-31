import os
from typing import Optional

from celery.result import AsyncResult  # type: ignore
from fastapi import APIRouter, status, UploadFile, Depends
from starlette.responses import FileResponse

from app.api.dependencies.task_id_depenency import get_task_id
from app.config import AppConfig, get_config
from app.schemas.celery_task_schema import (
    CeleryTaskSchema,
    CeleryTaskNoExcelSchema,
)
from app.tasks.celery_app import celery_app

from app.tasks.celery_app import process_excel_file_task

router = APIRouter(
    prefix="/excel-task",
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
    # Read the content of the file
    # Content is loaded entirely into memory.
    # If dealing with very large files, this might not be the most efficient solution...
    file_content = await upload_file.read()

    # Dispatch the background task that processes uploaded file
    task = process_excel_file_task.apply_async(
        args=[
            task_id,
            upload_file.filename,
            upload_file.content_type,
            file_content,
        ],
        task_id=task_id,
    )
    # Create an AsyncResult instance using the task.id
    task_result = AsyncResult(task.id, app=celery_app)

    return {"task_id": task_id, "status": task_result.status}


@router.get(
    path="/download/{task_id}",
    response_model=Optional[CeleryTaskNoExcelSchema],
    status_code=status.HTTP_200_OK,
)
async def get_processed_file(
    task_id: str,
    config: AppConfig = Depends(get_config),
):
    """
    Endpoint to download a processed Excel file using a given task ID.

    Args:
        task_id (str): The unique identifier for the task associated with the Excel file processing.
        config: An instance of AppConfig class

    Returns:
        FileResponse: A response object that represents the processed Excel file, allowing the client to download it.
        dict: A dictionary containing the 'task_id' and the 'message' of the background task.
    """
    # Check if task is completed using AsyncResult instance
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.status != "SUCCESS":
        return {
            "task_id": task_id,
            "status": task_result.status,
            "message": "File processing is not completed or task ID is invalid",
        }

    # Check if file exists that means the task is completed
    processed_file_path = os.path.join(config.excel.folder_path, f"{task_id}.xlsx")
    if not os.path.exists(path=processed_file_path):
        return {
            "task_id": task_id,
            "status": task_result.status,
            "message": "File processing error (check logs)",
        }

    return FileResponse(
        processed_file_path,
        media_type=config.excel.mime_xlsx,
        filename=processed_file_path,
    )


@router.get(
    path="/status/{task_id}",
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
