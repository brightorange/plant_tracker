import csv

DUMMY_DATA_PATH = "data/dummy.csv"

def load_data(plant_list):
    """Load plants from the dummy CSV file into plant_list.

    Prompts the user to choose between replacing the existing list or
    appending to it. Duplicate names are skipped in append mode.
    Returns the updated plant_list.
    """
    print("""
    How would you like to load the dummy data?
    1. Replace existing data
    2. Append to existing data
    """)
    mode = input("Enter option number, or 'exit' to cancel:\n")

    if mode.lower() == "exit":
        return plant_list

    if mode == "1":
        plant_list = read_dummy_data()
    elif mode == "2":
        new_plants = read_dummy_data()
        existing_names = set()
        for plant in plant_list:
            existing_names.add(plant["name"].lower())
        for plant in new_plants:
            if plant["name"].lower() in existing_names:
                print(f"A plant named '{plant['name']}' already exists. Skipping...\n")
            else:
                plant_list.append(plant)
    else:
        print("Invalid option, no data loaded.\n")
        return plant_list

    return plant_list


def read_dummy_data():
    """Read and parse the dummy CSV file, returning a list of plant dicts."""
    plants = []
    try:
        with open(DUMMY_DATA_PATH, 'r') as file:
            for row in csv.reader(file):
                if len(row) != 4:
                    continue
                plants.append({
                    "name": row[0].strip(),
                    "location": row[1].strip(),
                    "last_watered": row[2].strip(),
                    "water_interval_days": int(row[3].strip())
                })
    except FileNotFoundError:
        print(f"File '{DUMMY_DATA_PATH}' not found.\n")
    return plants
