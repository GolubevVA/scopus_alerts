import pytest
import os
from dotenv import load_dotenv
from pkg.scopus import ScopusClient
import importlib
from tests.mocks import FakeDateTime
from internal.article_processing.gpt_lang_marker import GPTLangMarker
from internal.article_processing.prompt_builder import initialize_templates
from typing import AsyncGenerator

load_dotenv()

@pytest.fixture
def scopus_api_key() -> str:
    key = os.getenv("SCOPUS_API_KEY")
    if not key:
        pytest.skip("SCOPUS_API_KEY not set in environment")
    return key

@pytest.fixture
async def scopus_client(scopus_api_key: str) -> AsyncGenerator[ScopusClient, None]:
    client = ScopusClient(scopus_api_key)
    yield client
    await client.close()

@pytest.fixture()
def freeze_scheduler_time(monkeypatch: pytest.MonkeyPatch):
    """
    Make all datetime.now() calls in the scheduler module return a fixed time.
    """
    mod = importlib.import_module("internal.scheduler.scheduler.scheduler")
    monkeypatch.setattr(mod, "datetime", FakeDateTime)

@pytest.fixture
def openai_api_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        pytest.skip("OPENAI_API_KEY not set in environment")
    return key

@pytest.fixture
async def gpt_lang_marker(openai_api_key: str) -> AsyncGenerator[GPTLangMarker, None]:
    marker = GPTLangMarker(api_key=openai_api_key)
    yield marker

@pytest.fixture(scope="session", autouse=True)
def setup_templates():
    initialize_templates()
    yield
