from __future__ import annotations

from datetime import datetime
import random
import string
from typing import List, Optional, Any, Dict

from sqlalchemy.orm import Session

from app.repos.order_repos import OrderRepository
from app.repos.order_line_repos import OrderLineRepository
from app.schemas.order_schema import OrderCreate, OrderUpdate
from app.models.order import Order


class OrderService:
    """Order service encapsulating business logic for orders and order lines.

    This class coordinates between the OrderRepository and OrderLineRepository
    to perform common operations while enforcing business rules (e.g., total
    calculation, validation, and generated order numbers).
    """

    def __init__(
        self,
        order_repo: Optional[OrderRepository] = None,
        order_line_repo: Optional[OrderLineRepository] = None,
    ) -> None:
        self.order_repo = order_repo or OrderRepository()
        self.order_line_repo = order_line_repo or OrderLineRepository()

    # --------------------------- Helper utilities ---------------------------
    def generate_order_no(self, db: Session) -> str:
        """Generate a unique, human-readable order number."""
        # Simple yet reasonably unique token: timestamp + random suffix
        random_suffix = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return f"ORD-{timestamp}-{random_suffix}"

    def calculate_order_total(self, db: Session, order_id: int) -> float:
        """Sum (quantity * unit_price) for all order lines of an order."""
        lines = self.order_line_repo.get_by_order_id(db, order_id)
        total = 0.0
        for line in lines:
            qty = getattr(line, "quantity", 0) or 0
            price = getattr(line, "unit_price", 0.0) or 0.0
            total += float(qty) * float(price)
        return total

    # --------------------------------- API ---------------------------------
    def get_all_orders(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        return self.order_repo.get_all(db, skip=skip, limit=limit)

    def get_order_by_id(self, db: Session, order_id: int) -> Order:
        order = self.order_repo.get_by_id(db, order_id)
        if order is None:
            raise ValueError(f"Order with id={order_id} not found.")
        return order

    def get_order_by_order_no(self, db: Session, order_no: str) -> Order:
        order = self.order_repo.get_by_order_no(db, order_no)
        if order is None:
            raise ValueError(f"Order with order_no={order_no} not found.")
        return order

    def get_order_with_lines(self, db: Session, order_id: int) -> Dict[str, Any]:
        order = self.order_repo.get_by_id(db, order_id)
        if order is None:
            raise ValueError(f"Order with id={order_id} not found.")
        lines = self.order_line_repo.get_by_order_id(db, order_id)
        return {"order": order, "lines": lines}

    def create_order(self, db: Session, order_data: OrderCreate, user_id: int) -> Order:
        # Validation: ensure there is at least one line
        lines = (
            getattr(order_data, "order_lines", None)
            or getattr(order_data, "lines", None)
            or []
        )
        if not lines:
            raise ValueError("An order must contain at least one order line.")

        # Generate order_no if not provided
        order_no = getattr(order_data, "order_no", None)
        if not order_no:
            order_no = self.generate_order_no(db)

        created_date = datetime.utcnow()

        # Build payload for Order (excluding lines)
        if hasattr(order_data, "dict"):
            payload: Dict[str, Any] = order_data.dict()
            payload.pop("order_lines", None)
            payload.pop("lines", None)
        else:
            payload = dict(order_data) if isinstance(order_data, dict) else {}

        payload.update(
            {
                "order_no": order_no,
                "created_date": created_date,
                "user_id": user_id,
            }
        )

        new_order = self.order_repo.create(db, obj_in=payload)

        # Persist order lines
        line_dicts: List[Dict[str, Any]] = []
        for l in lines:
            if hasattr(l, "dict"):
                line_dicts.append(l.dict())
            elif isinstance(l, dict):
                line_dicts.append(l)
            else:
                # Fallback: try to cast to dict if possible
                line_dicts.append(dict(l))

        self.order_line_repo.create_lines(db, order_id=new_order.id, lines=line_dicts)

        # Calculate and persist total_amount
        total = self.calculate_order_total(db, new_order.id)
        self.order_repo.update(db, db_obj=new_order, obj_in={"total_amount": total})

        return new_order

    def update_order(
        self, db: Session, order_id: int, order_data: OrderUpdate
    ) -> Order:
        existing = self.order_repo.get_by_id(db, order_id)
        if existing is None:
            raise ValueError(f"Order with id={order_id} not found.")

        if hasattr(order_data, "dict"):
            update_payload: Dict[str, Any] = order_data.dict()
        else:
            update_payload = dict(order_data) if isinstance(order_data, dict) else {}

        updated = self.order_repo.update(db, db_obj=existing, obj_in=update_payload)

        # Recalculate total_amount if relevant fields changed
        total = self.calculate_order_total(db, order_id)
        updated = self.order_repo.update(
            db, db_obj=updated, obj_in={"total_amount": total}
        )
        return updated

    def delete_order(self, db: Session, order_id: int) -> None:
        # Cascade delete lines first
        self.order_line_repo.delete_by_order_id(db, order_id)
        self.order_repo.delete(db, order_id)

    def search_orders(self, db: Session, query: str) -> List[Order]:
        return self.order_repo.search(db, query)
