"""
Task specification
Use this exact math word problem:

A coffee shop sells cups for $3 each and muffins for $2 each. If you buy 4 cups and 5 muffins, how much do you spend in total?

Your script must run two model calls and print them as:



=== ZERO SHOT ===
<model response>

=== STEP BY STEP ===
<model response>
Rules:

“ZERO SHOT” call: ask the question as-is.
“STEP BY STEP” call: prepend a short instruction like: Explain your reasoning step-by-step, then give the final answer.

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
        # {"role": "system", "content": "You are a helpful assistant that can classify movie reviews as positive or negative. "},
        # {"role": "user", "content": "A coffee shop sells cups for $3 each and muffins for $2 each. If you buy 4 cups and 5 muffins, how much do you spend in total?"},
    ]

    for i in range(2):
        if i == 0:
            messages.append({"role": "user", "content": "A coffee shop sells cups for $3 each and muffins for $2 each. If you buy 4 cups and 5 muffins, how much do you spend in total?"})
        else:
            messages.append({"role": "user", "content": "A coffee shop sells cups for $3 each and muffins for $2 each. If you buy 4 cups and 5 muffins, how much do you spend in total? Explain your reasoning step-by-step, then give the final answer."})
        
        completion = client.chat.completions.create(
            model=model_name,
            messages=messages,
            # temperature=0.1,
        )
        response = completion.choices[0].message.content
        print("=== {} ===\n{}".format("ZERO SHOT" if i == 0 else "STEP BY STEP", response))
    
if __name__ == "__main__":
    main()