import modules.fir_general as fir
import modules.vehicle_thefts as vehicle_thefts
import modules.vehicle_recoveries as vehicle_recoveries
import modules.users as user
import os

superAdminPwd = 'india@top'

adminLogin = False
superAdminLogin = False

def displayHeader(heading):
    print("********************************************************************")
    print("*                                                                  *")
    print("*                          " + heading + "                          *")
    print("*                                                                  *")
    print("********************************************************************")


def printMsg(msg):
    print("==============================================================================================================================================") 
    print(msg)
    print("==============================================================================================================================================") 
    

def printTable(myDict, colList=None):
   """ Pretty print a list of dictionaries (myDict) as a dynamically sized table.
   If column names (colList) aren't specified, they will show in random order.
   Author: Thierry Husson - Use it as you want but don't blame me.
   """
   if not colList: colList = list(myDict[0].keys() if myDict else [])
   myList = [colList] # 1st row = header
   for item in myDict: myList.append([str(item[col] if item[col] is not None else '') for col in colList])
   colSize = [max(map(len,col)) for col in zip(*myList)]
   formatStr = ' | '.join(["{{:<{}}}".format(i) for i in colSize])
   myList.insert(1, ['-' * i for i in colSize]) # Seperating line
   for item in myList: print(formatStr.format(*item))
    

def printUserList(dict1):
    print ("{:<10} {:<10} {:<10}".format('ID', 'User', 'Password'))
    print("======================================") 
    for row in dict1 :
        print ("{:<10} {:<10} {:<10}".format(row['id'], row['user'], row['password']))
    
    print("======================================") 

def printVehicleRecoveriesList(dict1):
    print ("{:<10} {:<15} {:<15} {:<30} {:<15} {:<15} {:<15}".format("ID","Vehicle No","Vehicle Type","Recovery Date","Recovery Status","Handover Status","Handover Date"))
    print("==============================================================================================================================================") 
    for row in dict1 :
        print ("{:<10} {:<15} {:<15} {:<30} {:<15} {:<15} {:<15}".format(row['id'], row['vehicle_no'], row['vehicle_type'], row['recovery_on'], row['recovery_status'], row['handover_status'], row['handover_on']))
    
    print("==============================================================================================================================================")

def printVehicleTheftList(dict1):
    print ("{:<10} {:<15} {:<15} {:<30} {:<15}".format("ID","Vehicle No","Vehicle Type","Complaint Date","Complaint Status"))
    print("==============================================================================================================================================") 
    for row in dict1 :
        print ("{:<10} {:<15} {:<15} {:<30} {:<15}".format(row['id'], row['vehicle_no'], row['vehicle_type'], row['complaint_on'], row['complaint_status']))
    
    print("==============================================================================================================================================")

while True :
    #os.system('cls') #not working
    displayHeader("ONLINE CRIME RECORD MANAGEMENT")
    
    print("1.  File FIR General")
    print("2.  File FIR Vehicle Theft")
    print("3.  Check FIR Status of Vehicle Theft")
    print("4.  List - FIR")
    print("5.  List - Vehicle Theft")
    print("6.  List - Vehicle Recoveries ");
    if not adminLogin :
        print("7.  Login");
    if adminLogin :
        print("7.  Logout");
        print("8.  Change FIR Status");
        print("9.  Vehicle Recoveries - Add");
        print("10. Vehicle Recoveries - Delete");
        print("11. Change Password");

    if superAdminLogin:
        print("12. List - USER");
        print("13. Create New User");
    print("type 0 if want to quit?")
    print()
    print()
    choice = input("Enter Choice:")
    try:
        choiceint = int(choice)
    except ValueError:
        print("Enter choice not an int!")
        continue

    choiceint = int(choice)
    if choiceint == 0 :
        break

    if not adminLogin and choiceint > 7 :
        print("Invalid Choice Select [1-7]")
        continue

    elif adminLogin and not superAdminLogin and choiceint > 11 :
        print("Invalid Choice Select [1-11]")
        continue

    elif superAdminLogin and choiceint > 13 :
        print("Invalid Choice Select [1-13]")
        continue
        
    if choiceint == 1 :
        displayHeader("FIR General")
        fir_type_input = input("FIR Type:")
        description = input("Description (max:100 char):")
        result = fir.add(fir_type_input.strip().lower(), description.strip().lower() )
        res = bool(fir.response_msg)
        if res :
            printMsg("SYSTEM " + fir.response_msg['status'].upper() + " : " + fir.response_msg['msg'])
        
    elif choiceint == 2:
        displayHeader("FIR for Vehicle Theft")
        vehicle_no_input = input("Vehicle No:")
        vehicle_type_input = input("Vehicle Type:")
        result = vehicle_thefts.add(vehicle_no_input.strip().lower(), vehicle_type_input.strip().lower())
        res = bool(vehicle_thefts.response_msg)
        if res :
            printMsg("SYSTEM " + vehicle_thefts.response_msg['status'].upper() + " : " + vehicle_thefts.response_msg['msg'])
        
    elif choiceint == 3:
        displayHeader("Check FIR Status")
        vehicle_no_input = input("Vehicle No:")
        vehicle_type_input = input("Vehicle Type:")
        result = vehicle_thefts.get(vehicle_no_input.strip().lower(), vehicle_type_input.strip().lower())
        res = bool(vehicle_thefts.response_msg)
        if res :
            printMsg("SYSTEM " + vehicle_thefts.response_msg['status'].upper() + " : " + vehicle_thefts.response_msg['msg'])
        else :
            print(result)
    elif choiceint == 4 :
        printTable(fir.list())

    elif choiceint == 5 :
        printTable(vehicle_thefts.list())
        #printVehicleTheftList(vehicle_thefts.list())
        #print(vehicle_thefts.list())

    elif choiceint == 6 :
        printTable(vehicle_recoveries.list())
        #printVehicleRecoveriesList(vehicle_recoveries.list())
        #print(vehicle_recoveries.list())

    elif choiceint == 7 :
        if not adminLogin:
            username = input("User:")
            pwd = input("Password:")

            if username == 'superadmin' and pwd == superAdminPwd :
                result = True
                superAdminLogin = True
            else :
                result = user.isValidUser(username.strip(), pwd.strip())
            if not result :
                print("Invalid User. Please Fill Proper Details")
                if user.response_msg != '' :
                    print("Error:" + str(user.response_msg))
            else :
                print("Successfully Login")
                adminLogin = True
                loggedUser = username
                loggedUserPwd = pwd
        else:
            superAdminLogin = False
            adminLogin = False
            loggedUser = ''
            loggedUserPwd = ''
            print("Successfully Logout")

    elif choiceint == 8:
        displayHeader("Change Status")
        vehicle_no_input = input("Vehicle No:")
        vehicle_type_input = input("Vehicle Type:")
        vehicle_status_input = input("New Status:")
        result = vehicle_thefts.changeStatus(vehicle_no_input.strip().lower(), vehicle_type_input.strip().lower(), vehicle_status_input.strip().lower())
        res = bool(vehicle_thefts.response_msg)
        if res :
            printMsg("SYSTEM " + vehicle_thefts.response_msg['status'].upper() + " : " + vehicle_thefts.response_msg['msg'])

    elif choiceint == 9 :
        displayHeader("New Vehicle Recovery")
        vehicle_no_input = input("Vehicle No:")
        vehicle_type_input = input("Vehicle Type:")
        result = vehicle_recoveries.add(vehicle_no_input.strip().lower(), vehicle_type_input.strip().lower())    
        res = bool(vehicle_recoveries.response_msg)
        if res :
            printMsg("SYSTEM " + vehicle_recoveries.response_msg['status'].upper() + " : " + vehicle_recoveries.response_msg['msg'])

        if result :
            #check in compalint if same vehicle register
            isVehicleExistInVehicleTheftComplaint = vehicle_thefts.isRecordExist(vehicle_no_input, vehicle_type_input)
            print("Is Record Exist In Vehicle Complaint:", end =" ")
            print(isVehicleExistInVehicleTheftComplaint)
            if isVehicleExistInVehicleTheftComplaint :
                result = vehicle_thefts.changeStatus(vehicle_no_input, vehicle_type_input, 'recovered')
                print('Status Changed in vehicle_thefts dataset: ', end =" ")
                print(result)
                
    elif choiceint == 10:
        displayHeader("Delete Record")
        vehicle_no_input = input("Vehicle No:")
        vehicle_type_input = input("Vehicle Type:")
        result = vehicle_recoveries.delete(vehicle_no_input.strip().lower(), vehicle_type_input.strip().lower())
        res = bool(vehicle_recoveries.response_msg)
        if res :
            printMsg("SYSTEM " + vehicle_recoveries.response_msg['status'].upper() + " : " + vehicle_recoveries.response_msg['msg'])

    elif choiceint == 11:
        displayHeader("Change Your Password")
        if superAdminLogin :
            username = input("User:")
            pwd = input("Password:")
            npwd = input("New Password:")
        elif adminLogin :
            username = loggedUser
            pwd = loggedUserPwd
            npwd = input("New Password:")
        result = user.changePassword(username.strip(), pwd.strip(), npwd.strip())
        res = bool(user.response_msg)
        if res :
            printMsg("SYSTEM " + user.response_msg['status'].upper() + " : " + user.response_msg['msg'])

    elif choiceint == 12:
        #displayHeader("User List")
        printTable(user.list())
        #printUserList(user.list())
        #print(user.list())

    elif choiceint == 13:
        displayHeader("Create New Admin User")
        username = input("User:")
        pwd = input("Password:")
        result = user.add(username.strip(), pwd.strip())
        res = bool(user.response_msg)
        if res :
            printMsg("SYSTEM " + user.response_msg['status'].upper() + " : " + user.response_msg['msg'])


    input("Press any key to continue..")
