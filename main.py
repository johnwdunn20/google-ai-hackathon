from fastapi import FastAPI, HTTPException, Depends
from src.json_diff import compare_json
from database.connection import database

from contextlib import asynccontextmanager
# This is a context manager that would allow us to connect to the db as soon as the server starts up. Can be implemented later if necessary

app = FastAPI()

# Each request depends on this (so will not use pooling)
async def connect_db():
    try:
        await database.connect()
        print('Connected to database')
        yield database
    finally:
        await database.disconnect()

@app.get("/schemas/{use_case_id}")
async def get_schemas(use_case_id: int, db = Depends(connect_db)):
    try:
        query = 'SELECT data_schema FROM healthcare_data.schema_details where use_case_id = :use_case_id'
        results = await db.fetch_all(query=query, values={"use_case_id": use_case_id})
        if not results:
            raise HTTPException(status_code=404, detail='No schemas found for this use case id')
        return results
    except Exception as e:
        print('Error: ', e)
        raise HTTPException(status_code=500, detail='Error fetching schemas')

# testing
@app.get("/")  # Defines a GET route for the root path "/"
async def root():
    return {"message": "Hello World!"}

# @app.get("/items/{item_id}")
# async def get_items(item_id: int):
#     return {'item_id: ': item_id}