from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

from app.auth.user_token import User, Settings
from ..auth.auth_services import AuthService

api = APIRouter()
auth_service = AuthService()


@AuthJWT.load_config
def get_config():
    return Settings()


@api.post("/login")
def login(user: User, authorize: AuthJWT = Depends()):
    return auth_service.login(user, authorize)


@api.post("/refresh")
def refresh(authorize: AuthJWT = Depends()):
    return auth_service.refresh(authorize)


# @api.delete("/logout")
# def logout(Authorize: AuthJWT = Depends()):
#     """
#     Because the JWT are stored in an httponly cookie now, we cannot
#     log the user out by simply deleting the cookies in the frontend.
#     We need the backend to send us a response to delete the cookies.
#     """
#     Authorize.jwt_required()

#     Authorize.unset_jwt_cookies()
#     return {"msg": "Successfully logout"}


# @api.get("/protected")
# def protected(Authorize: AuthJWT = Depends()):
#     """
#     We do not need to make any changes to our protected endpoints. They
#     will all still function the exact same as they do when sending the
#     JWT in via a headers instead of a cookies
#     """
#     Authorize.jwt_required()

#     current_user = Authorize.get_jwt_subject()
#     return {"user": current_user}
