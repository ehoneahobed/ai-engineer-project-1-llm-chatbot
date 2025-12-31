"""
This script should:

- load .env using python-dotenv
- call an LLM once (non-conversational is fine)
- send this exact prompt:
    Explain the difference between an AI Engineer and a Software Engineer in one sentence.

- print only the model’s text response to stdout (no JSON dumps)
- exit with status code 0 on success
"""
import os # for loading environment variables
import sys # for exiting the program
from dotenv import load_dotenv # load .env using python-dotenv
from openai import OpenAI # call an LLM once (non-conversational is fine)


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("ERROR: OPENAI_API_KEY is not set. Create a .env file from .env.example and add your key.")
    sys.exit(1)

client = OpenAI(api_key=api_key)
prompt = "Explain the difference between an AI Engineer and a Software Engineer in one sentence."

response = client.responses.create(
  model="gpt-4.1",
  input=prompt
)

print(response.output_text)