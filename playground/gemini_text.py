from dotenv import load_dotenv
import os

load_dotenv()

def get_res():
    API_KEY = os.getenv("GOOGLE_AI_STUDIO_API_KEY")
    if not API_KEY:
        raise ValueError("No API key found")
    

get_res()
