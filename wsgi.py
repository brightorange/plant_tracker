"""WSGI entry point for Apache mod_wsgi (or any WSGI server like gunicorn)."""
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

os.chdir(PROJECT_DIR)

from storage import DATA_DIR, DATA_PATH  # noqa: E402

if not os.path.isdir(DATA_DIR):
    os.makedirs(DATA_DIR, exist_ok=True)

from app import app as application  # noqa: E402  (Apache looks for `application`)
