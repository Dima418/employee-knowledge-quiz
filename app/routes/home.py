from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter(tags=["home"])

@router.get("/")
async def home():
    return HTMLResponse('<body><a href="/signin-google">Log In</a></body>')
