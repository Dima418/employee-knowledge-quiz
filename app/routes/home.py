from fastapi import APIRouter
from databases import Database

from app.core import config


router = APIRouter(tags=["home"])

@router.get("/")
async def home():
    return {"Hello": "World"}
