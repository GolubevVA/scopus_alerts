from internal.article_processing.gpt_lang_marker import GPTLangMarker
from internal.article_processing.prompt_builder import build_prompt

class LangRetriever:
    def __init__(self, title: str, prompt_type: str = "lang_retriever_v1"):
        self.title = title
        self.prompt_type = prompt_type
        try:
            self.client = GPTLangMarker()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Client: {e}")

    async def retrieve(self) -> list[str]:
        try:
            prompt = build_prompt(self.title, self.prompt_type)
        except Exception as e:
            raise RuntimeError(f"Failed to build prompt: {e}")

        try:
            result = await self.client.generate(prompt)
            return result["languages"]
        except Exception as e:
            raise RuntimeError(f"Failed to generate response from Client: {e}")
