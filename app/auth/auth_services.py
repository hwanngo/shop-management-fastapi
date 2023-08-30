from fastapi import HTTPException

from .user_token import AccessToken


class AuthService():
    def __init__(self) -> None:
        pass

    def login(self, user, authorize):
        if user.username != "test" or user.password != "test":
            raise HTTPException(status_code=401, detail="Bad username or password")

        access_token = authorize.create_access_token(subject=user.username)
        refresh_token = authorize.create_refresh_token(subject=user.username)

        return AccessToken(access_token=access_token, refresh_token=refresh_token)

    def refresh(self, authorize):
        authorize.jwt_refresh_token_required()

        current_user = authorize.get_jwt_subject()
        new_access_token = authorize.create_access_token(subject=current_user)

        # authorize.set_access_cookies(new_access_token)
        return AccessToken(access_token=new_access_token)
