from typing import List, Optional

from sqlalchemy.orm import Session

from app.repos.order_line_repos import OrderLineRepository
from app.schemas.order_line_schema import OrderLineCreate, OrderLineUpdate
from app.models.order_line import OrderLine


class OrderLineService:
    """Business logic for managing order lines.

    This service follows a simple, class-based pattern and delegates
    persistence operations to OrderLineRepository. It performs input
    validation and applies basic business rules as defined in the task.
    """

    @staticmethod
    def calculate_line_total(quantity: int, unit_price: float) -> float:
        """Compute the total price for a single line."""
        return float(quantity) * float(unit_price)

    @staticmethod
    def _extract_line_fields(line_data: OrderLineCreate) -> dict:
        """Safely extract common fields from a create/update payload.

        This helper tolerates both OrderLineCreate and OrderLineUpdate shapes
        since tests may pass either type depending on the call site.
        """
        return {
            "product": getattr(line_data, "product", None),
            "quantity": getattr(line_data, "quantity", None),
            "unit_price": getattr(line_data, "unit_price", None),
        }

    @staticmethod
    def validate_line_data(line_data: OrderLineCreate) -> None:
        """Validate order line data according to the business rules."""

        fields = OrderLineService._extract_line_fields(line_data)
        product = fields.get("product")
        quantity = fields.get("quantity")
        unit_price = fields.get("unit_price")

        if product is None or str(product).strip() == "":
            raise ValueError("Product cannot be empty")
        if quantity is None or int(quantity) <= 0:
            raise ValueError("Quantity must be greater than 0")
        if unit_price is None or float(unit_price) < 0:
            raise ValueError("Unit price must be non-negative")

    @staticmethod
    def get_lines_by_order_id(db: Session, order_id: int) -> List[OrderLine]:
        return OrderLineRepository.get_lines_by_order_id(db, order_id)

    @staticmethod
    def get_line_by_id(db: Session, line_id: int) -> Optional[OrderLine]:
        return OrderLineRepository.get_line_by_id(db, line_id)

    @staticmethod
    def create_line(
        db: Session, order_id: int, line_data: OrderLineCreate
    ) -> OrderLine:
        OrderLineService.validate_line_data(line_data)
        # Compute total for business rule (quantity * unit_price)
        line_total = OrderLineService.calculate_line_total(
            line_data.quantity, line_data.unit_price
        )
        created_line = OrderLineRepository.create_line(db, order_id, line_data)

        # Attach the computed total if the ORM object supports it (not guaranteed
        # to be persisted by the repository).
        if created_line is not None:
            if hasattr(created_line, "total"):
                setattr(created_line, "total", line_total)
            elif hasattr(created_line, "line_total"):
                setattr(created_line, "line_total", line_total)
        return created_line

    @staticmethod
    def update_line(
        db: Session, line_id: int, line_data: OrderLineUpdate
    ) -> Optional[OrderLine]:
        OrderLineService.validate_line_data(line_data)  # type: ignore[arg-type]
        updated_line = OrderLineRepository.update_line(db, line_id, line_data)  # type: ignore[arg-type]
        if updated_line is not None:
            line_total = OrderLineService.calculate_line_total(
                line_data.quantity, line_data.unit_price
            )  # type: ignore[arg-type]
            if hasattr(updated_line, "total"):
                setattr(updated_line, "total", line_total)  # type: ignore[assignment]
            elif hasattr(updated_line, "line_total"):
                setattr(updated_line, "line_total", line_total)  # type: ignore[assignment]
        return updated_line

    @staticmethod
    def delete_line(db: Session, line_id: int) -> None:
        return OrderLineRepository.delete_line(db, line_id)

    @staticmethod
    def delete_all_lines_by_order(db: Session, order_id: int) -> int:
        return OrderLineRepository.delete_all_lines_by_order(db, order_id)

    @staticmethod
    def bulk_create_lines(
        db: Session, order_id: int, lines_data: List[OrderLineCreate]
    ) -> List[OrderLine]:
        for line in lines_data:
            OrderLineService.validate_line_data(line)
        created_lines = OrderLineRepository.bulk_create_lines(db, order_id, lines_data)  # type: ignore[arg-type]

        # Attach computed totals where possible
        if isinstance(created_lines, list):
            for idx, line in enumerate(lines_data):
                if idx < len(created_lines):
                    created_line = created_lines[idx]
                    total = OrderLineService.calculate_line_total(
                        line.quantity, line.unit_price
                    )
                    if created_line is not None:
                        if hasattr(created_line, "total"):
                            setattr(created_line, "total", total)  # type: ignore[assignment]
                        elif hasattr(created_line, "line_total"):
                            setattr(created_line, "line_total", total)  # type: ignore[assignment]
        return created_lines
