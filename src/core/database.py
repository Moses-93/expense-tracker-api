from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker

from .config import DATABASE_URL

# Create a synchronous SQLite engine
engine = create_engine(DATABASE_URL)


# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Generator to return a session
def get_db():
    with SessionLocal() as session:
        yield session
