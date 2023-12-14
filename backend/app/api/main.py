from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.api.routers import excel_handle_logs_router, excel_handle_tasks_router
from app.db.setup import db_setup
from app.exceptions.not_found_exception import NotFoundException
from app.exceptions.uuid_exception import UUIDException

db_setup()

app = FastAPI()

app.include_router(excel_handle_logs_router.router)
app.include_router(excel_handle_tasks_router.router)


@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message},
    )


@app.exception_handler(UUIDException)
async def uuid_exception_handler(request: Request, exc: UUIDException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": exc.message},
    )
