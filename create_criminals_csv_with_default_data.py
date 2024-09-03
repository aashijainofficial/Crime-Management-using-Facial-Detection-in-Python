# importing the csv module
import modules.csvdb as mydb

# my data rows as dictionary objects
dummy_data =[{'id': '1', 'name': '', 'dob': '', 'address' : '', 'aadhaar_no': '', 'pic' : ''},
		]



mydb.saveData("data_files/criminals.csv", dummy_data, ["id","name","dob","address","aadhaar_no","pic"])
