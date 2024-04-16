
# databases package is used to perform async operations - useful because FastAPI is async
from databases import Database
import os
# import asyncio
# import pprint
from google.cloud import secretmanager
from functions.google_secret import get_secret

# get the database URL from the environment variables
# DATABASE_URL = os.getenv("DATABASE_URL")
# print('DATABASE_URL: ', DATABASE_URL)

# get secret from the secret manager
DATABASE_URL = get_secret('DATABASE_URL')
print('DATABASE_URL: ', DATABASE_URL)

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
