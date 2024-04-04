from dotenv import load_dotenv
import os
import pathlib
import textwrap
import google.generativeai as genai

load_dotenv()

def get_res():
    API_KEY = os.getenv("GOOGLE_AI_STUDIO_API_KEY")
    if not API_KEY:
        raise ValueError("No API key found")
    # configure gemini to use my api key
    genai.configure(api_key=API_KEY)
    
    # list out the available models:
    # for model in genai.list_models():
    #     if 'generateContent' in model.supported_generation_methods:
    #         print(f'{model.name}: {model.description}')
            
    # use gemini-pro for text only prompts
    model = genai.GenerativeModel('gemini-pro')
    
    # prompt the model
    response = model.generate_content('Give me some good, general advice.')
    # easier to convert to markdown in notebooks
    for key, val in response.items():
        print(f'{key.upper()}: {val}')
    

def main():
    get_res()

if __name__ == "__main__":
    main()