"""JSON-file persistence for the plant list."""
import json
import os

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_DATA_DIR = os.path.join(_BASE_DIR, "data")
DATA_DIR = os.environ.get("PLANT_TRACKER_DATA_DIR", _DEFAULT_DATA_DIR)
DATA_PATH = os.path.join(DATA_DIR, "plants.json")


def load_plants():
    """Load plants from the JSON file, returning [] if the file is missing."""
    if not os.path.exists(DATA_PATH):
        return []
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_plants(plant_list):
    """Persist the plant list to the JSON file. Returns True on success."""
    try:
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(plant_list, f, indent=2)
        return True
    except OSError:
        return False
