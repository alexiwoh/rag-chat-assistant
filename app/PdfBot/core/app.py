from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


def create_app() -> FastAPI:
    """
    Creates and configures a FastAPI application instance.

    - Mounts the '/static' route to serve static files like CSS, JS, etc.
    - Dynamically resolves the path to the static directory, regardless of where the app is run from.

    Returns:
        FastAPI: A fully configured FastAPI application.
    """
    app = FastAPI()

    # Dynamically resolve the absolute path to the 'static' directory
    # Assumes static folder lives at project_root/static
    static_dir = Path(__file__).resolve().parent.parent.parent / "static"
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    return app
