# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.settings.configs import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI)
OrmSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
