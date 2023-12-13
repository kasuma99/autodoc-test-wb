from fastapi import APIRouter, status, UploadFile

router = APIRouter(
    prefix="/excel",
    tags=["Excel Files Handling Endpoints"],
)


@router.post(
    path="",
    response_model=...,
    status_code=status.HTTP_202_ACCEPTED,
)
async def upload_file_to_process(
    excel_file: UploadFile,
):
    # upload Excel file and send it to celery worker
    pass


@router.get(
    path="/{uuid}",
    response_model=...,
    status_code=status.HTTP_200_OK,
)
async def get_processed_file(
    uuid: str,
):
    # return processed Excel file if it was processed, else ...
    pass


@router.get(
    path="/check_status/{uuid}",
    response_model=...,
    status_code=status.HTTP_200_OK,
)
async def check_processing_status():
    pass
