from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.order import Order
from app.models.order_line import OrderLine
from app.schemas.order_schema import OrderCreate, OrderUpdate, OrderPatch


class OrderRepository:
    """Repository for Order entity operations."""

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get all orders with pagination."""
        return db.query(Order).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, order_id: int) -> Optional[Order]:
        """Get order by ID."""
        return db.query(Order).filter(Order.id == order_id).first()

    @staticmethod
    def get_by_order_no(db: Session, order_no: str) -> Optional[Order]:
        """Get order by order number."""
        return db.query(Order).filter(Order.order_no == order_no).first()

    @staticmethod
    def create(db: Session, order_data: OrderCreate) -> Order:
        """Create new order."""
        db_order = Order(
            order_no=order_data.order_no,
            user_id=order_data.user_id,
            amount=order_data.amount,
            status=order_data.status,
            customer=order_data.customer,
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order

    @staticmethod
    def update(db: Session, order_id: int, order_data: OrderUpdate) -> Optional[Order]:
        """Update order."""
        db_order = db.query(Order).filter(Order.id == order_id).first()
        if not db_order:
            return None

        update_data = order_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_order, field, value)

        db.commit()
        db.refresh(db_order)
        return db_order

    @staticmethod
    def patch(db: Session, order_id: int, order_data: OrderPatch) -> Optional[Order]:
        """Partial update order."""
        db_order = db.query(Order).filter(Order.id == order_id).first()
        if not db_order:
            return None

        update_data = order_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_order, field, value)

        db.commit()
        db.refresh(db_order)
        return db_order

    @staticmethod
    def delete(db: Session, order_id: int) -> bool:
        """Delete order."""
        db_order = db.query(Order).filter(Order.id == order_id).first()
        if not db_order:
            return False
        db.delete(db_order)
        db.commit()
        return True

    @staticmethod
    def get_with_lines(db: Session, order_id: int) -> Optional[Order]:
        """Get order with order lines."""
        return (
            db.query(Order)
            .options(joinedload(Order.order_lines))
            .filter(Order.id == order_id)
            .first()
        )

    @staticmethod
    def search(db: Session, query: str) -> List[Order]:
        """Search orders by order number or customer."""
        return (
            db.query(Order)
            .filter(
                (Order.order_no.ilike(f"%{query}%"))
                | (Order.customer.ilike(f"%{query}%"))
            )
            .all()
        )

    @staticmethod
    def get_total_amount(db: Session, order_id: int) -> float:
        """Calculate total amount from order lines."""
        result = (
            db.query(OrderLine.order_id, OrderLine.amount * OrderLine.quantity)
            .filter(OrderLine.order_id == order_id)
            .all()
        )
        return sum(line[1] for line in result) if result else 0.0
