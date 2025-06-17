from internal.article_processing.gpt_lang_marker import GPTLangMarker
from internal.article_processing.prompt_builder import build_prompt, LANG_RETRIEVER_V1_TEMPLATE_NAME

class LangRetriever:
    '''
    Class for retrieving languages from an article's title using a language model.
    '''
    def __init__(self, api_key: str | None = None, prompt_type: str = LANG_RETRIEVER_V1_TEMPLATE_NAME, ):
        '''
        Initializes the LangRetriever with an OpenAI API key and prompt type.
        '''
        self.prompt_type = prompt_type
        try:
            self.client = GPTLangMarker(api_key=api_key)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Client: {e}")

    async def retrieve(self, title: str) -> list[str]:
        '''
        Retrieves languages from the article's title using the language model.
        '''
        try:
            prompt = build_prompt(title, self.prompt_type)
        except Exception as e:
            raise RuntimeError(f"Failed to build prompt: {e}")

        try:
            result = await self.client.generate(prompt)
            return result["languages"]
        except Exception as e:
            raise RuntimeError(f"Failed to generate response from Client: {e}")
