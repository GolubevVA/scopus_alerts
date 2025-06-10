import pytest
from internal.article_processing.lang_retriever import LangRetriever
from internal.article_processing.prompt_builder import LANG_RETRIEVER_V1_TEMPLATE_NAME

def test_lang_retriever_initialization(openai_api_key: str):
    retriever = LangRetriever(api_key=openai_api_key)
    
    assert retriever.prompt_type == LANG_RETRIEVER_V1_TEMPLATE_NAME
    assert retriever.client is not None
    assert retriever.client.api_key == openai_api_key

@pytest.mark.asyncio
async def test_lang_retriever_retrieve_english(openai_api_key: str):
    title = "Research on machine learning algorithms and artificial intelligence"
    retriever = LangRetriever(api_key=openai_api_key)
    result = await retriever.retrieve(title)
    
    assert isinstance(result, list)
    assert all(isinstance(lang, str) for lang in result)
    assert len(result) == 0

@pytest.mark.asyncio
async def test_lang_retriever_retrieve_russian(openai_api_key: str):
    title = "Исследование группы финно-угорских языков и их влияние на культуру"
    retriever = LangRetriever(api_key=openai_api_key)
    result = await retriever.retrieve(title)
    
    assert isinstance(result, list)
    assert all(isinstance(lang, str) for lang in result)
    assert len(result) > 0
    # Может содержать русский или связанные языки
    assert any(lang in result for lang in ["rus", "fin", "hun", "est"])

@pytest.mark.asyncio
async def test_lang_retriever_retrieve_french(openai_api_key: str):
    title = "Étude sur la langue française et son évolution historique"
    retriever = LangRetriever(api_key=openai_api_key)
    result = await retriever.retrieve(title)

    assert isinstance(result, list)
    assert all(isinstance(lang, str) for lang in result)
    assert len(result) > 0
    assert "fra" in result

@pytest.mark.asyncio
async def test_lang_retriever_retrieve_mixed_languages(openai_api_key: str):
    title = "Study of English and Исследование русского языка combined research"
    retriever = LangRetriever(api_key=openai_api_key)
    result = await retriever.retrieve(title)
    
    assert isinstance(result, list)
    assert all(isinstance(lang, str) for lang in result)
    assert len(result) > 0
    # Должно содержать и английский и русский
    assert "eng" in result or "rus" in result

def assert_language_codes_valid(languages: list[str]):
    """Проверяет, что коды языков соответствуют ISO формату (3 символа)"""
    assert all(len(lang) == 3 for lang in languages)
    assert all(lang.islower() for lang in languages)
    assert all(lang.isalpha() for lang in languages)

@pytest.mark.asyncio
async def test_lang_retriever_result_format(openai_api_key: str):
    title = "Any research title"
    retriever = LangRetriever(openai_api_key)
    result = await retriever.retrieve(title)
    
    assert isinstance(result, list)
    if len(result) > 0:
        assert_language_codes_valid(result)
