from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import cursor
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

url = "sqlite:///profile.db"
engine = create_engine(url)
inspector = inspect(engine)
# table_names = inspector.get_table_names()
# print(table_names)

Session = sessionmaker(autoflush=False, bind=engine)

@contextmanager
def new_session(**kwargs) -> Session:
    _session = Session(**kwargs)
    try:
        yield _session
    except Exception:
        _session.rollback()
        raise
    else:
        _session.commit()

@contextmanager
def new_cursor(session) -> cursor:
    cookies_connection = session.connection().connection
    cursor_instance: cursor = cookies_connection.cursor().__enter__()
    try:
        yield cursor_instance
    finally:
        cursor_instance.__exit__()
