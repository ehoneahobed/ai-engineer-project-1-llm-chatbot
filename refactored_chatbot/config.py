"""
This module contains the configuration for the chatbot.

It is a singleton module that loads the configuration from a .env file.
"""

import os
from dotenv import load_dotenv
from dataclasses import dataclass


load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.1))
MAX_CONTEXT_TOKENS = int(os.getenv("MAX_CONTEXT_TOKENS", 4096))


@dataclass(frozen=True)
class Config:
    api_key: str = API_KEY
    model_name: str = MODEL_NAME
    temperature: float = TEMPERATURE
    max_context_tokens: int = MAX_CONTEXT_TOKENS

    def __post_init__(self):
        if not self.api_key:
            raise ValueError("API key not found in environment variables")
    
    def get_config(self) -> dict[str, str|float|int]:
        return {
            "api_key": self.api_key,
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_context_tokens": self.max_context_tokens
        }

config = Config()
