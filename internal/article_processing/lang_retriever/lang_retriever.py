from internal.article_processing.gpt_lang_marker import GPTLangMarker
from internal.article_processing.prompt_builder import build_prompt, LANG_RETRIEVER_V1_TEMPLATE_NAME

class LangRetriever:
    def __init__(self, api_key: str | None = None, prompt_type: str = LANG_RETRIEVER_V1_TEMPLATE_NAME, ):
        self.prompt_type = prompt_type
        try:
            self.client = GPTLangMarker(api_key=api_key)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Client: {e}")

    async def retrieve(self, title: str) -> list[str]:
        try:
            prompt = build_prompt(title, self.prompt_type)
        except Exception as e:
            raise RuntimeError(f"Failed to build prompt: {e}")

        try:
            result = await self.client.generate(prompt)
            return result["languages"]
        except Exception as e:
            raise RuntimeError(f"Failed to generate response from Client: {e}")
