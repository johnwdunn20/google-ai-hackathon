from fastapi import FastAPI
from src.json_diff import compare_json
from database.connection import database

from contextlib import asynccontextmanager
# This is a context manager that would allow us to connect to the db as soon as the server starts up. Can be implemented later if necessary

app = FastAPI()

@app.get("/schemas/{use_case_id}")
async def get_schemas(use_case_id: int):
    await database.connect()
    try:
        query = 'SELECT data_schema FROM healthcare_data.schema_details = :use_case_id'
        values = {'master_id': use_case_id}
        results = await database.fetch_all(query=query, values=values)
        return results
    except Exception as e:
        print('Error: ', e)
    finally:
        await database.disconnect()

# testing
# @app.get("/")  # Defines a GET route for the root path "/"
# async def root():
#     return {"message": "Hello World!"}

# @app.get("/items/{item_id}")
# async def get_items(item_id: int):
#     return {'item_id: ': item_id}