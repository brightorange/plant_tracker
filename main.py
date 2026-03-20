import add_plants
import view_plants
import remove_plants
import edit_plant
import load_data
import water_plants

plant_list = []

while True:
    menu_option = input('''
    Please choose an option:
    1. Add plants
    2. View plants
    3. Remove plants
    4. Edit plant
    5. Water plants!
    6. View summary
    7. Load dummy data from file
    8. Exit
    ''')
    
    if menu_option == "1":
        plant_list = add_plants.add_plants(plant_list)

    elif menu_option == "2":
        while True:
            result = view_plants.view_plants_menu(plant_list)
            if not result["continue"]:
                break
            print(result["output"])

    elif menu_option == "3":
        plant_list = remove_plants.remove_plants(plant_list)

    elif menu_option == "4":
        plant_list = edit_plant.edit_plant(plant_list)

    elif menu_option == "5":
        plant_list = water_plants.water_plants(plant_list)

    elif menu_option == "6":
        print(view_plants.summary(plant_list))

    elif menu_option == "7":
        plant_list = load_data.load_data(plant_list)

    elif menu_option == "8":
        print("Exiting the program\n")
        break

    else:
        print("Invalid option, please choose again\n")