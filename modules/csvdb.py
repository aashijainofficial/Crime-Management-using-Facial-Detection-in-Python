import csv

def getData(filename):
    # initializing the titles and rows list
    fields = []
    rows = []

    # reading csv file
    with open(filename, 'r', newline='') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)

            # extracting field names through first row
            fields = next(csvreader)
			
            # extracting each data row one by one
            for row in csvreader:
                    colindex = 0;
                    item = {}
                    for col in row:
                            item[fields[colindex]] = col
                            colindex += 1
				
                    rows.append(item)
    return rows



def saveData(filename, data,  fileds=[]) :
    # writing to csv file
    with open(filename, 'w', newline='') as csvfile:
            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames = fileds)
            
            # writing headers (field names)
            writer.writeheader()
            
            # writing data rows
            writer.writerows(data)

    return True
