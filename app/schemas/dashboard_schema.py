from pydantic import BaseModel


class ProductSummary(BaseModel):
    product: str
    quantity: int
    total_amount: float

    class Config:
        orm_mode = True


class DashboardTotal(BaseModel):
    total_orders: int
    total_amount: float
    total_items: int

    class Config:
        orm_mode = True


class OrderStatistics(BaseModel):
    pending_count: int
    confirmed_count: int
    shipped_count: int
    delivered_count: int
    cancelled_count: int
    total_count: int

    class Config:
        orm_mode = True
