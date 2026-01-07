"""
Create a deterministic cost estimator.

Files to create
Create src/p1_chatbot/cost.py with:

a MODEL_PRICING_USD_PER_1M: dict[str, tuple[float, float]] mapping model → (input_per_1m, output_per_1m)
def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
docstrings and type hints
Rules:

estimate_cost returns a float USD value (e.g., 0.000123)
if the model is not in the dict, raise a ValueError with a clear message
"""

MODEL_PRICING_USD_PER_1M = {
    "gpt-4o-mini": (0.15, 0.60),
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
