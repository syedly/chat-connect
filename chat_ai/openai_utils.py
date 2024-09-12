import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

def get_openai_response(prompt):
    if not prompt:
        raise ValueError("The prompt is empty.")
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=100  # Adjust as needed
    )
    return response['choices'][0]['message']['content']