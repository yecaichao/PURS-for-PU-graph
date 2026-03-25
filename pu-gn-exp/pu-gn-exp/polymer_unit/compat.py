from pathlib import Path
import sys


def ensure_repo_root_on_path():
    current = Path(__file__).resolve()
    repo_root = current.parents[3]
    repo_root_str = str(repo_root)
    if repo_root.is_dir() and repo_root_str not in sys.path:
        sys.path.insert(0, repo_root_str)
    return repo_root
