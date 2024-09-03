import modules.csvdb as mydb

file_name = "data_files/users.csv"

response_msg = {}

def list():
    rows = mydb.getData(file_name)
    return rows

def add(user, password):
    global response_msg
    response_msg = {};
    if user == 'superadmin' :
        response_msg = {'status': 'error', 'msg': "superadmin user not allowed in system."}
        return False
        
    if not user or not password :
        response_msg = {'status': 'error', 'msg': "username and password required."}
        return False
    
    #Not duplicate entry if user already in users csv
    if isUserExist(user) :
        response_msg = {'status': 'error', 'msg': user + " already exist in our database. please login with your credentials"}
        return False

    rows = mydb.getData(file_name)

    newRecordNo = str(int(rows[len(rows)-1]['id']) + 1)
    item = {
        'id': newRecordNo, #increment 1 in last id
        'user': user,
        'password': password
    }
    rows.append(item)

    #Save New Record in users csv    
    if mydb.saveData(file_name, rows, ["id","user","password"]) :
        response_msg = {'status': 'success', 'msg': "user register with us on registration no." + newRecordNo, 'item_inserted' : item}
        return True

    response_msg = {'status': 'error', 'msg': "data could not save in db on some reason"}
    return False

def delete(user, password):
    global response_msg
    response_msg = {};
    
    if not user or not password :
        response_msg = {'status': 'error', 'msg': "user and password required."}
        return False

    rows = mydb.getData(file_name)
    rowsnew = []
    for row in rows :
        if row['user'] != user or row['password'] != password :
            rowsnew.append(row)        
        
    if rows != rowsnew and mydb.saveData(file_name, rowsnew, ["id","user","password"]) :
        response_msg = {'status': 'success', 'msg': "user successfully deleted"}
        return True

    response_msg = {'status': 'error', 'msg': "data could not deleted in db on some reason or record not found"}
    return False

def deleteByID(id):
    global response_msg
    response_msg = {};
    
    if not id :
        response_msg = {'status': 'error', 'msg': "id required."}
        return False
    
    rows = mydb.getData(file_name)
    rowsnew = []
    for row in rows :
        if row['id'] != id :
            rowsnew.append(row)        
        
    if rows != rowsnew and mydb.saveData(file_name, rowsnew, ["id","user","password"]) :
        response_msg = {'status': 'success', 'msg': "recovery successfully deleted"}
        return True

    response_msg = {'status': 'error', 'msg': "data could not deleted in db on some reason or record not found"}
    return False



def get(user):
    global response_msg
    response_msg = {};
    if not user :
        return {'status': 'error', 'msg': "username required."}
    
    rows = mydb.getData(file_name)
    for row in rows :
        if row['user'] == user :
            return row
        
    response_msg = {'status': 'error', 'msg': "user not found in db"}    
    return False


def changePassword(user, currentpwd, newpwd) :
    global response_msg
    response_msg = {};
    if not user or not currentpwd or not newpwd :
        response_msg = {'status': 'error', 'msg': "username, password and new password required."}
        return False

    
    rows = mydb.getData(file_name)
    for row in rows :
        if row['user'] == user and row['password'] == currentpwd :
            row['password'] = newpwd
            if mydb.saveData(file_name, rows, ["id","user","password"]) :
                response_msg = {'status': 'success', 'msg': "password changed successfully"}
                return True

    response_msg = {'status': 'error', 'msg': "password could not change due to passed values not matched"}
    return False

def isValidUser(user, password) :
    global response_msg
    response_msg = {};
    if not user or not password :
        response_msg = {'status': 'error', 'msg': "username and password required."}
        return False

    rows = mydb.getData(file_name)
    for row in rows :
        if row['user'] == user and row['password'] == password :
            response_msg = {'status': 'success', 'msg': "valid user."}
            return True

    response_msg = {'status': 'error', 'msg': "not a valid user."} 
    return False


def isUserExist(user):
    global response_msg
    response_msg = {};
    if not user :
        response_msg = {'status': 'error', 'msg': "username required."}
        return False
    
    rows = mydb.getData(file_name)
    for row in rows :
        if row['user'] == user :
            return True
        
    return False
