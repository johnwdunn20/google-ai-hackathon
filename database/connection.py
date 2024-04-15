# Use SQLAlchemy to create a connection pool to the database

from sqlalchemy import create_engine, MetaData
from databases import Database
import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# get the database URL from the environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
print('engine: ', engine)
metadata = MetaData()

# for async operations
database = Database(DATABASE_URL)

# def connect_to_db():
#     try:
#         # Create a connection pool to the database
#         POSTGRES_URL = os.getenv("POSTGRES_URL")
#         engine = create_engine(POSTGRES_URL, echo=True)
#         return engine
#     except Exception as e:
#         print('Error connecting to database: ', e)
#         return None