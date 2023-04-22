from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase
from db import engine


class Base(DeclarativeBase):
    pass


class Cookies(Base):
    __tablename__ = 'cookies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime)
    cookie = Column(String)
    last_start_time = Column(DateTime)
    counter = Column(Integer)


# Base.metadata.create_all(bind=engine)
