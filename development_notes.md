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
- Ran `gcloud auth application-default login` to authenticate google secret manager

# Google Notes
- Agent Builder allows you to easily add additional data to an LLM
  - Can build an LLM with access to your FHIR store on Agent Builder
  - Doesn't look like apps built with Agent Builder can be deployed via API
- Google AI Studio is a GUI to help with prompt engineering. Ex: can give it expected inputs and outputs and then it feeds those as examples into the model.
- VertexAI

# Summary
- Fine-Tuning: modify model weights based on a labeled data set
- RAG: provide additional information to the model before it replies. Need to search for the correct data
  - On Google, you can use their no-code tools to give it data, and then it does a semantic search for you
  - You'd need to do more of this on your own if you weren't using google's infrastructure