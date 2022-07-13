"""Home (or root) routes.

"""
from fastapi import APIRouter


router = APIRouter(tags=["home"])

@router.get("/")
async def home():
    """Root route.

    Returns:
        dict[str: str]: Hello world message.
    """
    return {"Hello": "World"}
