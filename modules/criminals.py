import modules.csvdb as mydb

file_name = "data_files/criminals.csv"

response_msg = {}

def list():
    rows = mydb.getData(file_name)
    return rows

def add(name, aadhaar_no, dob, address,	pic):
    global response_msg
    response_msg = {};

    if not name or not aadhaar_no :
        response_msg = {'status': 'error', 'msg': "name and aadhaar required."}
        return False
    
    #Not duplicate entry if user already in users csv
    if isRecordExist(name, aadhaar_no) :
        response_msg = {'status': 'error', 'msg': name + " already exist in our database."}
        return False

    rows = mydb.getData(file_name)

    newRecordNo = str(int(rows[len(rows)-1]['id']) + 1)
    item = {
        'id': newRecordNo, #increment 1 in last id
        'name': name,
        'dob': dob,
        'address': address,
        'aadhaar_no': aadhaar_no,
        'pic': pic
    }
    rows.append(item)

    #Save New Record in users csv    
    if mydb.saveData(file_name, rows, ["id","name","dob","address","aadhaar_no","pic"]) :
        response_msg = {'status': 'success', 'msg': "name register with us on registration no." + newRecordNo, 'item_inserted' : item}
        return True

    response_msg = {'status': 'error', 'msg': "data could not save in db on some reason"}
    return False

def delete(name, aadhaar_no):
    global response_msg
    response_msg = {};
    
    if not name or not aadhaar_no :
        response_msg = {'status': 'error', 'msg': "name and aadhaar no required."}
        return False

    rows = mydb.getData(file_name)
    rowsnew = []
    for row in rows :
        if row['name'] != name or row['aadhaar_no'] != aadhaar_no :
            rowsnew.append(row)        
        
    if rows != rowsnew and mydb.saveData(file_name, rowsnew, ["id","name","dob","address","aadhaar_no","pic"]) :
        response_msg = {'status': 'success', 'msg': "record successfully deleted"}
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
        
    if rows != rowsnew and mydb.saveData(file_name, rowsnew, ["id","name","dob","address","aadhaar_no","pic"]) :
        response_msg = {'status': 'success', 'msg': "record successfully deleted"}
        return True

    response_msg = {'status': 'error', 'msg': "data could not deleted in db on some reason or record not found"}
    return False



def get(aadhaar_no):
    global response_msg
    response_msg = {};
    if not name :
        return {'status': 'error', 'msg': "aadhaar_no required."}
    
    rows = mydb.getData(file_name)
    for row in rows :
        if row['aadhaar_no'] == aadhaar_no :
            return row
        
    response_msg = {'status': 'error', 'msg': "record not found in db"}    
    return False


def isValidUser(name, aadhaar_no) :
    global response_msg
    response_msg = {};
    if not name or not aadhaar_no :
        response_msg = {'status': 'error', 'msg': "name and aadhaar no. required."}
        return False

    rows = mydb.getData(file_name)
    for row in rows :
        if row['name'] == name and row['aadhaar_no'] == aadhaar_no :
            response_msg = {'status': 'success', 'msg': "valid user."}
            return True

    response_msg = {'status': 'error', 'msg': "not a valid user."} 
    return False


def isRecordExist(name, aadhaar_no):
    global response_msg
    response_msg = {};
    if not name or not aadhaar_no :
        response_msg = {'status': 'error', 'msg': "name and aadhaar no. required."}
        return False
    
    rows = mydb.getData(file_name)
    for row in rows :
        if row['name'] == name and row['aadhaar_no'] == aadhaar_no :
            return True
        
    return False
