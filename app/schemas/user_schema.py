# schemas.py
from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str
    username: str
    password: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
