# main.py

from fastapi import Depends, FastAPI
from app.auth.auth_services import get_current_active_user
from app.routes import song_apis, user_apis
from app.auth import auth_apis

app = FastAPI(
    title="My API",
    description="API documentation",
    version="1.0",
    openapi_url="/api/openapi.json",  # This path includes the prefix
    docs_url="/api/docs",  # This path includes the prefix
)
app.include_router(
    auth_apis.api,
    tags=["auth"]
)
app.include_router(
    song_apis.api,
    tags=["songs"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(
    user_apis.api,
    tags=["users"],
    dependencies=[Depends(get_current_active_user)],
)
