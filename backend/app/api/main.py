from fastapi import FastAPI

from app.api.routers import excel_handle_logs_router, excel_handle_tasks_router
from app.db.setup import db_setup

db_setup()

app = FastAPI()

app.include_router(excel_handle_logs_router.router)
app.include_router(excel_handle_tasks_router.router)
