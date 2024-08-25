# CookieCutter PyPackage AI  🐍✨️

**AI-powered cookiecutter template for python projects**

## Features

- Uses latest tooling (ruff, uv, pyproject.toml, pytest)
- Automatically generates project structure and makes a first attempt at coding the project
- Follows best practices

## Example Generated Project
These projects are uploaded without any fixes so you can accurately judge how well the code generator works.
- [Password Generator](https://github.com/brycedrennan/generated-password-generator)

## Getting started
Requirements:
- pyenv installed
```bash
pip install cookiecutter anthropic
export ANTHROPIC_API_KEY=<your-api-key>
# interactive inputs
cookiecutter gh:brycedrennan/cookiecutter-pypackage-ai
# or without interactive inputs
cookiecutter --no-input gh:brycedrennan/cookiecutter-pypackage-ai/cookiecutter-pypackage-ai project_name="password generator" detailed_project_description="library that generates various kinds of passwords"
```
