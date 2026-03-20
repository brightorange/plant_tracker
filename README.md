# Plant Tracker

A command-line application for managing your plant collection. Track your plants, their locations, and watering schedules.

## Features

- **Add plants** — Enter name, location, last watered date, and watering interval. Duplicate names are rejected; keep adding until `exit`.
- **View plants** — Browse your collection filtered by all, name, location, or plants that need watering now. Displays a table with each plant's next watering date and a `>>> WATER NOW <<<` indicator when overdue.
- **Remove plants** — Remove plants by exact name in a loop until you type `exit`.
- **Edit plant** — Update name, location, last watered date, or watering interval from an interactive menu.
- **Water plants** — Mark plants as watered today. Filter by plants that need water now: all of them, all in chosen location, one plant by name.
- **Load dummy data** — Populate the app with 15 sample plants from `data/dummy.csv` for testing.

## Project Structure

```
python_final/
├── main.py           # Entry point; runs the main menu loop
├── add_plants.py     # Add one or more plants with validation
├── edit_plants.py    # Edit fields of an existing plant
├── remove_plants.py  # Remove plants by name until exit
├── view_plants.py    # Display plants in a table with filters
├── water_plants.py   # Water plants; shared need_water / next_watering_date logic
├── load_data.py      # Load sample plant data from CSV
└── data/
    └── dummy.csv     # 15 sample plants across 7 locations
```

## Getting Started

### Running the App

```bash
python main.py
```

### Main Menu

```
1. Add plants
2. View plants
3. Remove plants
4. Edit plant
5. Water plants!
6. View summary
7. Load dummy data from file
8. Exit
```

### View Plants Sub-menu

```
1. All
2. Name
3. Location
4. Need watering now
```

### Water Plants Sub-menu

```
1. All plants that need water now
2. All plants at a location
3. A single plant by name
```

### Edit Plant Sub-menu

```
1. Name
2. Location
3. Last watered date
4. Water interval (days)
```

Enter `exit` at prompts to return to the previous menu.

## Plant Data Format

Each plant is stored as a dictionary with the following fields:

| Field | Type | Example |
|---|---|---|
| `name` | string | `monstera` |
| `location` | string | `salon` |
| `last_watered` | string `YYYY-MM-DD` | `2026-03-01` |
| `water_interval_days` | integer | `7` |

## Open to contributions

# Display how overdue watering is

Improve `view_plants.plants_info` function
If the plant needs watering, display how overdue the date in `status` field.

#  Add information about water need

Add new text field to plant that show how much water is need, is it high-watered or draught-tolerant

