from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel

if TYPE_CHECKING:
    from app.schemas.role_schema import RoleResponse


class UserBase(BaseModel):
    email: str
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserDto(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True


class UserResponse(UserBase):
    id: int
    create_date: datetime
    last_login: Optional[datetime] = None
    roles: List["RoleResponse"] = []

    class Config:
        orm_mode = True


class UserWithRoles(BaseModel):
    id: int
    email: str
    username: str
    password: str
    full_name: Optional[str] = None
    create_date: datetime
    last_login: Optional[datetime] = None
    roles: List["RoleResponse"] = []

    class Config:
        orm_mode = True


class UserInDB(BaseModel):
    id: int
    email: str
    username: str
    password: str
    full_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
