from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///database.db"

# Create a synchronous SQLite engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Generator to return a session
def get_db():
    with SessionLocal() as session:
        yield session
