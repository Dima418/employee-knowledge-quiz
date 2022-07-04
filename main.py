from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import home
from core import config


origins = ["http://localhost:8080", "http://127.0.0.1:8080"]

def get_application():
    _app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app

app = get_application()

app.include_router(home.router)
