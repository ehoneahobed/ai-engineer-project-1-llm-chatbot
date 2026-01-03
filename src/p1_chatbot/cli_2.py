"""
Before calling the API, ensure:
[ \text{estimated input tokens} + \text{RESERVED_OUTPUT_TOKENS} \le \text{EXERCISE_MAX_CONTEXT_TOKENS} ]

If the estimate is too large, truncate by repeatedly removing the oldest user+assistant pair:
remove messages at the start of the list
remove exactly 2 messages per truncation step: one user and one assistant
keep truncating until you are under the threshold
Every time you truncate, print:
[context] Truncated oldest messages to fit token budget.

Edge case rules
If the history is malformed (e.g., starts with an assistant message), truncate one message at a time until you get back to a sensible state.
Do not crash.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from .tokens import count_tokens

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
model_name = "gpt-4o-mini"

EXERCISE_MAX_CONTEXT_TOKENS = 4096
RESERVED_OUTPUT_TOKENS = 500
# TRUNCATE_THRESHOLD_TOKENS = 3500


def main():
    messages: list[dict[str, str]] = []
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "/quit"]:
            break
        if not user_input.strip():
            continue
        messages.append({"role": "user", "content": user_input})
        input_tokens_estimate = count_tokens(messages, model_name)
        # check if the input tokens are too large
        while input_tokens_estimate + RESERVED_OUTPUT_TOKENS >= EXERCISE_MAX_CONTEXT_TOKENS:
            # truncate the messages
            if len(messages) <= 2:
                break
            elif messages[0]["role"] == "system":
                messages = messages[1:]
            elif messages[0]["role"] != "user":
                messages = messages[1:]
            else:
                messages = messages[2:]
            print("[context] Truncated oldest messages to fit token budget.")
            input_tokens_estimate = count_tokens(messages, model_name)
        
        print(f"Tokens (estimated input): {input_tokens_estimate}")
        completion = client.chat.completions.create(
            model=model_name,
            messages=messages,
        )
        response = completion.choices[0].message.content
        print(response)
        messages.append({"role": "assistant", "content": response})
    
    print("Goodbye!")

if __name__ == "__main__":
    main()
