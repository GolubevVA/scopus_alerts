from typing import Dict

_PROMPT_TEMPLATES: Dict[str, str] = {}

def register_template(name: str, template: str) -> None:
    '''
    Registers a new prompt template with a given name.
    '''
    if name in _PROMPT_TEMPLATES:
        raise ValueError(f"Template with name '{name}' is already registered.")
    _PROMPT_TEMPLATES[name] = template

def get_template(name: str) -> str:
    '''
    Retrieves a prompt template by its name.
    '''
    template = _PROMPT_TEMPLATES.get(name)
    if template is None:
        raise KeyError(f"Template with name '{name}' not found.")
    return template

LANG_RETRIEVER_V1_TEMPLATE_NAME = "lang_retriever_v1"
'''Prompt template's name used in the application.'''

def initialize_templates() -> None:
    '''
    Initializes all prompt templates used in the application.
    '''
    register_template(
        LANG_RETRIEVER_V1_TEMPLATE_NAME,
        """
            ### Роль: Лингвист.
            ### Задача:
            Идентифицируй **только те естественные языки**, которые являются **объектом исследования** в статье, на основе её заголовка. 

            Строго следуй алгоритму анализа.

            ### Алгоритм анализа:
            1. **Явные упоминания**:
            - Извлекай **прямые названия языков** (напр. "эрзянский" -> "myv").
            - Для архаичных форм используй исторические коды (напр. "древнеанглийский" -> "ang").  
            - Аргументируй для себя, почему тот или иной язык должен попасть в ответ.  
            - Выведи строго ISO639-3 коды только тех языков, которые прямо или косвенно названы как объект исследования в заголовке
            - Не учитывай язык написания статьи, не включай языки по культурным или географическим ассоциациям без прямого указания
            - Если нет прямого указания на языковой анализ, то не включай язык в ответ.
            - Если приведена языковая группа, то надо выдать все коды языков этой группы, включая диалекты и подобное. (Например, "тюркские" -> "tur", "kaz", "uzb" и т.д.)

            2. **Неявные ссылки через контекст**:
            - **Языковые семьи/группы** -> все языки в группе (напр. "тюркские" -> 40+ кодов).
            - **Геоуказатели** -> языки региона (напр. "языки Океании" -> все коды языков Океании).
            - **Лингвистические конструкции** -> языки, участвующие в сравнении (напр. "сравнение аориста в балканских языках" -> все коды балканских языков).

            3. **Жёсткие фильтры**:
            - Игнорируй язык написания статьи, если он не является объектом исследования.
            - Отсекай производные прилагательные без прямого указания на язык (напр. "германская рукопись" != "deu/gmh").
            - Учитывай только прямые упоминания языков/языковых семей

            ### Обдумывание:
            Прежде, чем выдавать ответ, обдумай его в поле "reasoning":
            1. Выпиши сначала в нем для себя все языки, которые ты считаешь объектами исследования в статье, а затем отфильтруй их по критериям выше. 
            2. Затем подумай о том, какие языки ты мог забыть. В рассуждающей манере допиши их дальше в поле "reasoning".
            3. Отфильтруй все языки согласно критериям выше тоже в формате рассуждений и выпиши отфильтрованный список далее в поле "reasoning".
            4. После этого запиши полученный список языков в массив "languages".

            ### Формат вывода:
            - Аргументируй для себя в поле "reasoning", почему тот или иной язык должен попасть в ответ.
            - Напиши в ответ строго **только коды ISO-639-3** в массиве "languages".
            
            ### Входные данные:
            Заголовок статьи: {title}
        """
    )
