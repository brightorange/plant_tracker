import re

def add_plants(plant_list):
    """Prompt the user for plant details and add plants to plant_list.

    Validates that the name is unique, the date is in YYYY-MM-DD format,
    and the watering interval is a positive integer. Loops until the user
    types 'exit' at the name prompt, then returns the updated plant_list.
    """
    while True:
        new_plant = {
            "name": None,
            "location": None,
            "last_watered": None,
            "water_interval_days": None
        }

        new_plant["name"] = input("Please enter the name of the plant, or 'exit' to go back\n")
        if new_plant["name"].lower() == "exit":
            return plant_list

        duplicate_name = False
        for plant in plant_list:
            if plant["name"].lower() == new_plant["name"].lower():
                duplicate_name = True
                break
        if duplicate_name:
            print(f"A plant named '{new_plant['name']}' already exists. Please choose a different name.\n")
            continue

        new_plant["location"] = input("Please enter the location of the plant, or 'exit' to cancel this plant\n")
        if new_plant["location"].lower() == "exit":
            continue

        while True:
            last_watered_date = input("Please enter the last date the plant was watered, format: YYYY-MM-DD, or 'exit' to cancel this plant\n")
            if last_watered_date.lower() == "exit":
                break
            if re.match(r"^\d{4}-\d{2}-\d{2}$", last_watered_date):
                new_plant["last_watered"] = last_watered_date
                break
            print("Invalid date format, please use YYYY-MM-DD (e.g. 2026-03-15)\n")
        if new_plant["last_watered"] is None:
            continue

        while True:
            input_water_interval_days = input("Please enter the water interval in days, or 'exit' to cancel this plant\n")
            if input_water_interval_days.lower() == "exit":
                break
            if input_water_interval_days.isdigit() and int(input_water_interval_days) > 0:
                new_plant["water_interval_days"] = int(input_water_interval_days)
                break
            print("Invalid input, please enter a positive whole number (e.g. 7)\n")
        if new_plant["water_interval_days"] is None:
            continue

        plant_list.append(new_plant)
        print(f"Plant '{new_plant['name']}' added successfully.\n")
