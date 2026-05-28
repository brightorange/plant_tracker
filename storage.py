"""JSON-file persistence for the plant list."""
import json
import os

DATA_PATH = os.path.join("data", "plants.json")


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
    """Persist the plant list to the JSON file."""
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(plant_list, f, indent=2)
