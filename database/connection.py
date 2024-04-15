# Use SQLAlchemy to create a connection pool to the database

from sqlalchemy import create_engine, MetaData
# databases package is used to perform async operations - useful because FastAPI is async
from databases import Database
import os
from dotenv import load_dotenv
import asyncio

# load environment variables
load_dotenv()

# get the database URL from the environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
print('DATABASE_URL: ', DATABASE_URL)

from urllib.parse import urlparse

parsed_url = urlparse(DATABASE_URL)
print("Scheme:", parsed_url.scheme)
print("Username:", parsed_url.username)
print("Password:", parsed_url.password)
print("Hostname:", parsed_url.hostname)
print("Port:", parsed_url.port)  # This should be an integer
print("Path:", parsed_url.path)


engine = create_engine(DATABASE_URL)
print('engine: ', engine)
metadata = MetaData()

# for async operations
database = Database(DATABASE_URL)

async def test_query():
    await database.connect()
    try:
        query = 'SELECT * FROM public.test_table '
        results = await database.fetch_all(query)
        for result in results:
            print(result)
            
    except Exception as e:
        print('Error: ', e)
        
    finally:
        await database.disconnect()

asyncio.run(test_query())