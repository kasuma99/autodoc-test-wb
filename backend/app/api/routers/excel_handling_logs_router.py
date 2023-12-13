from fastapi import APIRouter, status


router = APIRouter(
    prefix="/logs",
    tags=["Excel Handling Logs Endpoints"],
)


@router.get(
    path="/{uuid}",
    response_model=...,
    status_code=status.HTTP_200_OK,
)
async def get_handling_log(
        uuid: str,
):
    pass
