from fastapi import HTTPException, status


HTTP_400_BAD_REQUEST: HTTPException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Incorrect email or password")

HTTP_401_UNAUTHORIZED: HTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"})

HTTP_403_FORBIDDEN: HTTPException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Could not validate credentials")

HTTP_404_NOT_FOUND: HTTPException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found")