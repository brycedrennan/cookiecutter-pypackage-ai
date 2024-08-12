import os
import re

from llmgen.llm import get_llm_response_from_template



GREEN = "\033[32m"  # Green text
RESET = "\033[0m"  # Reset to default color

SYSTEM_PROMPT = "You are a coding assistant. Always do exactly what is asked. Do not provide explanations unless explicitly asked."


def filtered_cookie_context(context):
    keys_to_filter = {
        "_extensions", "_output_dir", "_repo_dir", "_checkout"
    }
    cookie_context = {}
    for k, v in context.items():
        if k not in keys_to_filter:
            cookie_context[k] = v
    return cookie_context


def generate_context_value_anthropic(field_name, field_instructions, cookiecutter_context):
    print(f"{GREEN}Generating value for '{field_name}' using Anthropic...{RESET}")
    cookiecutter_context = filtered_cookie_context(cookiecutter_context)
    template_kwargs = {
        "field_name": field_name,
        "field_instructions": field_instructions,
        "cookiecutter_context": cookiecutter_context
    }
    content = get_llm_response_from_template(
        "fill-in-with-context",
        template_kwargs,
        max_tokens=8192
    )
    # extract the <final_value> tag
    print(content)
    match = re.search(r'<final_value>(.*?)</final_value>', content, re.DOTALL)
    if match:
        final_value = match.group(1).strip()
        return final_value
    else:
        print("ERROR: No final value found in the response.")
        return ""



def generate_context_value(field_name, field_instructions, cookiecutter_context):
    if os.environ.get("ANTHROPIC_API_KEY"):
        return generate_context_value_anthropic(field_name, field_instructions, cookiecutter_context)
    else:
        raise ValueError("No API key found. Please set ANTHROPIC_API_KEY environment variable.")