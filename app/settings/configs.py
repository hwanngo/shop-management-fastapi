import os
from ..utils.constants import JwtTokenExpires

# SQLAlchemy
DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = os.environ.get("DB_PORT", 3306)
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", 'root')
DB_NAME = os.environ.get("DB_NAME", 'fastapi')

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = JwtTokenExpires.ACCESS_TOKEN
JWT_REFRESH_TOKEN_EXPIRE_MINUTES = JwtTokenExpires.REFRESH_TOKEN
