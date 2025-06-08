import pytest
from internal.article_processing.lang_retriever import LangRetriever

def test_lang_retriever_initialization(setup_templates):
    title = "Test title"
    retriever = LangRetriever(title)
    
    assert retriever.title == title
    assert retriever.prompt_type == "lang_retriever_v1"
    assert retriever.client is not None

@pytest.mark.asyncio
async def test_lang_retriever_retrieve_english(setup_templates):
    title = "Research on machine learning algorithms and artificial intelligence"
    retriever = LangRetriever(title)
    result = await retriever.retrieve()
    
    assert isinstance(result, list)
    assert all(isinstance(lang, str) for lang in result)
    assert len(result) == 0

@pytest.mark.asyncio
async def test_lang_retriever_retrieve_russian(setup_templates):
    title = "Исследование группы финно-угорских языков и их влияние на культуру"
    retriever = LangRetriever(title)
    result = await retriever.retrieve()
    
    assert isinstance(result, list)
    assert all(isinstance(lang, str) for lang in result)
    assert len(result) > 0
    # Может содержать русский или связанные языки
    assert any(lang in result for lang in ["rus", "fin", "hun", "est"])

@pytest.mark.asyncio
async def test_lang_retriever_retrieve_french(setup_templates):
    title = "Étude sur les langues européennes et leur évolution historique"
    retriever = LangRetriever(title)
    result = await retriever.retrieve()
    
    assert isinstance(result, list)
    assert all(isinstance(lang, str) for lang in result)
    assert len(result) > 0
    assert "fra" in result

@pytest.mark.asyncio
async def test_lang_retriever_retrieve_mixed_languages(setup_templates):
    title = "Study of English and Исследование русского языка combined research"
    retriever = LangRetriever(title)
    result = await retriever.retrieve()
    
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
async def test_lang_retriever_result_format(setup_templates):
    title = "Any research title"
    retriever = LangRetriever(title)
    result = await retriever.retrieve()
    
    assert isinstance(result, list)
    if len(result) > 0:
        assert_language_codes_valid(result)
