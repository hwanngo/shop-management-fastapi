# routes.py

from fastapi import APIRouter
from ..database.database import OrmSession
# from app.auth.auth_services import get_current_active_user

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

# TODO: HTTP POST, HTTP PUT and HTTP DELETE


# @api.get("/users/me", response_model=user_token.User)
# async def read_users_me(
#     current_user: Annotated[user_token.User, Depends(get_current_active_user)]
# ):
#     return current_user
