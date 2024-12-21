from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Connection string for Azure SQL Database (ODBC Driver 18)
DATABASE_URL = os.environ["DATABASE_URL"]

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL, connect_args={"driver": "ODBC Driver 18 for SQL Server"}
)

# SessionLocal for managing database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
