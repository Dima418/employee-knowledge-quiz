from typing import Callable
from fastapi import FastAPI

from app.database.connection import open_db_connection, close_db_connection


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await open_db_connection(app)

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        await close_db_connection(app)

    return stop_app