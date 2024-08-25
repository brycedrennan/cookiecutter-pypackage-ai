import os
from pathlib import Path

from typing import Any
from anthropic import Anthropic
from jinja2 import Environment, FileSystemLoader

llmgen_dir = Path(__file__).parent
PROMPT_DIR = llmgen_dir / "prompts"
ANTHROPIC_MODEL = "claude-3-5-sonnet-20240620"
ANTHROPIC_KEY = os.environ["ANTHROPIC_API_KEY"]


env = Environment(loader=FileSystemLoader(PROMPT_DIR))

def get_llm_response(
    prompt: str,
    model: str = ANTHROPIC_MODEL,
    max_tokens: int = 2048,
) -> str:
    client = Anthropic(api_key=ANTHROPIC_KEY)
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    content = response.content[0].text
    return content


def get_llm_response_from_template(
    template_name: str, template_kwargs: dict[str, Any], max_tokens: int = 2048
) -> str:
    # print(f"LLM template: {template_name}")
    # print(f"LLM template kwargs: {template_kwargs}")
    prompt = render_prompt(template_name, template_kwargs)
    # print(f"LLM rendered prompt: \n{prompt}\n")
    return get_llm_response(prompt, max_tokens=max_tokens)


def render_prompt(prompt_name: str, prompt_kwargs: dict[str, Any]) -> str:
    template = env.get_template(f"{prompt_name}.md")
    return template.render(**prompt_kwargs)




