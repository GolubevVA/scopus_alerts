import pytest
import os
from dotenv import load_dotenv
from pkg.scopus import ScopusClient
from internal.article_processing.gpt_lang_marker import GPTLangMarker
from internal.article_processing.lang_retriever import LangRetriever
from internal.article_processing.prompt_builder import initialize_templates

load_dotenv()

@pytest.fixture
def scopus_api_key() -> str:
    key = os.getenv("SCOPUS_API_KEY")
    if not key:
        pytest.skip("SCOPUS_API_KEY not set in environment")
    return key

@pytest.fixture
async def scopus_client(scopus_api_key: str) -> ScopusClient:
    client = ScopusClient(scopus_api_key)
    yield client
    await client.close()

@pytest.fixture
def openai_api_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        pytest.skip("OPENAI_API_KEY not set in environment")
    return key

@pytest.fixture
async def gpt_lang_marker(openai_api_key: str) -> GPTLangMarker:
    marker = GPTLangMarker(api_key=openai_api_key)
    yield marker

@pytest.fixture(scope="session", autouse=True)
def setup_templates():
    from internal.article_processing.prompt_builder import initialize_templates
    initialize_templates()
    yield

