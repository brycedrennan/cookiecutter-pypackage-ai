import base64
import json
import sys
from functools import lru_cache
from pathlib import Path

from cookiecutter import main
from jinja2.ext import Extension
from llmgen.llm_context import generate_context_value

cookiecutter_json_path = Path(__file__).parent / "cookiecutter.json"


# add the directory this file is in to the sys path
this_template_dir = Path(__file__).parent
sys.path.append(this_template_dir)

GREEN = "\033[32m"  # Green text
RESET = "\033[0m"  # Reset to default color

SYSTEM_PROMPT = "You are a coding assistant. Always do exactly what is asked. Do not provide explanations unless explicitly asked."


def hooked_dump(f):
    if getattr(f, 'is_monkeypatched', False):
        return f

    def wrapper(replay_dir, template_name: str, context: dict):
        # print the starting context
        print(f"{GREEN}Starting context:{RESET}")
        for k, v in context["cookiecutter"].items():
            print(f"  {k}: {v}")
        post_input_context_hook(context["cookiecutter"], prompts=load_prompts())
        return f(replay_dir=replay_dir, template_name=template_name, context=context)

    wrapper.is_monkeypatched = True
    wrapper._orig = f
    return wrapper


main.dump = hooked_dump(main.dump)


class ContextModifyExtension(Extension):
    """Necessary for the monkeypatch to work
    Maybe just so this file loads and runs the monkepat
    """


@lru_cache()
def load_prompts():
    import json
    with open(cookiecutter_json_path) as f:
        return json.load(f)["__prompts__"]


def post_input_context_hook(context, prompts):
    for k, v in list(context.items()):
        if k.startswith("__"):
            context[k[2:]] = context[k]

    # handle prompts
    for keyname, instructions in prompts.items():
        current_value = context.get(keyname)
        if not current_value or current_value == "[AUTOGENERATE]":
            context[keyname] = generate_context_value(
                field_name=keyname,
                field_instructions=instructions,
                cookiecutter_context=context
            )

    # generate python_package_list
    if context.get("python_packages"):
        python_package_list = context["python_packages"].split(",")
        python_package_list = [p.strip() for p in python_package_list]
        context["python_package_list"] = python_package_list

    project_files = parse_file_structure(context["project_structure"])
    project_files.extend(parse_file_structure(context["test_structure"]))
    generate_structure_files(project_files, cookiecutter_context=context)

    # base64 encode all the context data
    context_json = json.dumps(context)
    context_b64 = base64.b64encode(context_json.encode("utf-8"))
    context_b64_str = context_b64.decode("utf-8")
    context["context_b64"] = context_b64_str


def parse_file_structure(file_structure) -> list[str]:
    lines = file_structure.split("\n")
    filenames = []
    for line in lines:
        line = line.strip()
        if line.startswith("- "):
            line = line[2:]
            line = line.strip().strip("`").strip()
            filenames.append(line)
    return filenames


def generate_structure_files(project_files: list[str], cookiecutter_context):
    # generate files from `project_structure` and `test_structure`
    
    cookiecutter_context.setdefault("project_file_contents", {})
    project_file_contents = cookiecutter_context["project_file_contents"]
    for file in project_files:
        instructions = f"Generate the content for the `{file}` file. Keep the design concise and correct. Do not include the file name or backticks in the response. If its for tests then use pytest and only cover the base cases. Respond only with the content."
        file_contents = generate_context_value(field_name=file, field_instructions=instructions, cookiecutter_context=cookiecutter_context)
        project_file_contents[file] = file_contents

    # for file in project_files:
    #     instructions = f"Review the code and generate a new revision for the `{file}` file.  Fix any issues and make any improvements you think are needed.  Output the new file in its entirety. Do not include the file name or backticks in the response.  All files should have valid endings. Respond only with the content."
    #     file_contents = generate_context_value(key_name=file, instructions=instructions, cookie_context=cookie_context)
    #     project_file_contents[file] = file_contents

