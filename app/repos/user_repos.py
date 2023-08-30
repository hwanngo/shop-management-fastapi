# user_repos.py

from sqlalchemy.orm import Session
from ..models.user import User

# TODO: Create, Update, Delete


class UserRepository():
    def __init__(self) -> None:
        pass

    def _retrieve_all_users(db: Session):
        return User.query.all()

    def _get_by_username(db: Session, username: str):
        if username != "test":
            return None
        else:
            return True
