# Use SQLAlchemy to create a connection pool to the database

from sqlalchemy import create_engine
import os

def connect_to_db():
    try:
        # Create a connection pool to the database
        POSTGRES_URL = os.getenv("POSTGRES_URL")
        engine = create_engine(POSTGRES_URL, echo=True)
        return engine
    except Exception as e:
        print('Error connecting to database: ', e)
        return None