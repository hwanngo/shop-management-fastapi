from typing import List, Generator
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.services.order_services import OrderService
from app.schemas.order_schema import (
    OrderResponse,
    OrderDto,
    OrderCreate,
    OrderUpdate,
    OrderPatch,
)
from app.utils.dependencies import login_required

# Dependency: get a SQLAlchemy session
from app.database.database import OrmSession


def get_db_session() -> Generator[Session, None, None]:
    """
    Dependency that yields a SQLAlchemy Session.
    Copied pattern from song_apis.py for consistent DB access.
    """
    db: Session = OrmSession()
    try:
        yield db
    finally:
        db.close()


api = APIRouter()


@api.get(
    "/api/v1/orders", response_model=List[OrderResponse], status_code=status.HTTP_200_OK
)
def get_orders(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db_session),
    user: dict = Depends(login_required),
) -> List[OrderResponse]:
    """
    Retrieve all orders with pagination.
    - skip: number of records to skip
    - limit: maximum number of records to return
    """
    service = OrderService(db)
    try:
        orders = service.get_all_orders(skip=skip, limit=limit)
        return orders
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@api.get(
    "/api/v1/orders/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
def get_order_by_id(
    order_id: int,
    db: Session = Depends(get_db_session),
    user: dict = Depends(login_required),
) -> OrderResponse:
    """
    Get an order by its ID.
    """
    service = OrderService(db)
    order = service.get_order_by_id(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return order


@api.get(
    "/api/v1/orders/by-order-no/{order_no}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
def get_order_by_order_no(
    order_no: str,
    db: Session = Depends(get_db_session),
    user: dict = Depends(login_required),
) -> OrderResponse:
    """
    Get an order by its order number.
    """
    service = OrderService(db)
    order = service.get_order_by_order_no(order_no)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return order


@api.post(
    "/api/v1/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED
)
def create_order(
    order_in: OrderCreate,
    db: Session = Depends(get_db_session),
    user: dict = Depends(login_required),
) -> OrderResponse:
    """
    Create a new order (including order lines).
    """
    service = OrderService(db)
    try:
        created = service.create_order(order_in)
        return created
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@api.put(
    "/api/v1/orders/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
def update_order(
    order_id: int,
    order_in: OrderUpdate,
    db: Session = Depends(get_db_session),
    user: dict = Depends(login_required),
) -> OrderResponse:
    """
    Fully update an existing order.
    """
    service = OrderService(db)
    existing = service.get_order_by_id(order_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    try:
        updated = service.update_order(order_id, order_in)
        return updated
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@api.patch(
    "/api/v1/orders/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
def patch_order(
    order_id: int,
    order_in: OrderPatch,
    db: Session = Depends(get_db_session),
    user: dict = Depends(login_required),
) -> OrderResponse:
    """
    Partially update an existing order.
    """
    service = OrderService(db)
    existing = service.get_order_by_id(order_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    try:
        patched = service.patch_order(order_id, order_in)
        return patched
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@api.delete("/api/v1/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db_session),
    user: dict = Depends(login_required),
) -> None:
    """
    Delete an order by its ID.
    """
    service = OrderService(db)
    existing = service.get_order_by_id(order_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    try:
        service.delete_order(order_id)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@api.get(
    "/api/v1/orders/{order_id}/lines",
    response_model=OrderDto,
    status_code=status.HTTP_200_OK,
)
def get_order_with_lines(
    order_id: int,
    db: Session = Depends(get_db_session),
    user: dict = Depends(login_required),
) -> OrderDto:
    """
    Get an order with all its order lines (detailed totals included in DTO).
    """
    service = OrderService(db)
    order = service.get_order_with_lines(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return order


@api.get(
    "/api/v1/orders/search",
    response_model=List[OrderResponse],
    status_code=status.HTTP_200_OK,
)
def search_orders(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db_session),
    user: dict = Depends(login_required),
) -> List[OrderResponse]:
    """
    Search orders by a query string.
    """
    service = OrderService(db)
    try:
        results = service.search_orders(q)
        return results
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
