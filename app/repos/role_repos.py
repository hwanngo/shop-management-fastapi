from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.role import Role
from app.schemas.role_schema import RoleCreate, RoleUpdate


class RoleRepository:
    """Repository for Role entity operations."""

    @staticmethod
    def get_all(db: Session) -> List[Role]:
        """Get all roles."""
        return db.query(Role).all()

    @staticmethod
    def get_by_id(db: Session, role_id: int) -> Optional[Role]:
        """Get role by ID."""
        return db.query(Role).filter(Role.id == role_id).first()

    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[Role]:
        """Get role by name."""
        return db.query(Role).filter(Role.role_name == name).first()

    @staticmethod
    def get_by_names(db: Session, names: List[str]) -> List[Role]:
        """Get multiple roles by name list."""
        return db.query(Role).filter(Role.role_name.in_(names)).all()

    @staticmethod
    def create(db: Session, role_data: RoleCreate) -> Role:
        """Create new role."""
        db_role = Role(role_name=role_data.role_name, description=role_data.description)
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
        return db_role

    @staticmethod
    def update(db: Session, role_id: int, role_data: RoleUpdate) -> Optional[Role]:
        """Update role."""
        db_role = db.query(Role).filter(Role.id == role_id).first()
        if not db_role:
            return None

        update_data = role_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_role, field, value)

        db.commit()
        db.refresh(db_role)
        return db_role

    @staticmethod
    def delete(db: Session, role_id: int) -> bool:
        """Delete role."""
        db_role = db.query(Role).filter(Role.id == role_id).first()
        if not db_role:
            return False
        db.delete(db_role)
        db.commit()
        return True
