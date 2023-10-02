import os.path

from pathlib import Path

project_dir = str(Path(__file__).parent.parent)
tests_dir = os.path.join(project_dir, "tests")
test_data_dir = os.path.join(tests_dir, "data")
