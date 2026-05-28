# Plant Tracker

A web application (Flask) for managing your plant collection. Track plants, their locations, and watering schedules from a clean browser UI. A legacy CLI version is still available via `main.py`.

## Features

- **Plant list** — Browse all plants in a table with name, location, last watered date, watering interval, next watering date, and a clear "Water now" badge when overdue.
- **Filtering & search** — Filter by all plants, by name, by location, or only plants that need water now.
- **Add / Edit / Remove** — Forms with validation (unique name, YYYY-MM-DD date, positive integer interval).
- **Water plants** — One-click "Water" per row, "Water all that need water" from the home page, or "Water all at location <name>".
- **Summary view** — Stat cards for total plants and overdue plants, plus a quick list of plants that need water today.
- **Dummy data loader** — Append or replace from `data/dummy.csv` (15 sample plants).
- **Persistence** — Plants are stored in `data/plants.json` between runs.

## Project Structure

```
plant_tracker-1/
├── app.py             # Flask web app (routes, validation, controllers)
├── storage.py         # JSON-file persistence (data/plants.json)
├── water_plants.py    # Shared logic: need_water / next_watering_date
├── load_data.py       # Read sample plants from CSV
├── main.py            # Legacy CLI entry point (still works)
├── add_plants.py      # CLI: add plants
├── edit_plant.py      # CLI: edit a plant
├── remove_plants.py   # CLI: remove plants
├── view_plants.py     # CLI: view plants / summary
├── templates/         # Jinja templates (base, index, add, edit, summary)
├── static/style.css   # App styling
└── data/
    ├── dummy.csv      # 15 sample plants across 7 locations
    └── plants.json    # Created on first save (gitignored)
```

## Getting Started

### 1. Create a virtual environment and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the web app

```bash
python app.py
```

Then open <http://127.0.0.1:5000> in your browser.

### Alternative: run the CLI

```bash
python main.py
```

(The CLI keeps plants only in memory for the current session.)

## Routes

| Method | Path                  | Description                                            |
|--------|-----------------------|--------------------------------------------------------|
| GET    | `/`                   | List plants, with optional `?filter=` and `?q=`        |
| GET/POST | `/add`              | Add a new plant                                        |
| GET/POST | `/edit/<name>`      | Edit an existing plant                                 |
| POST   | `/delete/<name>`      | Remove a plant                                         |
| POST   | `/water/<name>`       | Mark a single plant as watered today                   |
| POST   | `/water-needing`      | Water all plants that need water now                   |
| POST   | `/water-location`     | Water all plants at a given location                   |
| POST   | `/load-dummy`         | Load `data/dummy.csv` (`mode=append` or `mode=replace`)|
| GET    | `/summary`            | Collection summary                                     |

## Plant Data Format

Each plant is stored as a JSON object with the following fields:

| Field | Type | Example |
|---|---|---|
| `name` | string | `monstera` |
| `location` | string | `salon` |
| `last_watered` | string `YYYY-MM-DD` | `2026-03-01` |
| `water_interval_days` | integer | `7` |

## Open to contributions

Contributions are welcome. Good next features:

### 1) Show overdue days in status

- **Goal**: show how many days a plant is overdue alongside the "Water now" badge.
- **Where**: `water_plants.py` (`next_watering_date`, `need_water`), `app.py` (`_decorate`), and `templates/index.html`.

### 2) Add water-need profile per plant

- **Goal**: support a field like `water_need` (`low`, `medium`, `high`).
- **Where**: `app.py` (forms + validation), `templates/add.html` / `edit.html`, `data/dummy.csv`, `load_data.py`.

### 3) Improve water interval validation

- **Goal**: validate `water_interval_days` with a realistic range (for example `1..180`).
- **Where**: `app.py` validation in `/add` and `/edit/<name>`.
