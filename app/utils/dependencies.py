from fastapi import Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import JWTDecodeError
from ..repos.user_repos import UserRepository

user_repository = UserRepository()


def login_required(authorize: AuthJWT = Depends()):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        authorize.jwt_required()
        username = authorize.get_jwt_subject()
    except JWTDecodeError:
        raise credentials_exception

    try:
        user = user_repository._get_by_username(username)
        return user
    except Exception:
        raise credentials_exception


# RBAC: Role-Based Access Control dependencies
try:
    from typing import List  # noqa: E402
except Exception:
    List = list  # type: ignore


def require_role(role_name: str):
    """Factory that returns a dependency requiring a specific role."""

    def role_checker(Authorize: AuthJWT = Depends()):
        Authorize.jwt_required()
        user_roles = Authorize.get_raw_jwt().get("roles", [])
        if role_name not in user_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return True

    return role_checker


def require_admin():  # noqa: D401
    """Dependency that enforces ADMIN role."""
    return require_role("ADMIN")


def require_manager():  # noqa: D401
    """Dependency that enforces MANAGER role."""
    return require_role("MANAGER")


def require_sale():  # noqa: D401
    """Dependency that enforces SALE role."""
    return require_role("SALE")


def require_any_role(roles: List[str]):  # noqa: D401
    """Factory that returns a dependency allowing any of the provided roles."""

    def role_checker(Authorize: AuthJWT = Depends()):
        Authorize.jwt_required()
        user_roles = Authorize.get_raw_jwt().get("roles", [])
        if not any(r in user_roles for r in roles):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return True

    return role_checker


def get_current_user_with_roles(Authorize: AuthJWT = Depends()) -> dict:
    """Extract user and roles from the access token payload."""
    Authorize.jwt_required()
    payload = Authorize.get_raw_jwt()
    user_id = payload.get("user_id")
    roles = payload.get("roles", [])
    return {"user_id": user_id, "roles": roles}
