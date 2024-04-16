import os
import google.generativeai as genai
from functions.google_secret import get_secret


def get_res(prompt):
    API_KEY = get_secret("GOOGLE_AI_STUDIO_API_KEY")
    if not API_KEY:
        raise ValueError("No API key found")
    # configure gemini to use my api key
    genai.configure(api_key=API_KEY)

    # use gemini-pro for text only prompts
    model = genai.GenerativeModel('gemini-pro')
    
    # prompt the model
    response = model.generate_content(prompt)
    print('response from basic ai: ', response.text)
        
    return response.text
    

def main():
    get_res('What is the capital of France?')

if __name__ == "__main__":
    main()