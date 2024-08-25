SHELL := /bin/bash
python_version = {{cookiecutter.python_version}}
venv_prefix = {{cookiecutter.project_slug}}
venv_name = $(venv_prefix)-$(python_version)
pyenv_instructions=https://github.com/pyenv/pyenv#installation
pyenv_virt_instructions=https://github.com/pyenv/pyenv-virtualenv#pyenv-virtualenv


init: require_pyenv  ## Setup a dev environment for local development.
	@pwd
	@pyenv install $(python_version) -s
	@echo -e "\033[0;32m ✔️  🐍 $(python_version) installed \033[0m"
	@if ! [ -d "$$(pyenv root)/versions/$(venv_name)" ]; then\
		pyenv virtualenv $(python_version) $(venv_name);\
	fi;
	@pyenv local $(venv_name)
	@echo -e "\033[0;32m ✔️  🐍 $(venv_name) virtualenv activated \033[0m"
	@export PYENV_VERSION=$(venv_name); \
	export VIRTUAL_ENV=$$(pyenv prefix); \
	if uv --help >/dev/null 2>&1; then \
		uv pip install --upgrade uv; \
	else \
		pip install uv; \
	fi; \
	echo -e "\033[0;32m ✔️  uv installed \033[0m"; \
	if [ ! -f "tests/requirements-dev.txt" ]; then \
		make requirements; \
	fi; \
	uv pip sync tests/requirements-dev.txt; \
	uv pip install -e . --no-deps; \
	rm -rf *.egg-info; \
	echo -e "\nEnvironment setup! ✨ 🍰 ✨ 🐍 \n\nCopy this path to tell PyCharm where your virtualenv is. You may have to click the refresh button in the pycharm file explorer.\n"; \
	echo -e "\033[0;32m"; \
	pyenv which python; \
	echo -e "\n\033[0m"; \
	echo -e "The following commands are available to run in the Makefile\n"; \
	make -s help

af: autoformat  ## Alias for `autoformat`
autoformat:  ## Run the autoformatter.
	@-ruff check . --fix-only
	@ruff format .

autoformat-unsafe:  ## Run the autoformatter without --fix-only.
	@-ruff check . --fix-only --unsafe-fixes
	@ruff format .

test:  ## Run the tests.
	@pytest
	@echo -e "The tests pass! ✨ 🍰 ✨"

lint:  ## Run the code linter.
	@ruff check .
	@echo -e "No linting errors - well done! ✨ 🍰 ✨"

type-check: ## Run the type checker.
	@mypy .

deploy:  ## Deploy the package to pypi.org
	pip install twine build
	-git tag $$(python -m setuptools_scm)
	git push --tags
	rm -rf dist
	python -m build
	@echo 'pypi.org Username: '
	@read username && twine upload --verbose dist/* -u $$username;
	rm -rf build
	rm -rf dist
	@echo "Deploy successful! ✨ 🍰 ✨"

requirements:  ## Freeze the requirements.txt file
	@if ! [ -z "$(VIRTUAL_ENV)" ]; then \
		export VIRTUAL_ENV=$$(pyenv prefix); \
	fi; \
	if ! grep -q '^\[build-system\]' pyproject.toml; then \
		echo "No [build-system] section found. Assuming application project. Generating requirements.txt"; \
		uv pip compile pyproject.toml --output-file=requirements.txt || exit 1; \
		echo "Generating tests/requirements-dev.txt"; \
		uv pip compile pyproject.toml --extra dev --output-file=tests/requirements-dev.txt \
			--constraint requirements.txt || exit 1; \
	else \
		echo "[build-system] section found. Assuming library project."; \
		echo "Generating tests/requirements-dev.txt"; \
		uv pip compile pyproject.toml --extra dev --output-file=tests/requirements-dev.txt || exit 1; \
	fi


require_pyenv:
	@if ! [ -x "$$(command -v pyenv)" ]; then\
	  echo -e '\n\033[0;31m ❌ pyenv is not installed.  Follow instructions here: $(pyenv_instructions)\n\033[0m';\
	  exit 1;\
	else\
	  echo -e "\033[0;32m ✔️  pyenv installed\033[0m";\
	fi
	@if ! [[ "$$(pyenv virtualenv --version)" == *"pyenv-virtualenv"* ]]; then\
	  echo -e '\n\033[0;31m ❌ pyenv virtualenv is not installed.  Follow instructions here: $(pyenv_virt_instructions) \n\033[0m';\
	  exit 1;\
	else\
	  echo -e "\033[0;32m ✔️  pyenv-virtualenv installed\033[0m";\
	fi


help: ## Show this help message.
	@## https://gist.github.com/prwhite/8168133#gistcomment-1716694
	@echo -e "$$(grep -hE '^\S+:.*##' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' -e 's/^\(.\+\):\(.*\)/\\x1b[36m\1\\x1b[m:\2/' | column -c2 -t -s :)" | sort