from fastapi import HTTPException, status


def HTTP_400_BAD_REQUEST(detail: str = "Bad request"):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail
    )

def HTTP_401_UNAUTHORIZED(detail: str = "Unauthorized", headers: dict = None):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers=headers or {"WWW-Authenticate": "Bearer"}
    )

def HTTP_403_FORBIDDEN(detail: str = "Forbidden"):
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail
    )

def HTTP_404_NOT_FOUND(detail: str = "Not found"):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail
    )
