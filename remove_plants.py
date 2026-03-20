def remove_plants(plant_list):
    """Prompt for a plant name and remove it from plant_list.

    Loops until the user enters 'exit' to return to the main menu.
    Mutates plant_list in place and returns it when exiting.
    """
    while True:
        plant_name = input("Enter the name of the plant to remove, or 'exit' to go back:\n")
        if plant_name.lower() == "exit":
            return plant_list
        for plant in plant_list:
            if plant["name"] == plant_name:
                plant_list.remove(plant)
                print(f"Plant '{plant_name}' removed successfully.\n")
                break
        else:
            print(f"No plant named '{plant_name}' found.\n")
