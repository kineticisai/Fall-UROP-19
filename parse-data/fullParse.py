from parse import parse_file
import csv

#create a new csv file
f = open("data.csv", "x")

with open('data.csv', mode='w') as data:
    data_writer = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

def parseAll(init, final):
    while init < final:
        #my code has the folder named 2003copy, replace with your folder name

        #count the bnumber of files that dont return a full array
        file = "2003copy/0"+str(init)
        row = parse_file(file)
        data_writer.writerow(row)
        init += 1
    return

firstFile = 301001
lastFile = 304271
parseAll(firstFile, lastFile)
print("done")
