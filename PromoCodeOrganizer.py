#Import statements
import csv
import os
import os.path
from os.path import join as pjoin
import matplotlib.pyplot as plt
import numpy as np
import json
import random
from firebase import firebase
from firebase.firebase import FirebaseApplication

#Link to the firebase database
#https://console.firebase.google.com/u/0/project/bloody-76f85/database/bloody-76f85/data/


#Creates a list of num size filled with randomly generated hexadecimal colors
def randomColor(num):
    for i in num:
        tempColor = ""
        for i in range(6):
            tempColor = tempColor + random.choice(hexColorPool)
        colorList.append('#' + tempColor)
    return colorList


#Adds the points from the amazon file to the corresponding individual in the PointData file
def addPoints():
    
    #Initializes all the variables in this function
    cwdAmazon = os.getcwd() + "\\amazonpromo.csv"
    cwdPointData = os.getcwd() + "\\pointdata.csv"
    cwdGroupList = os.getcwd() + "\\GroupList.csv"
    priceCol = 2
    promoCol = 3
    nameCol = 4
    idList = []
    promoIdCounter = []
    promoName = []
    promoDate = []
    dateBool = True
    firstDate = ""
    lastDate = ""
    startYear = ""
    endYear = ""
    rowOneBool = True
    colorList = []
    hexColorPool = ['a', 'b', 'c', 'd', 'e', 'f', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    tempColor = ''
    totalSale = []
    promoName2 = []
    pointList = []
    pointDataIdName = []
    url = "https://bloody-76f85.firebaseio.com/"
    userIdList = []
    addedPoints = []
    currentPoints = []
    currentIdNames = []

    #Creates the idList for the different promo codes and gets the range of the dates
    with open(cwdAmazon) as csvfile:
        promoreader = csv.reader(csvfile, delimiter=',')

        for row in promoreader:
            if rowOneBool:
                rowOneBool = False
            else:
                if dateBool:
                    lastDate = str(row[0][5:10])
                    endYear = str(row[0][2:4])
                    dateBool = False

                if row[3] not in idList:
                    #if 'US Core Free Shipping Promotion, based off Policies' != row[4] and "Amazon" not in row[4] and "Next" not in row[4]:
                    if 'A.P.' in row[4]:
                        idList.append(row[3])


                firstDate = str(row[0][5:10])
                startYear = str(row[0][2:4])

        #Initializes the empty lists to be filled with data
        for i in range(len(idList)):
            promoIdCounter.append(0)
            promoName.append('')
            promoName2.append('')
            promoDate.append([])
            totalSale.append(float(0))
            pointList.append(float(0))


    #Fills in the empty lists that were created in the previous with open statement

    with open(cwdAmazon) as csvfile:
        promoreader = csv.reader(csvfile, delimiter=',')

        for row in promoreader:

            if not rowOneBool:
                rowOneBool = not rowOneBool

            else:
                for i in range(len(idList)):
                    if (idList[i] == row[promoCol]):
                        promoIdCounter[i] += 1
                        promoName[i] = row[nameCol]
                        promoName2[i] = row[nameCol]
                        promoDate[i].append(row[0][5:10])
                        totalSale[i] = totalSale[i] + float(row[2])

                        if row[nameCol][8] == '1':
                            pointList[i] += 5
                        else:
                            pointList[i] = pointList[i] + 10

    #Divides all of the point totals by the amount of people in that group
    for i in range(len(promoName)):
        pointList[i] = pointList[i] / int(promoName[i][8])



    '''
    Gonna make the name scheme of each affiliated influencer code:
    "A.P. 15% (#) - Name"
    where # is the number of people in the group (1 for solo), and Name is the group/solo name.
    Can add up and divide the points between the members of the group automatically
    Character 8 for number
    5  points per sale for solo
    10 points per sale for group, then divided between the number of members
    '''





    #Print statements for debugging (and to look cool)
    '''
    for i in range(len(idList)):
        print(promoName[i] + "\nCounter: " + str(promoIdCounter[i]))
        print(promoDate[i])
        print('\n')
    '''



    #Formats the dates and creates the new text file name
    firstDate = firstDate.replace("-", " ")
    lastDate = lastDate.replace("-", " ")
    fileName = startYear + "-" + endYear + "-" + firstDate + "-" + lastDate +".txt"


    #Checks if the file exists already, if it does then don't add any more points
    if (not os.path.exists(os.getcwd() + "\\Stored Data\\" + fileName)):
        
        fileName = (os.getcwd() + "\\Stored Data\\" + fileName)
        file = open(fileName, "w")
        


        #Creates the file and writes the information onto the text file
        for i in range(len(idList)):
            file.write(str(promoName[i]))

            if (promoIdCounter[i] == 1):
                file.write("\nUsed " + str(promoIdCounter[i]) + " time")

            else:
                file.write("\nUsed " + str(promoIdCounter[i]) + " times")

            file.write("\nDates Used: "+str(promoDate[i]))
            file.write("\nTotal Amount Saved: "+str(totalSale[i]))
            file.write("\nNumber of points per person: " + str(pointList[i]))
            file.write('\n\n\n')
        file.close()

        ##print(promoName)
        ##print(pointList)



        #Reads the groupList file and adds all the data to a list, and adds the points per person from the amazon data
        with open(cwdGroupList) as csvfile:
            groupreader = csv.reader(csvfile, delimiter=',')

            for row in groupreader:

                for i in range(len(promoName)):

                    if(row[0] == promoName[i]):
                        #if(int(promoName[i][8]) > 1):
                        tempList = row[1].split('-')
                        for item in tempList:
                            userIdList.append(item)
                        for j in range(len(tempList)):
                            addedPoints.append(pointList[i])
                     
                        #else:
                            #userIdList.append(row[1])
                            #addedPoints.append(pointList[i])


        #Opens the point data file and reads all of the current values
        with open(cwdPointData) as csvfile:
            groupreader = csv.reader(csvfile, delimiter=',')

            for row in groupreader:
                try:
                    currentIdNames.append(row[0])
                    currentPoints.append(row[1])
                except:
                    pass

        for i in range(len(userIdList)):

            if userIdList[i] not in currentIdNames:
                currentIdNames.append(userIdList[i])
                currentPoints.append(addedPoints[i])

            else:
                currentPoints[currentIdNames.index(userIdList[i])] = float(currentPoints[currentIdNames.index(userIdList[i])]) + float(addedPoints[i])


        #Adds all the new data to the old data and writes it to PointData
        with open(cwdPointData, 'w') as csvfile:
            groupwriter = csv.writer(csvfile, delimiter=',')
            for i in range(len(currentIdNames)):
                combinedCurrentList = []
                combinedCurrentList.append(currentIdNames[i])
                combinedCurrentList.append(currentPoints[i])
                groupwriter.writerow(combinedCurrentList)
    else:
        print("This months points have already been added.")

#This pushes all of the information in pointData to the firebase database
def updateFB():
    url = "https://bloody-76f85.firebaseio.com/"
    fb = firebase.FirebaseApplication(url, None)
    cwdPointData = os.getcwd() + "\\pointdata.csv"
    pointDataIdName = []
    addedPoints = []
    
    #Appends the IDs and the points for that ID to the firebase database
    with open(cwdPointData) as csvfile:
        promoreader = csv.reader(csvfile, delimiter=',')
        for row in promoreader:
            try:
                pointDataIdName.append(row[0])
                addedPoints.append(row[1])
            except:
                pass


    #Uploads the information to firebase
    for i in range(len(pointDataIdName)):
        data = {'Points':float(addedPoints[i])}
        result = fb.patch('/Users/' + pointDataIdName[i] + '/', data)



def graphData():
    for i in range(len(promoName)):
        promoName[i] = promoName[i][:15]



    index = np.arange(len(idList))
    randomColor(index)


    #Creates the barchart of the number of sales
    for i in range(len(promoName)):
        promoName[i] = promoName[i] + " - $" + str(totalSale[i])
    plt.figure(1)
    plt.bar(index, promoIdCounter, color = colorList)
    plt.xlabel('Promotion Name', fontsize=15)
    plt.ylabel("Number of Sales", fontsize=15)
    plt.tick_params(axis="both", which="both", bottom=False, top=False,
                    labelbottom=True, left=False, right=False, labelleft=True)
    if (len(index) < 5):
        plt.xticks(index, promoName, fontsize = 10, rotation=15)
    elif (len(index) > 5 and len(index) < 10):
        plt.xticks(index, promoName, fontsize = 7, rotation=15)
    else:
        plt.xticks(index, promoName, fontsize = 6, rotation=20)
    plt.title(firstDate + " - " + lastDate + " Total Number of Sales", fontsize = 20)
    plt.grid(color='#000000', which='major', axis='y', alpha= .08)
    plt.tight_layout()
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')
    



    #Creates the barchart of the amount saved
    for i in range(len(promoName2)):
        promoName2[i] = promoName2[i] + " - " + str(totalSale[i])
    plt.figure(2)
    plt.bar(index, totalSale, color = colorList)
    plt.xlabel("Promotion Name", fontsize=15)
    plt.ylabel("Total Amount Saved ($)", fontsize=15)
    plt.tick_params(axis="both", which="both", bottom=False, top=False,
                    labelbottom=True, left=False, right=False, labelleft=True)
    if (len(index) < 5):
        plt.xticks(index, promoName2, fontsize = 10, rotation=15)
    elif (len(index) > 5 and len(index) < 10):
        plt.xticks(index, promoName2, fontsize = 7, rotation=15)
    else:
        plt.xticks(index, promoName2, fontsize = 4, rotation=20)
    plt.title(firstDate + " - " + lastDate + " Total Amount Saved per Promo", fontsize = 20)
    plt.grid(color='#000000', which='major', axis='y', alpha= .25)
    plt.tight_layout()
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')


    #Displays all plt graphs
    plt.show()
