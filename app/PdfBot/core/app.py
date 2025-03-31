from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


def create_app():
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="static"), name="static")
    return app
