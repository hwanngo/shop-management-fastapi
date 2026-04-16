from typing import List, Generator
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.services.dashboard_services import DashboardService
from app.schemas.dashboard_schema import OrderStatistics, ProductSummary, DashboardTotal
from app.schemas.order_schema import OrderResponse
from app.utils.dependencies import login_required
from app.database.database import OrmSession


def get_db_session() -> Generator[Session, None, None]:
    """Dependency that yields a SQLAlchemy Session."""
    db: Session = OrmSession()
    try:
        yield db
    finally:
        db.close()


api = APIRouter()


@api.get(
    "/api/v1/dashboard/statistics",
    response_model=OrderStatistics,
    status_code=status.HTTP_200_OK,
)
def get_order_statistics(
    db: Session = Depends(get_db_session), user: dict = Depends(login_required)
) -> OrderStatistics:
    """Get order statistics including total orders and revenue."""
    service = DashboardService(db)
    try:
        stats = service.get_order_statistics()
        return stats
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@api.get(
    "/api/v1/dashboard/product-summary",
    response_model=List[ProductSummary],
    status_code=status.HTTP_200_OK,
)
def get_product_summary(
    db: Session = Depends(get_db_session), user: dict = Depends(login_required)
) -> List[ProductSummary]:
    """Get sales summary by product."""
    service = DashboardService(db)
    try:
        summary = service.get_product_summary()
        return summary
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@api.get(
    "/api/v1/dashboard/recent-orders",
    response_model=List[OrderResponse],
    status_code=status.HTTP_200_OK,
)
def get_recent_orders(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db_session),
    user: dict = Depends(login_required),
) -> List[OrderResponse]:
    """Get recent orders for dashboard display."""
    service = DashboardService(db)
    try:
        orders = service.get_recent_orders(limit=limit)
        return orders
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@api.get(
    "/api/v1/dashboard/top-products",
    response_model=List[ProductSummary],
    status_code=status.HTTP_200_OK,
)
def get_top_products(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db_session),
    user: dict = Depends(login_required),
) -> List[ProductSummary]:
    """Get top selling products by quantity sold."""
    service = DashboardService(db)
    try:
        products = service.get_top_selling_products(limit=limit)
        return products
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@api.get(
    "/api/v1/dashboard/totals",
    response_model=DashboardTotal,
    status_code=status.HTTP_200_OK,
)
def get_dashboard_totals(
    db: Session = Depends(get_db_session), user: dict = Depends(login_required)
) -> DashboardTotal:
    """Get dashboard totals including orders count, products count, revenue, and users count."""
    service = DashboardService(db)
    try:
        totals = service.get_dashboard_totals()
        return totals
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
