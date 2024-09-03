import modules.csvdb as mydb
from datetime import datetime

# datetime object containing current date and time
#now = datetime.now()

file_name = "data_files/vehicle_thefts.csv"

vehicle_types = ["car", "jeep", "bus", "bike", "moped", "scooty", "bicycle", "rickshaw", "auto", "scooter", "truck"]

response_msg = {}

def list():
    rows = mydb.getData(file_name)
    return rows

def add(vehicle_no, vehicle_type):
    global response_msg
    response_msg = {};
    
    if not vehicle_no or not vehicle_type :
        response_msg = {'status': 'error', 'msg': "vehicle no and vehicle type required."}
        return False

    if not vehicle_type in vehicle_types :
        response_msg = {'status': 'error', 'msg': "invalid vehicle type. allowed types are: " + ','.join(vehicle_types)}
        return False
    
    rows = mydb.getData(file_name)

    for row in rows :
        if row['vehicle_no'] == vehicle_no and row['vehicle_type'] == vehicle_type :
            response_msg = {'status': 'error', 'msg': "complaint already register with us on complaint no." + row['id']}
            return False

    newRecordNo = str(int(rows[len(rows)-1]['id']) + 1)
    item = {
        'id': newRecordNo, #increment 1 in last id
        'vehicle_no': vehicle_no,
        'vehicle_type': vehicle_type,
        'complaint_on' : datetime.now(),
        'complaint_status' : 'pending'
    }
    rows.append(item)

    #Save New Record in users csv    
    if mydb.saveData(file_name, rows, ["id","vehicle_no","vehicle_type","complaint_on","complaint_status"]) :
        response_msg = {'status': 'success', 'msg': "complaint register with us on complaint no." + newRecordNo, 'item_inserted' : item}
        return True
    
    response_msg = {'status': 'error', 'msg': "data could not save in db on some reason"}
    return False

def delete(vehicle_no, vehicle_type):
    global response_msg
    response_msg = {};
    
    if not vehicle_no or not vehicle_type :
        response_msg = {'status': 'error', 'msg': "vehicle no and vehicle type required."}
        return False

    if not vehicle_type in vehicle_types :
        response_msg = {'status': 'error', 'msg': "invalid vehicle type. allowed types are: " + ','.join(vehicle_types)}
        return False
    
    rows = mydb.getData(file_name)
    rowsnew = []
    for row in rows :
        if row['vehicle_no'] != vehicle_no or row['vehicle_type'] != vehicle_type :
            rowsnew.append(row)        
        
    if rows != rowsnew and mydb.saveData(file_name, rowsnew, ["id","vehicle_no","vehicle_type","complaint_on","complaint_status"]) :
        response_msg = {'status': 'success', 'msg': "recovery successfully deleted"}
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
        
    if rows != rowsnew and mydb.saveData(file_name, rowsnew, ["id","vehicle_no","vehicle_type","complaint_on","complaint_status"]) :
        response_msg = {'status': 'success', 'msg': "recovery successfully deleted"}
        return True

    response_msg = {'status': 'error', 'msg': "data could not deleted in db on some reason or record not found"}
    return False
    

def get(vehicle_no, vehicle_type):
    global response_msg
    response_msg = {};
    
    if not vehicle_no or not vehicle_type :
        response_msg = {'status': 'error', 'msg': "vehicle no and vehicle type required."}
        return False

    if not vehicle_type in vehicle_types :
        response_msg = {'status': 'error', 'msg': "invalid vehicle type. allowed types are: " + ','.join(vehicle_types)}
        return False

    rows = mydb.getData(file_name)
    for row in rows :
        if row['vehicle_no'] == vehicle_no and row['vehicle_type'] == vehicle_type :
            return row
        
    response_msg = {'status': 'error', 'msg': "vehicle not found in db"}    
    return False


def isRecordExist(vehicle_no, vehicle_type) :
    global response_msg
    response_msg = {};
    
    if not vehicle_no or not vehicle_type :
        response_msg = {'status': 'error', 'msg': "vehicle no and vehicle type required."}
        return False

    if not vehicle_type in vehicle_types :
        response_msg = {'status': 'error', 'msg': "invalid vehicle type. allowed types are: " + ','.join(vehicle_types)}
        return False

    rows = mydb.getData(file_name)
    for row in rows :
        if row['vehicle_no'] == vehicle_no and row['vehicle_type'] == vehicle_type :
            return True
        
    response_msg = {'status': 'error', 'msg': "vehicle not found in db"}    
    return False

def changeStatus(vehicle_no, vehicle_type, newstatus) :
    global response_msg
    response_msg = {};
    
    if not vehicle_no or not vehicle_type or not newstatus :
        response_msg = {'status': 'error', 'msg': "vehicle no and vehicle type required."}
        return False

    if not vehicle_type in vehicle_types :
        response_msg = {'status': 'error', 'msg': "invalid vehicle type. allowed types are: " + ','.join(vehicle_types)}
        return False
    
    rows = mydb.getData(file_name)
    for row in rows :
        if row['vehicle_no'] == vehicle_no and row['vehicle_type'] == vehicle_type :
            row['complaint_status'] = newstatus
            if mydb.saveData(file_name, rows, ["id","vehicle_no","vehicle_type","complaint_on","complaint_status"]) :
                response_msg = {'status': 'success', 'msg': "status changed successfully in db"}
                return True

    response_msg = {'status': 'error', 'msg': "status could not change in db on some reason"}
    return False
