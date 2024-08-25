# CookieCutter AI PyPackage  🐍✨️

**AI-powered cookiecutter template for python projects**

## Features

- Uses latest tooling (ruff, uv, pyproject.toml, pytest)
- Automatically generates project structure and makes a first attempt at coding the project
- Follows best practices

## Getting started
Requirements:
- pyenv installed
```bash
pip install cookiecutter anthropic
export ANTHROPIC_API_KEY=<your-api-key>
# interactive inputs
cookiecutter gh:brycedrennan/cc-python-pkg
# or without interactive inputs
cookiecutter --no-input ~/projects/cc-python-pkg project_name="password generator" detailed_project_description="library that generates various kinds of passwords"
```
