from fastapi import FastAPI, HTTPException, Depends, Body
from functions.json_diff import json_diff
from functions.json_to_schema import json_to_schema
from database.connection import database
import pprint
import json
from typing import List, Dict, Any
from pydantic import BaseModel
from functions.google_secret import get_secret
from gemeni.basic_ai import get_res

app = FastAPI(
    title="Improving Interoperability in Healthcare Data",
    version="0.1",
    description="This API is designed to improve interoperability in healthcare data by providing a way to map new data schemas to a master schema. It was built for the DevPost Google AI Hackathon. For a full description of the project, visit [DevPost](https://devpost.com/software/google-ai-hackathon-placeholder)",
)


# Each request depends on this (so will not use pooling)
async def connect_db():
    try:
        await database.connect()
        print("Connected to database")
        yield database
    finally:
        await database.disconnect()


@app.get(
    "/", summary="Initial route", description="Test Description"
)  # Defines a GET route for the root path "/"
async def root():
    return {
        "about": "Summary of the project",
        "additional_documentation": "Link to DevPost and/or Youtube video",
        "usage": "Visit /docs to see the API documentation and /openapi.json to see the OpenAPI schema",
    }

# view all use cases
@app.get(
    "/use_cases",
    description="View all use cases",
)
async def view_use_cases(db=Depends(connect_db)):
    try:
        query = "SELECT * FROM healthcare_data.use_case"
        results = await db.fetch_all(query=query)
        if not results:
            raise HTTPException(
                status_code=404, detail="No use cases found"
            )
        print('Results type: ', type(results).__name__)
        for result in results:
            # pretty print result
            pprint.pprint(dict(result))
            print('Result type: ', type(result).__name__)
            print('Result Master Schema: ', type(result['master_schema']).__name__)
            print('Result to dict: ', dict(result))
            print('Master Schema to json load: ', json.loads(result['master_schema']))

        # dict converts results to a list of dictionaries

        return [{"id": result['id'], "description": result['description'], "master_schema": json.loads(result['master_schema'])} for result in results]
    except Exception as e:
        print("Error: ", e)
        raise HTTPException(status_code=500, detail="Error fetching use cases")

class Master_Schema(BaseModel):
    class Config:
        extra = "allow"


# create a new use case
@app.post(
    "/new_use_case",
    description="Create a new use case",
)
async def new_use_case(
    master_schema: Master_Schema = Body(
        ...,
        example={
            "visit": {"id": "int", "date": "date"},
            "patient": {"id": "int", "age": "int", "name": "text"},
        },
    ),
    db=Depends(connect_db),
):
    try:
        # add new use case to db
        insert_query = "INSERT INTO healthcare_data.use_case (master_schema) VALUES (:master_schema) RETURNING id"

        row_id = await db.execute(
            query=insert_query,
            values={
                "master_schema": json.dumps(dict(master_schema)),
            },
        )
        # Return success message and new rowId
        return {
            "message": "Use case added",
            "row_id": row_id,
            }
    except Exception as e:
        print("Error: ", e)
        raise HTTPException(status_code=500, detail="Error adding use case")

# get all schemas for a particular use case
@app.get(
    "/schemas/{use_case_id}",
    description="Get all schemas for a use case. Currently the only use case is '1'",
)
async def get_schemas(use_case_id: int, db=Depends(connect_db)):
    try:
        query = "SELECT data_schema FROM healthcare_data.schema_details where use_case_id = :use_case_id"
        results = await db.fetch_all(query=query, values={"use_case_id": use_case_id})
        if not results:
            raise HTTPException(
                status_code=404, detail="No schemas found for this use case id"
            )
        for result in results:
            # pretty print result
            pprint.pprint(dict(result)["data_schema"])

        return [json.loads(result["data_schema"]) for result in results]
    except Exception as e:
        print("Error: ", e)
        raise HTTPException(status_code=500, detail="Error fetching schemas")


class JsonObj(BaseModel):
    class Config:
        extra = "allow"


# route when you get new data
@app.post(
    "/new_data/{use_case_id}",
    description="Check if new data is compatable with the existing data schema. If it's not, the route will suggest a new schema. Currently, the only supported use case is '1'",
)
async def new_schema(
    use_case_id: int,
    json_obj: JsonObj = Body(
        ...,
        example={
            "visit": {"id": 501, "date": "2023-10-01"},
            "patient": {
                "id": 101,
                "age": 30,
                "height": "72",
                "name": "John Doe",
            },
        },
    ),
    db=Depends(connect_db),
):
    try:
        print("Json obj: ", json_obj)
        # convert to schema
        schema = json_to_schema(dict(json_obj))
        print("Schema: ", schema)

        if not schema:
            raise HTTPException(
                status_code=400, detail="Error converting JSON to schema"
            )

        # check if schema already exists in db
        query_existing_schemas = "SELECT data_schema FROM healthcare_data.schema_details where use_case_id = :use_case_id"
        existing_schemas = await db.fetch_all(
            query=query_existing_schemas, values={"use_case_id": use_case_id}
        )

        # check if schema has already been mapped to the master schema. If it has, state that it has already been mapped
        for existing_schema in existing_schemas:
            comparison = json_diff(schema, json.loads(existing_schema["data_schema"]))
            if not comparison:
                return {"message": "Schema has already been mapped"}

        # if schema is new, get the comparison to the master schema so that it can be mapped
        query_master_schema = (
            "SELECT master_schema FROM healthcare_data.use_case where id = :use_case_id"
        )
        master_schema = await db.fetch_one(
            query=query_master_schema, values={"use_case_id": use_case_id}
        )
        comparison_to_master = json_diff(
            json.loads(master_schema["master_schema"]), schema
        )

        # add new schema to db
        insert_query = "INSERT INTO healthcare_data.schema_details (use_case_id, data_schema, comparison_to_master_schema) VALUES (:use_case_id, :data_schema, :comparison_to_master)"

        await db.execute(
            query=insert_query,
            values={
                "use_case_id": use_case_id,
                "data_schema": json.dumps(schema),
                "comparison_to_master": str(comparison_to_master),
            },
        )

        # invoke gemeni to suggest a new master schema
        answer = get_res(master_schema["master_schema"], schema)

        # return suggested new master schema and relevant information
        return {
            "original_master_schema": json.loads(master_schema["master_schema"]),
            "new_schema": json.loads(json.dumps(schema)),
            "comparison_to_master_schema": str(
                comparison_to_master
            ),  # *** this should be formatted better, but need to turn "delete" from a symbol to a string
            "suggested_new_master_schema": json.loads(answer),
        }
    except Exception as e:
        print("Error: ", e)
        raise HTTPException(status_code=500, detail="Error adding schema")


