from datetime import datetime
from .db import engine, new_session
from .models import Base, Profile


def create_db():
    Base.metadata.create_all(bind=engine)

    with new_session() as session:
        now = datetime.now()
        for _id in range(12):
            instance = Profile(created_at=now, counter=0)
            session.add(instance)
