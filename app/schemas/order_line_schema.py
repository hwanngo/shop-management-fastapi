from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class OrderLineBase(BaseModel):
    product: str
    amount: float
    quantity: int = 1


class OrderLineCreate(OrderLineBase):
    order_id: Optional[int] = None

    class Config:
        orm_mode = True


class OrderLineUpdate(BaseModel):
    product: Optional[str] = None
    amount: Optional[float] = None
    quantity: Optional[int] = None

    class Config:
        orm_mode = True


class OrderLineInDB(BaseModel):
    id: int
    order_id: int
    product: str
    amount: float
    quantity: int
    created_at: datetime

    class Config:
        orm_mode = True


class OrderDto(BaseModel):
    id: int
    status: Optional[str] = None
    total_amount: Optional[float] = None

    class Config:
        orm_mode = True


class OrderLineResponse(BaseModel):
    id: int
    order_id: int
    product: str
    amount: float
    quantity: int
    created_at: datetime
    order: Optional[OrderDto] = None

    class Config:
        orm_mode = True
