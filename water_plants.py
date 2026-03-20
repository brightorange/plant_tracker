from datetime import date, datetime


def next_watering_date(plant):
    """Return the next watering date for a plant as a date object."""
    from datetime import timedelta
    last_watered = datetime.strptime(plant["last_watered"], "%Y-%m-%d").date()
    return last_watered + timedelta(days=plant["water_interval_days"])


def need_water(plant):
    """Return True if the plant's next watering date is today or overdue."""
    next_date = next_watering_date(plant)
    return next_date <= date.today()


def get_plants_needing_water(plant_list, location=None):
    """Return a list of plants that need watering today, optionally filtered by location."""
    plants_to_water = []

    for plant in plant_list:
        if location:
            location_matches = plant["location"].lower() == location.lower()
        else:
            location_matches = True
        if location_matches and need_water(plant):
            plants_to_water.append(plant)

    return plants_to_water


def water_plants(plant_list):
    """Prompt the user to select which plants to water and mark them as watered today.

    Offers filtering by all overdue plants, by location, or by name.
    Returns the updated plant_list.
    """
    if not plant_list:
        print("No plants in your list yet.\n")
        return plant_list

    while True:
        choice = input("""
    Which plants do you want to water?
    1. All plants that need water now
    2. All plants at a location
    3. A single plant by name
    Type 'exit' to return to the main menu.\n""")

        if choice.lower() == "exit":
            break

        elif choice == "1":
            plants_to_water = get_plants_needing_water(plant_list)
            if not plants_to_water:
                print("No plants need watering today.\n")
            else:
                confirm_and_water(plants_to_water)

        elif choice == "2":
            location = input("Enter location:\n")
            plants_to_water = get_plants_needing_water(plant_list, location=location)
            if not plants_to_water:
                print(f"No plants at '{location}' need watering today.\n")
            else:
                confirm_and_water(plants_to_water)

        elif choice == "3":
            name = input("Enter plant name:\n").lower()
            matches = [p for p in plant_list if p["name"].lower() == name]
            if matches:
                confirm_and_water(matches)
            else:
                print(f"No plant named '{name}' found.\n")

        else:
            print("Invalid option.\n")

    return plant_list

def confirm_and_water(plants):
    """Ask for confirmation, then set last_watered to today for all plants in the list."""
    today = str(date.today())
    print(f"\nPlants to be watered ({len(plants)}):")
    for plant in plants:
        print(f"  - {plant['name']} ({plant['location']})")

    confirm = input("\nMark all as watered today? (yes/no)\n")
    if confirm.lower() == "yes":
        for plant in plants:
            plant["last_watered"] = today
        print(f"Done! {len(plants)} plant(s) marked as watered on {today}.\n")
    else:
        print("Cancelled. No changes made.\n")
