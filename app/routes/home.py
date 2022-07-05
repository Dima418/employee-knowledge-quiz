from fastapi import APIRouter


router = APIRouter(tags=["home"])

@router.get("/")
async def home():
    return {"Hello": "World"}
