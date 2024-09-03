import modules.users as user


import os

def displayHeader(heading):
    print("********************************************************************")
    print("*                                                                  *")
    print("*                          " + heading + "                          *")
    print("*                                                                  *")
    print("********************************************************************")
    

while True :
    #os.system('cls')
    displayHeader("User Dashboard")
    
    print("1. List")
    print("2. Add New")
    print("3. Search User")
    print("4. Change Password")
    print("5. Validate User")
    print("type 0 if want to quit?")
    print()
    print()
    choice = input("Enter Choice:")
    choiceint = int(choice)
    if choiceint == 0 :
        break

    if choiceint == 1 :
        print(user.list())
        
    elif choiceint == 2:
        displayHeader("Add New User")
        user_input = input("User:")
        pwd_input = input("Password:")
        print(user.add(user_input, pwd_input))

    elif choiceint == 3:
        displayHeader("Search User")
        user_input = input("User:")
        print(user.get(user_input))

    elif choiceint == 4:
        displayHeader("Change Password")
        user_input = input("User:")
        pwd_input = input("Password:")
        pwd_new_input = input("New Password:")
        print(user.changePassword(user_input, pwd_input, pwd_new_input))

    elif choiceint == 5:
        displayHeader("Validate User")
        user_input = input("User:")
        pwd_input = input("Password:")
        print(user.isValidUser(user_input, pwd_input))

    #input("Press Enter to continue...")
