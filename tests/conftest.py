import pytest
import os
from dotenv import load_dotenv
from pkg.scopus.client import ScopusClient

load_dotenv()

@pytest.fixture
def scopus_api_key():
    key = os.getenv("SCOPUS_API_KEY")
    if not key:
        pytest.skip("SCOPUS_API_KEY not set in environment")
    return key

@pytest.fixture
def scopus_client(scopus_api_key):
    return ScopusClient(scopus_api_key)
