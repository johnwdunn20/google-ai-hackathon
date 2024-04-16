import os
import google.generativeai as genai
from functions.google_secret import get_secret


def get_res(master_schema: str, new_schema: str, prompt: str = None):
    API_KEY = get_secret("GOOGLE_AI_STUDIO_API_KEY")
    if not API_KEY:
        raise ValueError("No API key found")
    # configure gemini to use my api key
    genai.configure(api_key=API_KEY)

    # use gemini-pro for text only prompts
    model = genai.GenerativeModel('gemini-pro')
    
    # prompt the model
    prompt = f''' Given the following master schema and new schema, suggest how to update the master schema to include the new schema. Do not reply with and text and only provide the updated master schema.
    
    # Master Schema
    {master_schema}
    
    # New Schema
    {new_schema}
    '''
    
    response = model.generate_content(prompt)
    # print('response from basic ai: ', response.text)
        
    return response.text
    

def main():
    get_res('What is the capital of France?')

if __name__ == "__main__":
    main()