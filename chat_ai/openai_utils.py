import openai
from django.conf import settings

openai.api_key = "sk-None-TDzQy85Nh7X0741e9GijT3BlbkFJ85PmwNaXXGlx69xOCtUC"

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