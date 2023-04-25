from sqlalchemy import BINARY, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Relationship
from sqlalchemy.sql.functions import now

from db import engine


class Base(DeclarativeBase):
    pass


class Profile(Base):
    __tablename__ = "profile"
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=now())
    last_update = Column(DateTime)
    counter = Column(Integer)
    cookie = Relationship("Cookies", backref="profile", lazy='dynamic')


class Cookies(Base):
    __tablename__ = 'cookies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cookie = Column(BINARY)
    domain = Column(String)
    profile_id = Column(Integer, ForeignKey("profile.id"))

