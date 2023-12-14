from fastapi import APIRouter, status, Depends, HTTPException

from app.api.dependencies.excel_handle_service_dependency import (
    get_excel_handling_service,
)
from app.schemas.excel_handle_logs_schema import ExcelHandleLogSchema
from app.services.excel_handle_service import ExcelHandleService

router = APIRouter(
    prefix="/excel-logs",
    tags=["Processed Excel Files Logs"],
)


@router.get(
    path="/{task_id}",
    response_model=ExcelHandleLogSchema,
    status_code=status.HTTP_200_OK,
)
async def get_log(
    task_id: str,
    service: ExcelHandleService = Depends(get_excel_handling_service),
):
    """
    Retrieves the processing log for an Excel file handling task based on the given task ID.

    Parameters:
        task_id (str): The unique identifier of the background task for which the logs are requested.
        service (ExcelHandleService): The service responsible for handling Excel file
                                      operations, injected through dependency injection.

    Returns:
        ExcelHandleLogSchema: A Pydantic model containing the detailed log of the specified task.
    """

    excel_log = service.get_log(uuid=task_id)
    return excel_log


@router.get(
    path="",
    response_model=list[ExcelHandleLogSchema],
    status_code=status.HTTP_200_OK,
)
async def get_logs(
    service: ExcelHandleService = Depends(get_excel_handling_service),
):
    """
    Retrieves all the processing logs for an Excel file handling task.

    Parameters:
        service (ExcelHandleService): The service responsible for handling Excel file
                                      operations, injected through dependency injection.

    Returns:
        list[ExcelHandleLogSchema]: A list of Pydantic models containing the detailed log of the specified task.
    """
    excel_logs = service.get_logs()
    return excel_logs
