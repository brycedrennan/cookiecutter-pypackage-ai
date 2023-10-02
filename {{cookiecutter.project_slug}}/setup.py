import subprocess
from functools import lru_cache

from setuptools import find_packages, setup


@lru_cache
def get_git_revision_hash() -> str:
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "HEAD"])
            .decode("ascii")
            .strip()
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return "no-git"


revision_hash = get_git_revision_hash()

with open("README.md", encoding="utf-8") as f:
    readme = f.read()
    readme = readme.replace(
        '<img src="',
        f'<img src="{{cookiecutter.github_content_url}}/{revision_hash}/',
    )

setup(
    name="{{cookiecutter.project_name}}",
    author="{{cookiecutter.full_name}}",
    version="{{cookiecutter.version}}",
    description="{{cookiecutter.project_short_description}}",
    long_description=readme,
    long_description_content_type="text/markdown",
    project_urls={
        "Documentation": "{{cookiecutter.github_url}}",
        "Source": "{{cookiecutter.github_url}}",
    },
    packages=find_packages(include=("{{cookiecutter.python_module_name}}", "{{cookiecutter.python_module_name}}.*")),
    scripts=[],
    entry_points={},
    package_data={"{{cookiecutter.python_module_name}}": []},
    install_requires=[
        {%- for package in cookiecutter.python_package_list -%}
        "{{package}}",
        {%- endfor -%}
    ],
    # don't specify maximum python versions as it can cause very long dependency resolution issues as the resolver
    # goes back to older versions of packages that didn't specify a maximum
    # https://discuss.python.org/t/requires-python-upper-limits/12663/75
    python_requires=">=3.8",
)
