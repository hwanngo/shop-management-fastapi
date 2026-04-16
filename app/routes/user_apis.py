"""User routes with enhanced role management.

This module provides CRUD operations for users and new endpoints to manage
roles associated with users. All routes are protected by the login_required
dependency.
"""

from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List
from sqlalchemy.orm import Session

from app.repos.user_repos import UserRepository
from app.services.user_services import UserService
from app.schemas.user_schema import UserResponse, UserWithRoles, UserCreate
from app.utils.dependencies import login_required
from app.database.database import OrmSession

api = APIRouter()


def get_db_session():
    """Yield a new SQLAlchemy Session per request."""
    db_session = OrmSession()
    try:
        yield db_session
    finally:
        db_session.close()


@api.get("/api/v1/users", response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db_session), _=Depends(login_required)):
    """Get all users (basic info).

    Returns a list of UserResponse objects.
    """
    service = UserService(UserRepository())
    return service.retrieve_all_users(db)


@api.get("/api/v1/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int, db: Session = Depends(get_db_session), _=Depends(login_required)
):
    """Get a user by ID (basic info)."""
    service = UserService(UserRepository())
    user = service.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@api.post("/api/v1/users", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db_session),
    _=Depends(login_required),
):
    """Create a new user (basic info)."""
    service = UserService(UserRepository())
    user = service.create_user(db, user_data)
    return user


@api.put("/api/v1/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserCreate,
    db: Session = Depends(get_db_session),
    _=Depends(login_required),
):
    """Update an existing user by ID."""
    service = UserService(UserRepository())
    user = service.update_user(db, user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@api.delete("/api/v1/users/{user_id}")
async def delete_user(
    user_id: int, db: Session = Depends(get_db_session), _=Depends(login_required)
):
    """Delete a user by ID."""
    service = UserService(UserRepository())
    ok = service.delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}


@api.get("/api/v1/users/{user_id}/roles", response_model=UserWithRoles)
async def get_user_with_roles(
    user_id: int, db: Session = Depends(get_db_session), _=Depends(login_required)
):
    """Get a user along with their roles."""
    service = UserService(UserRepository())
    user = service.get_with_roles(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@api.post("/api/v1/users/{user_id}/roles", response_model=UserWithRoles)
async def assign_roles_to_user(
    user_id: int,
    role_ids: List[int] = Body(..., embed=True),
    db: Session = Depends(get_db_session),
    _=Depends(login_required),
):
    """Assign roles to a user by role IDs."""
    service = UserService(UserRepository())
    user = service.add_roles(db, user_id, role_ids)
    if not user:
        raise HTTPException(status_code=404, detail="User not found or roles invalid")
    return user


@api.delete("/api/v1/users/{user_id}/roles", response_model=UserWithRoles)
async def remove_roles_from_user(
    user_id: int,
    role_ids: List[int] = Body(..., embed=True),
    db: Session = Depends(get_db_session),
    _=Depends(login_required),
):
    """Remove roles from a user by role IDs."""
    service = UserService(UserRepository())
    user = service.remove_roles(db, user_id, role_ids)
    if not user:
        raise HTTPException(status_code=404, detail="User not found or roles invalid")
    return user


@api.get("/api/v1/users/by-role/{role_name}", response_model=List[UserResponse])
async def get_users_by_role(
    role_name: str, db: Session = Depends(get_db_session), _=Depends(login_required)
):
    """Get all users that have a specific role by role name."""
    service = UserService(UserRepository())
    users = service.get_by_role(db, role_name)
    return users
