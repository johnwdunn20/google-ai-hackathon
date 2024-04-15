# No longer using synchronous SQLAlchemy, instead using async databases package
# from sqlalchemy import create_engine, MetaData

# databases package is used to perform async operations - useful because FastAPI is async
from databases import Database
import os
from dotenv import load_dotenv
import asyncio
import pprint

# load environment variables
load_dotenv()

# get the database URL from the environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
print('DATABASE_URL: ', DATABASE_URL)

# from urllib.parse import urlparse

# parsed_url = urlparse(DATABASE_URL)
# print("Scheme:", parsed_url.scheme)
# print("Username:", parsed_url.username)
# print("Password:", parsed_url.password)
# print("Hostname:", parsed_url.hostname)
# print("Port:", parsed_url.port)  # This should be an integer
# print("Path:", parsed_url.path)


# for async operations
database = Database(DATABASE_URL)

async def test_query():
    await database.connect()
    try:
        query = 'SELECT * FROM public.test_table '
        results = await database.fetch_all(query)
        print('Results: ', results)
        for result in results:
            # pretty print the result. Need to convert it to a dictionary first
            pprint.pprint(dict(result))
            
    except Exception as e:
        print('Error: ', e)
        
    finally:
        await database.disconnect()

asyncio.run(test_query())