from fastapi import FastAPI

from app.api.routers import excel_handle_logs_router, excel_handle_tasks_router

app = FastAPI()

app.include_router(excel_handle_logs_router.router)
app.include_router(excel_handle_tasks_router.router)
