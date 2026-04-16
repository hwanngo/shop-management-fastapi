from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.order import Order
from app.models.order_line import OrderLine
from app.models.user import User
from app.schemas.dashboard_schema import OrderStatistics, ProductSummary, DashboardTotal
from app.schemas.order_schema import OrderResponse


class DashboardService:
    """Service for dashboard reporting and statistics."""

    def __init__(self, db: Session):
        self.db = db

    def get_order_statistics(self) -> OrderStatistics:
        """Get order statistics including total orders and revenue."""
        total_orders = self.db.query(func.count(Order.id)).scalar() or 0
        total_revenue = self.db.query(func.sum(Order.amount)).scalar() or 0.0
        total_products = self.db.query(func.sum(OrderLine.quantity)).scalar() or 0

        return OrderStatistics(
            total_orders=total_orders,
            total_amount=float(total_revenue),
            total_products_sold=int(total_products),
        )

    def get_product_summary(self) -> List[ProductSummary]:
        """Get sales summary by product."""
        results = (
            self.db.query(
                OrderLine.product,
                func.sum(OrderLine.quantity).label("quantity"),
                func.sum(OrderLine.amount * OrderLine.quantity).label("revenue"),
            )
            .group_by(OrderLine.product)
            .all()
        )

        return [
            ProductSummary(
                product=row.product,
                quantity=row.quantity or 0,
                revenue=float(row.revenue) if row.revenue else 0.0,
            )
            for row in results
        ]

    def get_recent_orders(self, limit: int = 10) -> List[OrderResponse]:
        """Get recent orders for dashboard display."""
        orders = (
            self.db.query(Order).order_by(Order.created_at.desc()).limit(limit).all()
        )
        return [OrderResponse.from_orm(order) for order in orders]

    def get_top_selling_products(self, limit: int = 5) -> List[ProductSummary]:
        """Get top selling products by quantity sold."""
        results = (
            self.db.query(
                OrderLine.product,
                func.sum(OrderLine.quantity).label("quantity"),
                func.sum(OrderLine.amount * OrderLine.quantity).label("revenue"),
            )
            .group_by(OrderLine.product)
            .order_by(func.sum(OrderLine.quantity).desc())
            .limit(limit)
            .all()
        )

        return [
            ProductSummary(
                product=row.product,
                quantity=row.quantity or 0,
                revenue=float(row.revenue) if row.revenue else 0.0,
            )
            for row in results
        ]

    def get_dashboard_totals(self) -> DashboardTotal:
        """Get dashboard totals including orders count, products count, revenue, and users count."""
        orders_count = self.db.query(func.count(Order.id)).scalar() or 0
        products_count = (
            self.db.query(func.count(func.distinct(OrderLine.product))).scalar() or 0
        )
        revenue = self.db.query(func.sum(Order.amount)).scalar() or 0.0
        users_count = self.db.query(func.count(User.id)).scalar() or 0

        return DashboardTotal(
            orders_count=orders_count,
            products_count=products_count,
            revenue=float(revenue),
            users_count=users_count,
        )
