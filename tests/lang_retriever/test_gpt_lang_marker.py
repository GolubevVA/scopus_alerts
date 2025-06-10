import pytest
import os
from unittest.mock import patch
from internal.article_processing.gpt_lang_marker import GPTLangMarker, DEfAULT_MODEL
from tests.lang_retriever.utils import flaky_passes

def test_gpt_lang_marker_initialization(openai_api_key: str):
    marker = GPTLangMarker(api_key=openai_api_key)
    assert marker.api_key == openai_api_key
    assert marker.model == DEfAULT_MODEL
    assert marker.client is not None

@patch.dict(os.environ, {}, clear=True)
def test_gpt_lang_marker_initialization_missing_key():
    with pytest.raises(ValueError, match="API key must be provided"):
        GPTLangMarker(api_key=None)

@pytest.mark.asyncio
@flaky_passes()
async def test_gpt_lang_marker_generate_english(gpt_lang_marker: GPTLangMarker):
    prompt = """
    Твоя задача — определить язык текста, который будет задан ниже. Ты можешь подумать над своим ответом в поле "reasoning". Ответь дай в поле "languages", в список помести один язык в кодировке ISO-639-3 — ответ на вопрос о том, какой язык используется в тексте ниже.

    Текст: "Hello world, how are you today?"
    """
    result = await gpt_lang_marker.generate(prompt)
    
    assert isinstance(result, dict)
    assert "languages" in result
    assert "reasoning" in result
    assert isinstance(result["languages"], list)
    assert "eng" in result["languages"]

@pytest.mark.asyncio
@flaky_passes()
async def test_gpt_lang_marker_generate_russian(gpt_lang_marker: GPTLangMarker):
    prompt = """
    Определи язык следующего текста. Обязательно верни ответ в кодировке ISO-639-3. 
    Текст: "Привет мир, как дела?"

    Обрати внимание на то, что тебе нужно определить язык текста, а не язык этого запроса. Ты можешь подумать над своим ответом в поле "reasoning". Ответь дай в поле "languages", в список помести один язык в кодировке ISO-639-3 — ответ на вопрос, какой язык используется в тексте.
    """
    result = await gpt_lang_marker.generate(prompt)
    
    assert isinstance(result, dict)
    assert "languages" in result
    assert "reasoning" in result
    assert isinstance(result["languages"], list)
    assert "rus" in result["languages"]

@pytest.mark.asyncio
@flaky_passes()
async def test_gpt_lang_marker_generate_french(gpt_lang_marker: GPTLangMarker):
    prompt = """
    Определи язык следующего текста. Обязательно верни ответ в кодировке ISO-639-3. 
    Текст: "Bonjour le monde, comment allez-vous?"

    Обрати внимание на то, что тебе нужно определить язык текста, а не язык этого запроса. Ты можешь подумать над своим ответом в поле "reasoning". Ответь дай в поле "languages", в список помести один язык в кодировке ISO-639-3 — ответ на вопрос, какой язык используется в тексте.
    """
    result = await gpt_lang_marker.generate(prompt)
    
    assert isinstance(result, dict)
    assert "languages" in result
    assert "reasoning" in result
    assert isinstance(result["languages"], list)
    assert "fra" in result["languages"]
