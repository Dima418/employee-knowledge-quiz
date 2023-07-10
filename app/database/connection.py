from fastapi import FastAPI
from databases import Database
from app.core.config import DATABASE_URL
import logging


logger = logging.getLogger(__name__)

async def open_db_connection(app: FastAPI) -> None:
    database = Database(DATABASE_URL, min_size=2, max_size=10)

    try:
        await database.connect()
        app.state._db = database
        logging.info("Database connected successfully")
    except Exception as e:
        logger.warning("Database connection error")
        logger.warning("Database URL:", DATABASE_URL)
        logger.warning("Error:", e)

async def close_db_connection(app: FastAPI) -> None:
    try:
        await app.state._db.disconnect()
        logging.info("Database disconnected successfully")

    except Exception as e:
        logger.warning("Database disconnection error")
        logger.warning("Error:", e)
