import os

# SQLAlchemy
DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = os.environ.get("DB_PORT", 3306)
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", 'root')
DB_NAME = os.environ.get("DB_NAME", 'fastapi')

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

JWT_SECRET_KEY = "tXbNLty1IeJhFgj7Lwzc4ZZozPXkew6B8RXNmtPIdQQY39GYPe9SRV6lG4LuLoQWD22ZpGxf6dxZLGGFaHQnmg"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
JWT_REFRESH_TOKEN_EXPIRE_MINUTES = 1440
