from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base

if TYPE_CHECKING:
    from .order_line import OrderLine
    from .user import User


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_no: Mapped[str] = mapped_column(
        String(20), unique=True, index=True, nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), index=True, nullable=False
    )
    amount: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)
    order_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    status: Mapped[int] = mapped_column(Integer, default=0)
    customer: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    order_lines: Mapped[List["OrderLine"]] = relationship(
        "OrderLine", back_populates="order"
    )
    user: Mapped["User"] = relationship("User", back_populates="orders")
