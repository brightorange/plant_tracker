import re

def edit_plant(plant_list):
    """Prompt for a plant name then interactively edit its fields via a sub-menu.
    Allows updating name (with uniqueness check), location, last watered date,
    and watering interval. The edit submenu runs until the user enters 'exit'.
    Returns the updated plant_list.
    """
    plant_name = input("Enter the name of the plant to edit, or 'exit' to go back:\n")
    if plant_name.lower() == "exit":
        return plant_list

    for plant in plant_list:
        if plant["name"] == plant_name:
            break
    else:
        print(f"No plant named '{plant_name}' found.\n")
        return plant_list

    while True:
        print(f"Editing '{plant['name']}'. What would you like to change?")
        input_option=input("""
        1. Name
        2. Location
        3. Last watered
        4. Water interval
        Please enter 'exit' to go back to the main menu.
        """)

        if input_option == "exit":
            return plant_list

        elif input_option == "1":
            new_name = input("Enter new name:\n")
            if new_name == "exit":
                continue
            for p in plant_list:
                if p["name"] == new_name:
                    print(f"A plant named '{new_name}' already exists. Please choose a different name.\n")
                    break
            else:
                plant["name"] = new_name
                print("Name updated.\n")
          
        elif input_option == "2":
            new_location = input("Enter new location:\n")
            if new_location == "exit":
                continue
            plant["location"] = new_location
            print("Location updated.\n")
            continue

        elif input_option == "3":
            new_last_watered = input("Enter new last watered date (YYYY-MM-DD):\n")
            if new_last_watered == "exit":
                continue
            elif re.match(r'^\d{4}-\d{2}-\d{2}$', new_last_watered):
                plant["last_watered"] = new_last_watered
                print("Last watered date updated.\n")
                continue
            else:
                print("Invalid date format, please use YYYY-MM-DD (e.g. 2026-03-15)\n")
                continue

        elif input_option == "4":
            new_water_interval_days = input("Enter new water interval in days:\n")
            if new_water_interval_days == "exit":
                continue
            elif new_water_interval_days.isdigit():
                plant["water_interval_days"] = int(new_water_interval_days)
                print("Water interval updated.\n")
                continue
            else:
                print("Invalid input, please enter a positive whole number (e.g. 7)\n")
                continue

        else:
            print("Invalid option, please choose 1-4.\n")
            continue


        
