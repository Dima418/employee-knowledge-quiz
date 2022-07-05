from fastapi import APIRouter
from databases import Database

from app.core import config


router = APIRouter(tags=["home"])

@router.get("/")
async def home():
    return {"Hello": "World"}

@router.get("/connected")
async def home():
    database = Database(config.DATABASE_URL)
    try:
        await database.connect()
        return "Connected successfully"
    except Exception as e:
        return "Connection failed", e
