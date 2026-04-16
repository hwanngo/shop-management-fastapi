from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Repos & Schemas
from app.repos.role_repos import RoleRepository
from app.schemas.role_schema import RoleResponse, RoleCreate, RoleUpdate
from app.utils.dependencies import login_required
from app.database.database import OrmSession
from app.models import role as role_model  # SQLAlchemy model for Role


def get_db_session():
    """Dependency: provide a SQLAlchemy session per request.

    Copied pattern from song_apis.py: create a new DB session, yield it,
    then close it after request completes.
    """
    db = OrmSession()
    try:
        yield db
    finally:
        db.close()


api = APIRouter()


def _to_role_orm(role_in: RoleCreate) -> role_model.Role:
    """Helper to convert API input into a Role ORM instance."""
    return role_model.Role(name=role_in.name)


@api.get(
    "/api/v1/roles",
    response_model=List[RoleResponse],
    status_code=status.HTTP_200_OK,
)
def get_all_roles_endpoint(
    db: Session = Depends(get_db_session),
    _login: None = Depends(login_required),
):
    """Fetch all roles."""
    repo = RoleRepository(db)
    roles = repo.get_all()
    return [RoleResponse.from_orm(r) for r in roles]


@api.get(
    "/api/v1/roles/{role_id}",
    response_model=RoleResponse,
    status_code=status.HTTP_200_OK,
)
def get_role_by_id_endpoint(
    role_id: int,
    db: Session = Depends(get_db_session),
    _login: None = Depends(login_required),
):
    """Fetch a role by its ID."""
    repo = RoleRepository(db)
    role = repo.get_by_id(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )
    return RoleResponse.from_orm(role)


@api.get(
    "/api/v1/roles/by-name/{role_name}",
    response_model=RoleResponse,
    status_code=status.HTTP_200_OK,
)
def get_role_by_name_endpoint(
    role_name: str,
    db: Session = Depends(get_db_session),
    _login: None = Depends(login_required),
):
    """Fetch a role by its unique name (e.g., ADMIN, MANAGER)."""
    repo = RoleRepository(db)
    role = repo.get_by_name(role_name)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )
    return RoleResponse.from_orm(role)


@api.post(
    "/api/v1/roles",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_role_endpoint(
    role_in: RoleCreate,
    db: Session = Depends(get_db_session),
    _login: None = Depends(login_required),
):
    """Create a new role. Ensures the role name is unique."""
    repo = RoleRepository(db)
    # Enforce uniqueness on role name
    if repo.get_by_name(role_in.name) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role with this name already exists",
        )
    new_role = _to_role_orm(role_in)
    created = repo.create(new_role)
    return RoleResponse.from_orm(created)


@api.put(
    "/api/v1/roles/{role_id}",
    response_model=RoleResponse,
    status_code=status.HTTP_200_OK,
)
def update_role_endpoint(
    role_id: int,
    role_in: RoleUpdate,
    db: Session = Depends(get_db_session),
    _login: None = Depends(login_required),
):
    """Update an existing role."""
    repo = RoleRepository(db)
    existing = repo.get_by_id(role_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )
    # Apply updates (only fields that are provided)
    if role_in.name is not None:
        existing.name = role_in.name
    db.commit()
    db.refresh(existing)
    return RoleResponse.from_orm(existing)


@api.delete(
    "/api/v1/roles/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_role_endpoint(
    role_id: int,
    db: Session = Depends(get_db_session),
    _login: None = Depends(login_required),
):
    """Delete a role by ID."""
    repo = RoleRepository(db)
    existing = repo.get_by_id(role_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )
    repo.delete(role_id)
    return None
