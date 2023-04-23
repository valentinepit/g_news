from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


url = "sqlite:///./profile.db"
engine = create_engine(url)

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
