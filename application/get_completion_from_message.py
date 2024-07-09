from openai import OpenAI
import os
api_key_file_path = 'openai_api_key.txt'

# Read the API key from the file
with open(api_key_file_path, 'r') as file:
    api_key = file.read().strip()

# Set the API key for OpenAI
os.environ['OPENAI_API_KEY'] = api_key
client = OpenAI()

def GetCompletionFromMessages (messages,
                                 model="gpt-3.5-turbo-1106",
                                 temperature=0.5, max_tokens=500):
    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=temperature,
    max_tokens=max_tokens)
    return response.choices[0].message.content