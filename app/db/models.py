from sqlalchemy import Column, Integer, String, DateTime, BINARY
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.functions import now

from app.db.db import engine


class Base(DeclarativeBase):
    pass


class Cookies(Base):
    __tablename__ = 'cookies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=now())
    cookie = Column(BINARY)
    last_update = Column(DateTime)
    counter = Column(Integer)


# Base.metadata.create_all(bind=engine)
