from google.cloud import secretmanager

# get the database URL from the secret manager
def get_secret(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    project_id = 'coral-silicon-420022'
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    
    response = client.access_secret_version(request={"name": secret_name})
    
    return response.payload.data.decode('UTF-8')