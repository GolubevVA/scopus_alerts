import os
import asyncio
import json
from openai import AsyncOpenAI, OpenAIError

DEfAULT_MODEL = "gpt-4o-mini"
'''Default OpenAI model used in the application.'''

class GPTLangMarker:
    '''
    Class for interacting with OpenAI's GPT model to detect languages in article titles.
    '''
    def __init__(self, api_key: str | None = None, model: str = DEfAULT_MODEL):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided either as an argument or in the OPENAI_API_KEY environment variable.")
        self.model = model
        self._create_client()

    def _create_client(self) -> None:
        self.client = AsyncOpenAI(api_key=self.api_key)

    async def generate(self, prompt: str, temperature: float = 0.1, max_tokens: int = 2048, max_retries: int = 3) -> dict:
        '''
        ## Args:
        - `prompt`: The prompt to send to the OpenAI model.
        - `temperature`: The temperature for the model's response (default is 0.1).
        - `max_tokens`: The maximum number of tokens to generate in the response (default is 2048).
        - `max_retries`: The maximum number of retries in case of failure (default is 3).
        ## Returns:
        - A dictionary containing the detected languages and reasoning.
        ## Raises:
        - `RuntimeError`: If the request fails after the maximum number of retries.

        Exponential backoff is used for retries. The client is reinitialized on each retry to handle potential connection issues.
        '''
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
                                    "reasoning": {
                                        "type": "string",
                                        "description": "The field you should use to think about the language detection."
                                    },
                                    "languages": {
                                        "type": "array",
                                        "items": {"type": "string", "pattern": "^[a-z]{3}$"},
                                        "description": "List of detected languages in ISO-639-3 format."
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
