from selenium import webdriver
from seleniumScripts import buildRow
import PySimpleGUI as sg
import csv
import os

# Window Layouts 

fileSelectorColumn = [
    [
        [sg.Text("Please Select Montgomery FOIA CSV:")],
        [sg.Input(), sg.FileBrowse()],
        [sg.Text("Please Select Destination:")],
        [sg.Input(), sg.FolderBrowse()],
        [sg.Text("Please Select Chromedriver:")],
        [sg.Input(), sg.FileBrowse()],
        [sg.OK(), sg.Cancel()]
    ]
]

window = sg.Window(title="Montgomery-FOIA-Script", layout=fileSelectorColumn, margins=(150, 150))

csvFileTarget = ""
outputFileDestination = ""
outputFileName = ""
chromedriverLocation=""

while True:
    event, values = window.read()

    if event == "OK":
        if values[0] == '':
            sg.popup("Please Select a CSV")
        elif not values[0].endswith(".csv"):
            sg.popup("Incorrect Input File Type. \nPlease Select a CSV")
        elif values[1] == '':
            sg.popup("Please Select a Destination Folder. \nE.g. C:\\Users\\FOIA_PC\\Desktop")
        elif values[2] == '':
            sg.popup("Please Select ChromeDriver. \nE.g. C:\\Users\\FOIA_PC\\Downloads\\chromedriver.exe")
        elif not values[2].endswith("chromedriver.exe"):
            sg.popup("Please Select the chromedriver. Must be named \"chromedriver\"")
        else:
            outputFileName = sg.popup_get_text("Please Give a Name to the Output CSV: \nE.g. DateTimeCounty.csv")
            if not outputFileName.endswith(".csv"):
                sg.popup("Incorrect Output CSV Name. \nPlease add \".csv\"")
            else:
                csvFileTarget = values[0]
                outputFileDestination = values[1]
                chromedriverLocation = values[2]
                break
    elif event == "Cancel":
        quit()
    elif event == sg.WIN_CLOSED:
        quit()

window.close()

driver = ''

try:
    driver = webdriver.Chrome(chromedriverLocation)
except:
    sg.popup("Incorrect version of chromedriver. Please see the instructions for help.")
    quit()

outputList = []
problemList = []

with open(csvFileTarget) as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    next(reader)
    for row in reader:
        newRow = ''
        try:
            newRow = buildRow(driver, row[0], row[1])
            outputList.append(newRow)
        except:
            problemList.append(row)  

with open(os.path.join(outputFileDestination, outputFileName), 'w', newline='\n') as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerow(["List", "Levy Year", "Bill Type", "Bill No.", "Company Name", "Balance", "Interest", 
            "Total", "Is List eq to Total", "Property Address", "Mortgage Line 1", "Property Description", "Mortgage Line 2", "Mortgage Line 3"])
    for row in outputList:
        writer.writerow(row)

if problemList:
    with open(os.path.join(outputFileDestination, "problem_numbers.csv"), 'w', newline='\n') as problemL:
        writer = csv.writer(problemL, delimiter=",")
        writer.writerow(["Bill No.", "Balance"])
        for row in problemList:
            writer.writerow(row)

driver.close()