"""
This script should:

Create the loop that continuously reads user input and exits cleanly.

Requirements
Your loop must:

prompt with exactly You: (note the trailing space)
exit when the user types any of: quit, exit, /quit (case-insensitive)
ignore empty input (if user hits Enter, reprompt without calling the API)
Acceptance checks
Typing quit exits without a traceback.
Typing an empty line does not call the LLM.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def main():
    messages: list[dict[str, str]] = []
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "/quit"]:
            break
        if not user_input.strip():
            continue
        messages.append({"role": "user", "content": user_input})
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        response = completion.choices[0].message.content
        print(response)
        messages.append({"role": "assistant", "content": response})
    
    print("Goodbye!")

if __name__ == "__main__":
    main()
