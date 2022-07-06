from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.base import Base
from app.database.session import engine
from app.core import config, handlers
from app.routes import home


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

    _app.add_event_handler("startup", handlers.create_start_app_handler(_app))
    _app.add_event_handler("shutdown", handlers.create_stop_app_handler(_app))

    return _app

Base.metadata.create_all(bind=engine)

app = get_application()

app.include_router(home.router)
