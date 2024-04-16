from fastapi import FastAPI, HTTPException, Depends
from functions.json_diff import json_diff
from functions.json_to_schema import json_to_schema
from database.connection import database
import pprint
import json
from typing import List, Dict, Any
from pydantic import BaseModel
from functions.google_secret import get_secret
from contextlib import asynccontextmanager
# This is a context manager that would allow us to connect to the db as soon as the server starts up. Can be implemented later if necessary

app = FastAPI(title='Improving Interoperability in Healthcare Data', version='0.1', description='This API is designed to improve interoperability in healthcare data by providing a way to map new data schemas to a master schema. It was built for the DevPost Google AI Hackathon. For a full description of the project, visit [DevPost](https://devpost.com/software/google-ai-hackathon-placeholder)')

# Each request depends on this (so will not use pooling)
async def connect_db():
    try:
        await database.connect()
        print('Connected to database')
        yield database
    finally:
        await database.disconnect()

@app.get("/", summary='Initial route', description='Test Description')  # Defines a GET route for the root path "/"
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

# route when you get new data    
@app.post('/new_data/{use_case_id}')
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

        # check if schema has already been mapped to the master schema. If it has, state that it has already been mapped
        for existing_schema in existing_schemas:
            comparison = json_diff(schema, json.loads(existing_schema['data_schema']))
            if not comparison:
                return {'message': 'Schema has already been mapped'}
            
        # if schema is new, get the comparison to the master schema so that it can be mapped
        query_master_schema = 'SELECT master_schema FROM healthcare_data.master_schema where id = :use_case_id'
        master_schema = await db.fetch_one(query=query_master_schema, values={"use_case_id": use_case_id})
        comparison_to_master = json_diff(schema, json.loads(master_schema['master_schema']))
        
        # add new schema to db
        
        # invoke gemeni to suggest a new master schema
            
        return {
            'message': 'Schema added',
            'comparison_to_master': comparison_to_master,
            'new_master_schema': '** fill in later **'
        }
    except Exception as e:
        print('Error: ', e)
        raise HTTPException(status_code=500, detail='Error adding schema')