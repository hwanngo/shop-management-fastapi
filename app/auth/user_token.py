from pydantic import BaseModel
from datetime import timedelta

from ..settings.configs import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRE_MINUTES, JWT_REFRESH_TOKEN_EXPIRE_MINUTES


class AccessToken(BaseModel):
    access_token: str
    refresh_token: str = ""


class User(BaseModel):
    username: str
    password: str


class Settings(BaseModel):
    authjwt_secret_key: str = JWT_SECRET_KEY
    access_expires: int = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expires: int = timedelta(days=JWT_REFRESH_TOKEN_EXPIRE_MINUTES)
    # authjwt_denylist_enabled: bool = True
    # authjwt_denylist_token_checks: set = {"access", "refresh"}
