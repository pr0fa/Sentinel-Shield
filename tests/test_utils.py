import os

def get_fixture_path(filename):
    """Helper to get the absolute path to a test fixture file."""
    return os.path.join(os.path.dirname(__file__), "sample_files", filename)

def read_fixture(filename):
    """Helper to read the content of a test fixture file."""
    path = get_fixture_path(filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()