#Import statements
import csv
import os
import random as rd
from random import randint

#Initialize the variables
cwdEmail = os.getcwd() + "\\EmailIdList.csv"
idList = []
emailList = []
combinedList=[]

#Define functions
def generateId():
    return str(random_with_N_digits())

def random_with_N_digits():
    range_start = 10**(8)
    range_end = (10**9)-1
    num = randint(range_start, range_end)
    if num in idList:
        num = random_with_N_digits()
    return num





with open(cwdEmail) as csvfile:
    promoreader = csv.reader(csvfile, delimiter=',')
    for row in promoreader:
        try:
            emailList.append(row[0])
            try:
                if row[1] == "":
                    idList.append(0)
                else:
                    idList.append(row[1])
            except:
                idList.append(0)
        except:
            pass
        

for i in range(len(emailList)):
    if int(idList[i]) == 0:
        idList[i] = generateId()


        
print (emailList)
print(idList)



for i in range(len(emailList)):
    #This prevents errors when editing the csv file in excel, where it would produce empty lines then give the empty lines an id number
    if (str(emailList[i]) != ""):
        combinedList.append([emailList[i], idList[i]])

print(combinedList)


with open(cwdEmail, "w") as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    for i in range(len(combinedList)):
       writer.writerow(combinedList[i])

        
    


