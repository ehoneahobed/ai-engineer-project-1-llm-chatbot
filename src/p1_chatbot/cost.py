"""
A script to estimate the cost of tokens used in a chatbot's conversation.
"""

MODEL_PRICING_USD_PER_1M = {
    "gpt-5.2": (1.75, 14.00),
    "gpt-5.1": (1.25, 10.00),
    "gpt-5": (1.25, 10.00),
    "gpt-5-mini": (0.25, 2.00),
    "gpt-5-nano": (0.05, 0.40),
    "gpt-4o-mini": (0.15, 0.60),
    "gpt-4o": (2.50, 10.00),
    "gpt-4o-2024-05-13": (50.00, 15.00),
}

def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    if model not in MODEL_PRICING_USD_PER_1M:
        raise ValueError(f"Model {model} not found in MODEL_PRICING_USD_PER_1M")
    input_price_per_1m, output_price_per_1m = MODEL_PRICING_USD_PER_1M[model]
    input_price = input_price_per_1m * (input_tokens / 1_000_000)
    output_price = output_price_per_1m * (output_tokens / 1_000_000)
    return input_price + output_price

if __name__ == "__main__":
    print(estimate_cost("gpt-4o-mini", 1_000_000, 1_000_000))
