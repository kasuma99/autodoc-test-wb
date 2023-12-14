import uvicorn

from app.api.main import app


def start_fastapi_app():
    uvicorn.run(app=app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    start_fastapi_app()
