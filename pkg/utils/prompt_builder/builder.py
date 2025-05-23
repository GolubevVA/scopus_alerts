from typing import Dict
from .registry import get_template

def build_prompt(title: str, prompt_type: str) -> str:
    try:
        template = get_template(prompt_type)
    except Exception as e:
        raise RuntimeError(f"Failed to get template for prompt_type '{prompt_type}': {e}")

    try:
        prompt = template.format(title=title)
    except KeyError as e:
        raise RuntimeError(f"Template formatting error: missing placeholder {e} in template '{prompt_type}'")
    except Exception as e:
        raise RuntimeError(f"Failed to format template '{prompt_type}': {e}")

    return prompt
