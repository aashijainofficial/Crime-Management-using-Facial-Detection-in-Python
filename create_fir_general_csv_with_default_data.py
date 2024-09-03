# importing the csv module
import modules.csvdb as mydb

# my data rows as dictionary objects
dummy_data =[{'id': '1', 'fir_type': 'NULL', 'description': '', 'complaint_on' : '', 'complaint_status': '', 'complaint_completed_on' : '', 'complaint_response': ''},
		]


mydb.saveData("data_files/fir_general.csv", dummy_data, ["id","fir_type","description","complaint_on","complaint_status","complaint_completed_on","complaint_response"])
