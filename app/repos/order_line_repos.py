from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.order_line import OrderLine
from app.schemas.order_line_schema import OrderLineCreate, OrderLineUpdate


class OrderLineRepository:
    """Repository for OrderLine entity operations."""

    @staticmethod
    def get_all_by_order_id(db: Session, order_id: int) -> List[OrderLine]:
        """Get all order lines for an order."""
        return db.query(OrderLine).filter(OrderLine.order_id == order_id).all()

    @staticmethod
    def get_by_id(db: Session, line_id: int) -> Optional[OrderLine]:
        """Get order line by ID."""
        return db.query(OrderLine).filter(OrderLine.id == line_id).first()

    @staticmethod
    def create(db: Session, order_id: int, line_data: OrderLineCreate) -> OrderLine:
        """Create new order line."""
        db_line = OrderLine(
            order_id=order_id,
            product=line_data.product,
            amount=line_data.amount,
            quantity=line_data.quantity,
        )
        db.add(db_line)
        db.commit()
        db.refresh(db_line)
        return db_line

    @staticmethod
    def update(
        db: Session, line_id: int, line_data: OrderLineUpdate
    ) -> Optional[OrderLine]:
        """Update order line."""
        db_line = db.query(OrderLine).filter(OrderLine.id == line_id).first()
        if not db_line:
            return None

        update_data = line_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_line, field, value)

        db.commit()
        db.refresh(db_line)
        return db_line

    @staticmethod
    def delete(db: Session, line_id: int) -> bool:
        """Delete order line."""
        db_line = db.query(OrderLine).filter(OrderLine.id == line_id).first()
        if not db_line:
            return False
        db.delete(db_line)
        db.commit()
        return True

    @staticmethod
    def delete_all_by_order_id(db: Session, order_id: int) -> int:
        """Delete all lines for an order. Returns count deleted."""
        result = db.query(OrderLine).filter(OrderLine.order_id == order_id).delete()
        db.commit()
        return result

    @staticmethod
    def bulk_create(
        db: Session, order_id: int, lines_data: List[OrderLineCreate]
    ) -> List[OrderLine]:
        """Create multiple order lines."""
        db_lines = []
        for line_data in lines_data:
            db_line = OrderLine(
                order_id=order_id,
                product=line_data.product,
                amount=line_data.amount,
                quantity=line_data.quantity,
            )
            db.add(db_line)
            db_lines.append(db_line)
        db.commit()
        for db_line in db_lines:
            db.refresh(db_line)
        return db_lines
