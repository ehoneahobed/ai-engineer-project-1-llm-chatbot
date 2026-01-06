"""
Task specification
Implement a small “review classifier”:

labels: Positive or Negative
you must provide exactly 3 labeled examples in the prompt history
you then pass 1 new unlabeled review and print only the label
Use these exact examples:

I loved this movie. Great pacing and strong acting. → Positive
Not worth my time. The plot was confusing and boring. → Negative
Surprisingly good. I would watch it again. → Positive
Use this exact test review (the one you classify):

The cinematography was nice but the story felt flat and predictable.

Output requirement
Your script must print exactly one of:

Positive
Negative
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
model_name = "gpt-4o-mini"

def main():
    messages: list[dict[str, str]] = [
        {"role": "system", "content": "You are a helpful assistant that can classify movie reviews as positive or negative. "},
        {"role": "user", "content": "I loved this movie. Great pacing and strong acting."},
        {"role": "assistant", "content": "Positive"},
        {"role": "user", "content": "Not worth my time. The plot was confusing and boring."},
        {"role": "assistant", "content": "Negative"},
        {"role": "user", "content": "Surprisingly good. I would watch it again."},
        {"role": "assistant", "content": "Positive"},
        {"role": "user", "content": "The cinematography was nice but the story felt flat and predictable."},
    ]

    completion = client.chat.completions.create(
        model=model_name,
        messages=messages,
        # temperature=0.1,
    )
    response = completion.choices[0].message.content
    print(response)
    
if __name__ == "__main__":
    main()