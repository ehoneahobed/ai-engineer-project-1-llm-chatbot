"""
After each model response, print:

prompt tokens
completion tokens
cost for the turn
total cost for the session so far

[usage] prompt_tokens=<N> completion_tokens=<M>
[cost]  turn_usd=<VALUE> total_usd=<VALUE>

Fallback rule
If completion.usage is None in your SDK/model combination, fall back to:

prompt token estimate from Day 3 (count_tokens(...))
completion tokens estimate by tokenizing the assistant text

"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from .tokens import count_tokens
from .prompts import SYSTEM_PROMPT
from .cost import estimate_cost

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
model_name = "gpt-4o-mini"

EXERCISE_MAX_CONTEXT_TOKENS = 4096
RESERVED_OUTPUT_TOKENS = 500
# TRUNCATE_THRESHOLD_TOKENS = 3500


def main():
    messages: list[dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    print("System prompt loaded. Type /quit to exit.")

    while True:
        user_input = input("You: ")
        total_cost = 0
        cot_mode = False
        if user_input.lower() in ["quit", "exit", "/quit"]:
            break
        if not user_input.strip():
            continue

        if user_input.lower() in ["/cot"]:
            """
            When CoT mode is enabled, modify the next user message content by prefixing:
            Explain your reasoning step-by-step, then give the final answer.\n\n
            The /cot command itself must NOT be sent to the LLM and must NOT be stored in messages.

            Print an on-screen confirmation:
            when enabled: [mode] CoT enabled for next turn.
            after the CoT turn is used: [mode] CoT disabled.
            """
            cot_mode = True
            print("[mode] CoT enabled for next turn.")
            user_input = input("You: ")
            user_input = "Explain your reasoning step-by-step, then give the final answer.\n\n" + user_input
            
            
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
            max_tokens=RESERVED_OUTPUT_TOKENS,
            temperature=0.1,
        )
        if completion.usage is None:
            prompt_tokens = count_tokens(messages, model_name)
            completion_tokens = count_tokens(completion.choices[0].message.content, model_name)
        else:
            prompt_tokens = completion.usage.prompt_tokens
            completion_tokens = completion.usage.completion_tokens
        turn_cost = estimate_cost(model_name, prompt_tokens, completion_tokens)
        total_cost += turn_cost

        response = completion.choices[0].message.content
        print(response)
        print(f"[usage] prompt_tokens={prompt_tokens} completion_tokens={completion_tokens}")
        print(f"[cost] turn_usd={turn_cost} total_usd={total_cost}")

        messages.append({"role": "assistant", "content": response})
        if cot_mode:
            print("[mode] CoT disabled.")
            cot_mode = False
    
    print("Goodbye!")

if __name__ == "__main__":
    main()
