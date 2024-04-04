from fastapi import FastAPI

app = FastAPI()

@app.get("/")  # Defines a GET route for the root path "/"
async def root():
    return {"message": "Hello World!"}
