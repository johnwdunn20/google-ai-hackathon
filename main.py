from fastapi import FastAPI

app = FastAPI()

@app.get("/")  # Defines a GET route for the root path "/"
async def root():
    return {"message": "Hello World!"}

@app.get("/items/{item_id}")
async def get_items(item_id):
    return {'item_id: ': item_id}