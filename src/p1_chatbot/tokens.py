"""
This function counts the number of tokens in a list of messages.
"""
import tiktoken

def count_tokens(messages: list[dict[str, str]], model: str) -> int:
    """Count the number of tokens in a list of messages."""
    number_of_tokens = 0
    try:
        encoding = tiktoken.encoding_for_model(model)
    except ValueError:
        encoding = tiktoken.get_encoding("cl100k_base")

    for message in messages:
        number_of_tokens += 4 # accounts for <im_start> and <im_end>
        for key, value in message.items():
            number_of_tokens += len(encoding.encode(value))
    return number_of_tokens

