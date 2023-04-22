from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

url = "sqlite:///profile.db"
engine = create_engine(url)

Session = sessionmaker(autoflush=False, bind=engine)
