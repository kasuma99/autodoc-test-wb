from fastapi import APIRouter, status


router = APIRouter(
    prefix="/excel",
    tags=["Excel Files Handling Endpoints"],
)


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


@router.post(
    path="",
    response_model=...,
    status_code=status.HTTP_202_ACCEPTED,
)
async def upload_file_to_process(
    excel_file: ...,
):
    # upload Excel file and send it to celery worker
    pass
