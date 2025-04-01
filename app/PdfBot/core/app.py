from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


def create_app() -> FastAPI:
    app = FastAPI()

    # Dynamically resolve path to 'static' no matter where script is run from
    static_dir = Path(__file__).resolve().parent.parent.parent / "static"
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    return app
