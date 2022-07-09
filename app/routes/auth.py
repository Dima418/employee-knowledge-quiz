from authlib.integrations.starlette_client import OAuthError
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session

from app.core import config
from app.core.security import create_access_token, oauth
from app.crud.user import crud_user
from app.database.session import get_db
from app.schemes.token import Token
from app.schemes.user import UserBase, UserSignUp
from app.utils.HTTP_errors import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED


router = APIRouter(tags=["auth"])
jwt_auth_path = config.JWT_AUTH_PATH
google_auth_path = config.GOOGLE_AUTH_PATH
google_auth_url = config.GOOGLE_AUTH_URL

# JWT Auth

@router.post(jwt_auth_path, response_model=Token)
async def signin_jwt(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = await crud_user.authenticate(
        db,
        email=form_data.username,
        password=form_data.password
    )

    if user is None:
        raise HTTP_400_BAD_REQUEST

    user_data = {"sub": user.email}
    access_token = await create_access_token(user_data)

    return Token(access_token=access_token)

# Google Auth

@router.get("/signin-google")
async def signin_google(request: Request):
    redirect_uri = google_auth_url
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.route(google_auth_path)
async def auth_google(request: Request, db: Session = Depends(get_db)):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        raise HTTP_401_UNAUTHORIZED

    user_data = await oauth.google.parse_id_token(request, access_token)

    user = await crud_user.get_by_email(db, email=user_data["email"])

    # Save the user
    # request.session["user"] = dict(user)

    if user is None:
        raise HTTP_401_UNAUTHORIZED

    new_token = await create_access_token(user_data["email"])
    return JSONResponse({"result": True, "access_token": new_token})


@router.post("/signup", response_model=UserBase)
async def user_signup(*, user_in: UserSignUp, db: Session = Depends(get_db)) -> UserBase:
    user = await crud_user.get_by_email(db, email=user_in.email)
    if user is not None:
        raise HTTP_400_BAD_REQUEST

    user = await crud_user.create(db, obj_in=user_in)
    return user


@router.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/")
