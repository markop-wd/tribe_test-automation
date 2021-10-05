from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def get_dot_env() -> Path:
    return get_project_root().joinpath('.env')
