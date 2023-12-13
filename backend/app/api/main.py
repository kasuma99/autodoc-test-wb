from importlib import import_module
from pathlib import Path

import uvicorn
from fastapi import FastAPI


def connect_routers(fastapi_app: FastAPI, routers_folder: str = "routers"):
    """
    Automatically includes all routers from the specified folder into the FastAPI app.

    :param fastapi_app: The FastAPI application instance.
    :param routers_folder: The folder containing router modules.
    """
    routers_dir = Path(routers_folder)
    if not routers_dir.is_dir():
        raise ValueError(
            f"The folder {routers_folder} does not exist or is not a directory."
        )

    for file in routers_dir.iterdir():
        if file.is_file() and file.suffix == ".py" and not file.name.startswith("__"):
            router_module_name = (
                file.stem
            )  # Get the file name without the '.py' extension
            module_path = f"{routers_folder}.{router_module_name}"
            try:
                router_module = import_module(module_path)

                if hasattr(router_module, "router"):
                    print("1")
                    fastapi_app.include_router(router_module.router)
            except Exception as e:
                print(f"Error importing {module_path}: {e}")


if __name__ == "__main__":
    app = FastAPI()

    # Connect all routers from folder routers
    connect_routers(fastapi_app=app)

    uvicorn.run(app, host="0.0.0.0", port=8000)
