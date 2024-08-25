import json
import base64
import os
import subprocess


project_context_b64 = """{{cookiecutter.context_b64}}"""


project_context = json.loads(base64.b64decode(project_context_b64))


def main():
    try:
        with open("project_context.json", "w") as f:
            json.dump(project_context, f, indent=4)
    except Exception as e:
        print(f"Error writing project context: {e}")

    for file, contents in project_context.get("project_file_contents", {}).items():
        # make the directory if it doesn't exist
        try:
            os.makedirs(os.path.dirname(file), exist_ok=True)
        except Exception as e:
            print(f"Error making directory for file {file}: {e}")
        try:
            with open(file, "w") as f:
                f.write(contents)
        except Exception as e:
            print(f"Error writing file {file}: {e}")
    subprocess.run(["git", "init"], check=False)
    subprocess.run(["git", "commit", "--allow-empty", "-m", "Project start"], check=False)
    subprocess.run(["make", "init"], check=False)
    subprocess.run(["make", "autoformat-unsafe"], check=False)


main()