import pytest
import os
from dotenv import load_dotenv
from pkg.scopus import ScopusClient
import importlib
from tests.mocks import FakeDateTime

load_dotenv()

@pytest.fixture
def scopus_api_key():
    key = os.getenv("SCOPUS_API_KEY")
    if not key:
        pytest.skip("SCOPUS_API_KEY not set in environment")
    return key

@pytest.fixture
async def scopus_client(scopus_api_key: str):
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
    yield
