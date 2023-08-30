

from fastapi import Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import JWTDecodeError
from ..repos.user_repos import UserRepository

user_repository = UserRepository()


def login_required(authorize: AuthJWT = Depends()):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        authorize.jwt_required()
        username = authorize.get_jwt_subject()
    except JWTDecodeError:
        raise credentials_exception

    try:
        user = user_repository._get_by_username(username)
        return user
    except Exception:
        raise credentials_exception
