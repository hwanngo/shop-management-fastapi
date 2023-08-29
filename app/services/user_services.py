# services.py

from sqlalchemy.orm import Session
from app.models import user

# TODO: Create, Update, Delete


# Retrieve
def retrieve_all_users(db: Session):
    return db.query(user.User).all()
