from fastapi import FastAPI, HTTPException, Depends
from functions.json_diff import compare_json
from functions.json_to_schema import json_to_schema
from database.connection import database
import pprint
import json
from typing import List, Dict, Any
from pydantic import BaseModel

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

@app.get("/")  # Defines a GET route for the root path "/"
async def root():
    return {
        "about": "Summary of the project",
        "additional_documentation": "Link to DevPost and/or Youtube video",
        "usage": "Visit /docs to see the API documentation and /openapi.json to see the OpenAPI schema",
    }


@app.get("/schemas/{use_case_id}")
async def get_schemas(use_case_id: int, db = Depends(connect_db)):
    try:
        query = 'SELECT data_schema FROM healthcare_data.schema_details where use_case_id = :use_case_id'
        results = await db.fetch_all(query=query, values={"use_case_id": use_case_id})
        if not results:
            raise HTTPException(status_code=404, detail='No schemas found for this use case id')
        for result in results:
            # pretty print result
            pprint.pprint(dict(result)['data_schema'])
            
        return [json.loads(result['data_schema']) for result in results]
    except Exception as e:
        print('Error: ', e)
        raise HTTPException(status_code=500, detail='Error fetching schemas')

# type for any json object
class JsonObj(BaseModel):
    class Config:
        extra = 'allow'
    
@app.post('/new_schema/{use_case_id}')
async def new_schema(use_case_id: int, json_obj: JsonObj, db = Depends(connect_db)):
    try:
        print('json_obj: ', json_obj)
        print('use_case_id: ', use_case_id)
        
        # convert to schema
        schema = json_to_schema(dict(json_obj))
        print('schema: ', schema)
        
        # check if schema already exists in db
        query_existing_schemas = 'SELECT data_schema FROM healthcare_data.schema_details where use_case_id = :use_case_id'
        existing_schemas = await db.fetch_all(query=query_existing_schemas, values={"use_case_id": use_case_id})
        # # **** Maybe I just have a unique constraint on the use_case_id column in the schema_details table? This probably works if I can make it unique per use case id****
        
        # query = 'INSERT INTO healthcare_data.schema_details (use_case_id, data_schema) VALUES (:use_case_id, :data_schema)'
        # await db.execute(query=query, values={"use_case_id": use_case_id, "data_schema": json.dumps(schema)})
        return 'Succesful test'
    except Exception as e:
        print('Error: ', e)
        raise HTTPException(status_code=500, detail='Error adding schema')