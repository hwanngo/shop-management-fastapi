from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from app.schemas.user_schema import UserResponse


class OrderLineCreate(BaseModel):
    product_id: int
    quantity: int = 1
    price: float = 0.0
    amount: float = 0.0

    class Config:
        orm_mode = True


class OrderLineResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: float
    amount: float
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    order_no: str
    user_id: int
    amount: float = 0.0
    status: int = 0
    customer: Optional[str] = None


class OrderCreate(OrderBase):
    order_lines: Optional[List[OrderLineCreate]] = None

    class Config:
        orm_mode = True


class OrderUpdate(BaseModel):
    order_no: Optional[str] = None
    amount: Optional[float] = None
    status: Optional[int] = None
    customer: Optional[str] = None

    class Config:
        orm_mode = True


class OrderPatch(OrderUpdate):
    pass


class OrderInDB(OrderBase):
    id: int
    order_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class OrderResponse(OrderInDB):
    order_lines: List[OrderLineResponse] = []
    user: Optional["UserResponse"] = None


class OrderDto(BaseModel):
    id: int
    order_no: str

    class Config:
        orm_mode = True
