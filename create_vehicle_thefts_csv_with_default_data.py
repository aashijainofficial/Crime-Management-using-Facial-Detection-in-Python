# importing the csv module
import modules.csvdb as mydb

# my data rows as dictionary objects
dummy_data =[{'id': '1', 'vehicle_no': '000000', 'vehicle_type': '', 'complaint_on' : '', 'complaint_status': ''},
		]



mydb.saveData("data_files/vehicle_thefts.csv", dummy_data, ["id","vehicle_no","vehicle_type","complaint_on","complaint_status"])
