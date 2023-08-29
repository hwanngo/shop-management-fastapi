# routes.py

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm
from app.settings.configs import ACCESS_TOKEN_EXPIRE_MINUTES
from app.auth.auth_services import authenticate_user, create_access_token
from app.database.database import OrmSession
from app.auth import user_token

api = APIRouter()


# We need to have an independent database session/connection per request, use
# the same session through all the request and then close it after the request
# is finished.
# And then a new session will be created for the next request.
# Our dependency will create a new SQLAlchemy Session that will be used in a
# single request, and then close it once the request is finished.
# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-dependency
def get_db_session():
    db_session = OrmSession()
    try:
        yield db_session
    finally:
        db_session.close()


fake_users_db = {
    "admin": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "hashed_password": "$2a$12$kvB4IR6lCN9Rz2AjLB1V0uyjz8jXtwMdxOfjcX04OfnvV.nLJpoAu",
        "created_at": "1",
        "updated_at": "1"
    }
}

# TODO: HTTP POST, HTTP PUT and HTTP DELETE


# HTTP GET
@api.post("/auth", response_model=user_token.Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
