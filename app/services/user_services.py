# services.py

from typing import List, Optional
from sqlalchemy.orm import Session

from ..repos.user_repos import UserRepository
from app.models.user import User
from app.schemas.user_schema import UserCreate

"""User service providing business-logic operations for user management.

This service delegates to the repository for data access and contains
lightweight orchestration suitable for the API layer.
"""


class UserService:
    def __init__(self, repository: UserRepository = None) -> None:
        self.repository = repository or UserRepository()

    # Basic user operations
    def retrieve_all_users(self, db: Session) -> List[User]:
        return self.repository._retrieve_all_users(db)

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return self.repository._get_by_username(db, username)

    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    def create_user(self, db: Session, user_data: UserCreate) -> User:
        # Create a new user without roles by default; roles can be attached via dedicated endpoints
        new_user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            password=user_data.password,
        )
        db.add(new_user)
        db.flush()
        db.commit()
        db.refresh(new_user)
        return new_user

    def update_user(
        self, db: Session, user_id: int, user_data: UserCreate
    ) -> Optional[User]:
        user = self.get_by_id(db, user_id)
        if not user:
            return None
        user.email = user_data.email
        user.username = user_data.username
        user.full_name = user_data.full_name
        user.password = user_data.password
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def delete_user(self, db: Session, user_id: int) -> bool:
        user = self.get_by_id(db, user_id)
        if not user:
            return False
        db.delete(user)
        db.commit()
        return True

    # Role-related operations
    def get_with_roles(self, db: Session, user_id: int):
        return self.repository.get_with_roles(db, user_id)

    def add_roles(self, db: Session, user_id: int, role_ids: List[int]):
        return self.repository.add_roles(db, user_id, role_ids)

    def remove_roles(self, db: Session, user_id: int, role_ids: List[int]):
        return self.repository.remove_roles(db, user_id, role_ids)

    def get_by_role(self, db: Session, role_name: str):
        return self.repository.get_by_role(db, role_name)

    def create_with_roles(
        self, db: Session, user_data: UserCreate, role_ids: List[int]
    ):
        return self.repository.create_with_roles(db, user_data, role_ids)
