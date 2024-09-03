import modules.vehicle_recoveries as thisObject


import os

def displayHeader(heading):
    print("********************************************************************")
    print("*                                                                  *")
    print("*                          " + heading + "                          *")
    print("*                                                                  *")
    print("********************************************************************")
    

while True :
    #os.system('cls')
    displayHeader("Vehicle Recoveries")
    
    print("1. List")
    print("2. Add New")
    print("3. Search Record")
    print("4. Change Status")
    print("5. Delete Record")
    print("type 0 if want to quit?")
    print()
    print()
    choice = input("Enter Choice:")
    choiceint = int(choice)
    if int(choiceint) == 0 :
        break

    if choiceint == 1 :
        print(thisObject.list())
        
    elif choiceint == 2:
        displayHeader("Add New Recovery")
        vehicle_no_input = input("Vehicle No:")
        vehicle_type_input = input("Vehicle Type:")
        print(thisObject.add(vehicle_no_input, vehicle_type_input))

    elif choiceint == 3:
        displayHeader("Search Record")
        vehicle_no_input = input("Vehicle No:")
        vehicle_type_input = input("Vehicle Type:")
        print(thisObject.get(vehicle_no_input, vehicle_type_input))

    elif choiceint == 4:
        displayHeader("Change Status")
        vehicle_no_input = input("Vehicle No:")
        vehicle_type_input = input("Vehicle Type:")
        vehicle_status_inputt = input("New Status:")
        print(thisObject.changeStatus(vehicle_no_input, vehicle_type_input, vehicle_status_inputt))

    elif choiceint == 5:
        displayHeader("Delete Record")
        vehicle_no_input = input("Vehicle No:")
        vehicle_type_input = input("Vehicle Type:")
        print(thisObject.delete(vehicle_no_input, vehicle_type_input))

        
    #input("Press Enter to continue...")
