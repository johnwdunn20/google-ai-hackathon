
# databases package is used to perform async operations - useful because FastAPI is async
from databases import Database
import os
# import asyncio
# import pprint
from google.cloud import secretmanager

# get the database URL from the environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
print('DATABASE_URL: ', DATABASE_URL)

# get the database URL from the secret manager
def get_secret(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    project_id = 'coral-silicon-420022'
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    
    response = client.access_secret_version(request={"name": secret_name})
    
    return response.payload.data.decode('UTF-8')

test_secret = get_secret('test_secret')
print('test_secret: ', test_secret)

# *** TO SEE THE PARSED QUERY STRING ***
# from urllib.parse import urlparse
# parsed_url = urlparse(DATABASE_URL)
# print("Scheme:", parsed_url.scheme)
# print("Username:", parsed_url.username)
# print("Password:", parsed_url.password)
# print("Hostname:", parsed_url.hostname)
# print("Port:", parsed_url.port)  # This should be an integer
# print("Path:", parsed_url.path)


# create a database object
database = Database(DATABASE_URL)
