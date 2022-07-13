"""Application entry point.

"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.base_class import Base
from app.database.session import engine
from app.core import config, handlers
from app.routes import auth, home, user, quiz
from app.database import base


origins = ["http://localhost:8080", "http://127.0.0.1:8080"]

def get_application():
    """Create and return the initialised FastAPI application.

    Returns:
        (FastAPI): FastAPI instance.
    """
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

    _app.include_router(auth.router)
    _app.include_router(home.router)
    _app.include_router(user.router)
    _app.include_router(quiz.router)

    Base.metadata.create_all(bind=engine)

    return _app

app = get_application()
