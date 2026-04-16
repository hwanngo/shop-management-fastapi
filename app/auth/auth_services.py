from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.database import OrmSession
from app.models.user import User
from app.repos.user_repos import UserRepository
from fastapi_jwt_auth import AuthJWT
from .user_token import AccessToken
from app.settings.configs import (
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES,
)


class AuthService:
    def __init__(self) -> None:
        pass

    # Internal helpers
    @staticmethod
    def _authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        user = UserRepository._get_by_username(db, username)
        if not user:
            return None
        if user.password != password:
            return None
        return user

    @staticmethod
    def _load_user_with_roles(db: Session, user_id: int) -> Optional[User]:
        return UserRepository.get_with_roles(db, user_id)

    def _roles_for_user(self, db: Session, user: User) -> List[str]:
        user_with_roles = self._load_user_with_roles(db, user.id)
        if not user_with_roles:
            return []
        return [r.role_name for r in getattr(user_with_roles, "roles", [])]

    def _token_claims(self, db: Session, user: User) -> dict:
        roles = self._roles_for_user(db, user)
        return {
            "user_id": user.id,
            "roles": roles,
            "issued_at": int(datetime.utcnow().timestamp()),
        }

    def _create_access_token(self, db: Session, user: User, authorize: AuthJWT) -> str:
        claims = self._token_claims(db, user)
        expires_delta = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        return authorize.create_access_token(
            subject=user.username,
            user_claims=claims,
            fresh=True,
            expires_delta=expires_delta,
        )

    def _create_refresh_token(self, db: Session, user: User, authorize: AuthJWT) -> str:
        claims = self._token_claims(db, user)
        expires_delta = timedelta(minutes=JWT_REFRESH_TOKEN_EXPIRE_MINUTES)
        return authorize.create_refresh_token(
            subject=user.username,
            user_claims=claims,
            expires_delta=expires_delta,
        )

    # Public API
    def authenticate_user(
        self, db: Session, username: str, password: str
    ) -> Optional[User]:
        return self._authenticate_user(db, username, password)

    def create_access_token(self, db: Session, user: User, authorize: AuthJWT) -> str:
        return self._create_access_token(db, user, authorize)

    def create_refresh_token(self, db: Session, user: User, authorize: AuthJWT) -> str:
        return self._create_refresh_token(db, user, authorize)

    def get_current_user_roles(self, authorize: AuthJWT) -> List[str]:
        roles: List[str] = []
        # Try to read roles from claims first
        try:
            claims = authorize.get_jwt_claims()
            if isinstance(claims, dict):
                roles = claims.get("roles", []) or []
        except Exception:
            pass
        if not roles:
            # Fallback to raw JWT payload if available
            get_raw = getattr(authorize, "get_raw_jwt", None)
            if callable(get_raw):
                raw = get_raw()
                if isinstance(raw, dict):
                    roles = raw.get("roles", []) or []
        return list(roles)

    def login(self, user, authorize: AuthJWT):
        # Open a DB session for authentication and token creation
        with OrmSession() as db:
            authenticated_user = self.authenticate_user(
                db, user.username, user.password
            )
            if not authenticated_user:
                raise HTTPException(status_code=401, detail="Bad username or password")

            access_token = self.create_access_token(db, authenticated_user, authorize)
            refresh_token = self.create_refresh_token(db, authenticated_user, authorize)

            return AccessToken(access_token=access_token, refresh_token=refresh_token)

    def refresh(self, authorize: AuthJWT):
        authorize.jwt_refresh_token_required()

        current_user = authorize.get_jwt_subject()
        # Re-create access token for the current user from DB
        with OrmSession() as db:
            user = UserRepository._get_by_username(db, current_user)
            if not user:
                raise HTTPException(status_code=401, detail="Invalid user")
            new_access_token = self.create_access_token(db, user, authorize)

        # authorize.set_access_cookies(new_access_token)
        return AccessToken(access_token=new_access_token)
