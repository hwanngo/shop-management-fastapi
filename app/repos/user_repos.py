# user_repos.py

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from app.models.user import User
from app.models.role import Role
from app.schemas.user_schema import UserCreate

"""User repository with SQLAlchemy 2.0+ patterns.

This module provides both existing helpers (updated to 2.0 syntax) and
additional utilities to work with users and their associated roles.
"""


class UserRepository:
    def __init__(self) -> None:
        pass

    # Existing methods (updated to SQLAlchemy 2.0 patterns)
    @staticmethod
    def _retrieve_all_users(db: Session) -> List[User]:
        """Return all users using SQLAlchemy 2.0 style queries."""
        return db.query(User).all()

    @staticmethod
    def _get_by_username(db: Session, username: str) -> Optional[User]:
        """Return a user by username or None if not found."""
        return db.query(User).filter(User.username == username).first()

    # New enhanced methods
    @staticmethod
    def get_with_roles(db: Session, user_id: int) -> Optional[User]:
        """Get a user with roles eagerly loaded."""
        return (
            db.query(User)
            .options(joinedload(User.roles))
            .filter(User.id == user_id)
            .first()
        )

    @staticmethod
    def add_roles(db: Session, user_id: int, role_ids: List[int]) -> Optional[User]:
        """Assign roles to a user by role IDs."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        roles = db.query(Role).filter(Role.id.in_(role_ids)).all()
        for role in roles:
            if role not in user.roles:
                user.roles.append(role)

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def remove_roles(db: Session, user_id: int, role_ids: List[int]) -> Optional[User]:
        """Remove specified roles from a user."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        roles = {r.id: r for r in db.query(Role).filter(Role.id.in_(role_ids)).all()}
        # Remove found roles from the user's collection
        for role in list(user.roles):
            if role.id in roles:
                user.roles.remove(role)

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_by_role(db: Session, role_name: str) -> List[User]:
        """Return all users that have a given role name."""
        # Join through the association to filter by Role.role_name
        return (
            db.query(User)
            .join(User.roles)
            .join(Role)
            .filter(Role.role_name == role_name)
            .distinct()
            .all()
        )

    @staticmethod
    def update_last_login(db: Session, user_id: int) -> Optional[User]:
        """Update the last_login timestamp for a user to now."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        user.last_login = datetime.utcnow()
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def create_with_roles(
        db: Session, user_data: UserCreate, role_ids: List[int]
    ) -> User:
        """Create a new user and assign roles by IDs."""
        # Create user from provided data (password is required in UserCreate)
        new_user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            password=user_data.password,
        )
        db.add(new_user)
        db.flush()  # assign an ID for relationship population if needed

        # Attach roles if provided
        if role_ids:
            roles = db.query(Role).filter(Role.id.in_(role_ids)).all()
            for role in roles:
                new_user.roles.append(role)

        db.commit()
        db.refresh(new_user)
        return new_user
