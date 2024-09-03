# importing the csv module
import modules.csvdb as mydb

# my data rows as dictionary objects
dummy_data =[{'id': '1', 'user': 'user1', 'password': 'user1pwd'}]

mydb.saveData("data_files/users.csv", dummy_data, ["id","user","password"])
