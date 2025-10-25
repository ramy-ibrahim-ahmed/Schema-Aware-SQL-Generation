import google.generativeai as genai
from typing import Literal
from .providers import GeminiNLP


class NLPFactory:

    @staticmethod
    def create_nlp(provider: Literal["gemini", "openai"], api_key: str):
        if provider == "gemini":
            genai.configure(api_key=api_key)
            return GeminiNLP(gemini_client=genai)

        else:
            raise ValueError(f"Not available provider: {provider}")
