"""Application handlers.

Handlers are functions that are called when the application is started or stopped.

"""

from typing import Callable
from fastapi import FastAPI

from app.database.connection import open_db_connection, close_db_connection


def create_start_app_handler(app: FastAPI) -> Callable:
    """Called when the application is started.

    This function is used to create the database connection.

    Args:
        app (FastAPI): FastAPI instance.

    Returns:
        (Callable): Handler that is called when the application is started.
    """
    async def start_app() -> None:
        await open_db_connection(app)

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    """Called when the application is stopped.

    This function is used to close the database connection.

    Args:
        app (FastAPI): FastAPI instance.

    Returns:
        (Callable): Handler that is called when the application is stopped.
    """
    async def stop_app() -> None:
        await close_db_connection(app)

    return stop_app