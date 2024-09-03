import modules.csvdb as mydb
from datetime import datetime

# datetime object containing current date and time
#now = datetime.now()

file_name = "data_files/fir_general.csv"

fir_types = ["document lost", "lost", "theft", "fight", "murder", "kidnapping", "domestic violence", "molestation", "harrasment", "rape", "fraud"]

response_msg = {}

def list():
    rows = mydb.getData(file_name)
    return rows

def add(fir_type, description):
    global response_msg
    response_msg = {};
    
    if not fir_type or not description :
        response_msg = {'status': 'error', 'msg': "fir type and description required."}
        return False

    if not fir_type in fir_types :
        response_msg = {'status': 'error', 'msg': "invalid type. allowed types are: " + ','.join(fir_types)}
        return False
    
    rows = mydb.getData(file_name)

    for row in rows :
        if row['fir_type'] == fir_type and row['description'] == description :
            response_msg = {'status': 'error', 'msg': "complaint already register with us on complaint no." + row['id']}
            return False

    newRecordNo = str(int(rows[len(rows)-1]['id']) + 1)
    item = {
        'id': newRecordNo, #increment 1 in last id
        'fir_type': fir_type,
        'description': description,
        'complaint_on' : datetime.now(),
        'complaint_status' : 'pending',
        'complaint_completed_on' : '',
        'complaint_response' : ''
    }
    rows.append(item)

    #Save New Record in users csv    
    if mydb.saveData(file_name, rows, ["id","fir_type","description","complaint_on","complaint_status","complaint_completed_on","complaint_response"]) :
        response_msg = {'status': 'success', 'msg': "complaint register in db at complaint no." + newRecordNo}
        return True

    response_msg = {'status': 'error', 'msg': "data could not save in db on some reason"}
    return False

def delete(fir_no):
    global response_msg
    response_msg = {};
    
    if not fir_no :
        response_msg = {'status': 'error', 'msg': "fir no. required."}
        return False
    
    rows = mydb.getData(file_name)
    rowsnew = []
    for row in rows :
        if row['id'] != fir_no :
            rowsnew.append(row)        
        
    if rows != rowsnew and mydb.saveData(file_name, rowsnew, ["id","fir_type","description","complaint_on","complaint_status","complaint_completed_on","complaint_response"]) :
        response_msg = {'status': 'success', 'msg': "record deleted successfully"}
        return True

    response_msg = {'status': 'error', 'msg': "data could not delete from db on some reason"}
    return False    
    

def get(fir_no):
    global response_msg
    response_msg = {};
    
    if not fir_no :
        response_msg = {'status': 'error', 'msg': "fir no. required."}
        return False

    rows = mydb.getData(file_name)
    for row in rows :
        if row['id'] == fir_no :
            return row

    response_msg = {'status': 'error', 'msg': "fir not found in db"}    
    return False


def changeStatus(fir_no, newstatus) :
    global response_msg
    response_msg = {};
    
    if not fir_no or not newstatus :
        response_msg = {'status': 'error', 'msg': "fir no and new status required."}
        return False

    rows = mydb.getData(file_name)
    for row in rows :
        if row['id'] == fir_no :
            row['complaint_status'] = newstatus
            if mydb.saveData(file_name, rows, ["id","fir_type","description","complaint_on","complaint_status","complaint_completed_on","complaint_response"]) :
                response_msg = {'status': 'success', 'msg': "status changed successfully in db"}
                return True

    response_msg = {'status': 'error', 'msg': "status could not change in db on some reason"}
    return False
