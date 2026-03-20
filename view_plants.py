from water_plants import get_plants_needing_water, need_water, next_watering_date

def view_plants_menu(plant_list):
    """Handle one view-menu interaction and return the result.

    Returns:
        dict: {
            "continue": bool,  # False when user chose exit
            "output": str      # text to display for this step
        }
    """
    input_filter = input("""
Choose a filter to view plants:
    1. All
    2. Name
    3. Location
    4. Need watering now
    Type 'exit' to return to the main menu.\n""").strip().lower()

    if input_filter == "exit":
        return {"continue": False, "output": ""}
    else:
        return {"continue": True, "output": view_plants(input_filter, plant_list)}

def view_plants(filter_by, plant_list):
    """Return as a string the plants filtered by the given option.
    filter_by options:
        "1" - all plants
        "2" - search by exact name (case-insensitive)
        "3" - search by exact location (case-insensitive)
        "4" - plants that need watering now
    """
    if not plant_list:
        return "No plants in your list yet. Add plants or load dummy data (option 7).\n"

    if filter_by == "1":
        return plants_info(plant_list)

    elif filter_by == "2":
        plant_name = input("Enter the plant name to search for:\n").strip().lower()
        plant_list_filtered = []
        for plant in plant_list:
            if plant_name == plant["name"].lower():
                plant_list_filtered.append(plant)
        if plant_list_filtered:
            return plants_info(plant_list_filtered)
        else:
            return f"No plants found with name '{plant_name}'.\n"

    elif filter_by == "3":
        plant_location = input("Enter the location to search for:\n").strip().lower()
        plant_list_filtered = []
        for plant in plant_list:
            if plant_location == plant["location"].lower():
                plant_list_filtered.append(plant)
        if plant_list_filtered:
            return plants_info(plant_list_filtered)
        else:
            return f"No plants found in location '{plant_location}'.\n"

    elif filter_by == "4":
        plant_list_filtered = get_plants_needing_water(plant_list)
        if plant_list_filtered:
            return f"""\nPlants that need watering today:\n{plants_info(plant_list_filtered)}"""
        else:
            return "No plants need watering today.\n"

    else:
        return f"Unknown filter '{filter_by}'. Choose: 1, 2, 3, 4 or 'exit' to return to the main menu.\n"


def plants_info(plant_list):
    """Return as a string the information table of plants with name, location, dates, interval, and water status."""
    
    plants_info = f"""Name               Location             Last Watered      Interval (days)   Next Watering       Status
{"-" * 110}\n"""

    for p in plant_list:
        next_date = next_watering_date(p)
        next_str = str(next_date) if next_date else "N/A"
        status = ">>> WATER NOW <<<" if need_water(p) else ""
        plants_info += f"{p['name']:<20} {p['location']:<20} {p['last_watered']:<15} {str(p['water_interval_days']):<16} {next_str:<15} {status}\n"

    return plants_info

def summary(plant_list):
    """Return as a string the summary table: totals, need watering now, 
    and a formatted table of plants with name, location, dates, interval, and water status."""

    total = len(plant_list)
    need_water_now = get_plants_needing_water(plant_list)

    summary = f"""
    {'='*40}
    PLANT COLLECTION SUMMARY
    {'='*40}
    Total plants       : {total}
    Need watering now  : {len(need_water_now)}
    {'='*40}\n
    """

    if need_water_now:
        summary += "Plants that need watering now:\n"
        for p in need_water_now:
            summary += f"    >>> {p['name']} ({p['location']})\n"
    summary += "\n"
    summary += plants_info(plant_list)

    return summary