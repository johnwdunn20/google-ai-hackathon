# Set Up for my own libraries
1. Set up virtual environment with `virtualenv venv` and activate it `source venv/bin/activate`
  a. Note: Windows commands are slightly different
2. In the virtual environment shell, run `pip install -r requirements.txt`
3. To add newly installed libraries to requirements.txt, can fun `pip freeze > requirements.txt` after installation

# Server
1. To run the server: `uvicorn main:app --reload`
  a. Runs on port 8000 by default but can specify with `uvicorn main:app --reload --port 8000`
  b. http://localhost:8000/docs contains openapi (swagger)
  c. http://localhost:8000/redoc contains Redocs
  d. http://localhost:8000/openapi.json contains the openapi specification automatically created for you by fastapi based on your routes
  

# Notes
- Requirements.txt has too many libraries for production but is fine for now. Clean up unnecessary ones

# Deployment
- Run `gcloud app deploy`
- To view service, run `gcloud app browse`