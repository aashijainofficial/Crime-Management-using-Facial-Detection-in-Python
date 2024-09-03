# importing the csv module
import modules.csvdb as mydb

# my data rows as dictionary objects
dummy_data =[{'id': '1', 'vehicle_no': '000000', 'vehicle_type': '', 'recovery_on' : '', 'recovery_status': '', 'handover_status': '', 'handover_on': ''},
		]




mydb.saveData("data_files/vehicle_recoveries.csv", dummy_data, ["id","vehicle_no","vehicle_type","recovery_on","recovery_status","handover_status","handover_on"])
