# tests/conftest.py
import sys
from pathlib import Path

# Ensure `src/` is on sys.path before test modules import from exercises
repo_root = Path(__file__).resolve().parent.parent
src_dir = repo_root / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))
