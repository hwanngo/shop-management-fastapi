from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel

if TYPE_CHECKING:
    from app.schemas.user_schema import UserDto


class RoleBase(BaseModel):
    role_name: str
    description: Optional[str] = None


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    role_name: Optional[str] = None
    description: Optional[str] = None


class RoleResponse(RoleBase):
    id: int
    create_date: datetime
    users: Optional[List["UserDto"]] = None

    class Config:
        orm_mode = True


class RoleInDB(BaseModel):
    id: int
    role_name: str
    description: Optional[str] = None
    create_date: datetime

    class Config:
        orm_mode = True
