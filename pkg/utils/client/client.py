import os
from openai import OpenAI, OpenAIError

class Client:
    def __init__(self, api_key: str = None):
        self.model = "gpt-4o-mini"
        self.api_key = api_key or os.environ.get("OPENAPI_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided either as an argument or in the OPENAPI_KEY environment variable.")
        try:
            self.client = OpenAI(api_key=self.api_key)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize OpenAI client: {e}")

    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2048) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "strict": True,
                        "name": "LanguageDetection",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "languages": {
                                    "type": "array",
                                    "items": {"type": "string", "pattern": "^[a-z]{3}$"}
                                },
                                "reasoning": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                }
                            },
                            "required": ["languages", "reasoning"],
                            "additionalProperties": False
                        }
                    }
                },
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except OpenAIError as e:
            raise RuntimeError(f"OpenAI API error: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during generation: {e}")
