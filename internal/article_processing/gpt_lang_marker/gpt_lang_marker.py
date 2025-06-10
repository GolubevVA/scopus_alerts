import os
import asyncio
import json
from openai import AsyncOpenAI, OpenAIError

DEfAULT_MODEL = "gpt-4o-mini"

class GPTLangMarker:
    def __init__(self, api_key: str = None, model: str = DEfAULT_MODEL):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided either as an argument or in the OPENAI_API_KEY environment variable.")
        self.model = model
        self._create_client()

    def _create_client(self) -> None:
        self.client = AsyncOpenAI(api_key=self.api_key)

    async def generate(self, prompt: str, temperature: float = 0.1, max_tokens: int = 2048, max_retries: int = 3) -> dict:
        for attempt in range(max_retries):
            try:
                response = await self.client.chat.completions.create(
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
                content = response.choices[0].message.content.strip()
                return json.loads(content)
            except (OpenAIError, Exception) as e:
                self._create_client()
                if attempt == max_retries - 1:
                    raise RuntimeError(f"Failed after {max_retries} retries: {e}")
                await asyncio.sleep(2 ** attempt)
