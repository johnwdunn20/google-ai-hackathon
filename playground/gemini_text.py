from dotenv import load_dotenv
import os

load_dotenv()


def get_res():
    test_key = os.getenv("TEST_KEY")
    if not test_key:
        raise ValueError("No API key found")
    


get_res()
