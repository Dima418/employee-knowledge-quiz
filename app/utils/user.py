from datetime import datetime

from fastapi import Depends, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.security import reusable_oauth2
from app.crud.user import crud_user
from app.database.session import get_db
from app.database.models.user import User
from app.schemes.token import AccsessTokenData
from app.utils.token import decode_jwt


async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2)
) -> User:
    token_data: AccsessTokenData = await decode_jwt(token, AccsessTokenData)
    token_expired = datetime.utcfromtimestamp(token_data.exp) < datetime.utcnow()
    user = await crud_user.get_by_email(db, email=token_data.email)

    if not token_expired and user is not None:
        return user

    query = "?" + f"refresh_token={token_data.refresh_token}"
    return RedirectResponse("/refresh" + query, status_code=status.HTTP_303_SEE_OTHER)
