import csv
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import random

filename = "rootbeer.csv"

files = []
authors = []
dates = []

with open(filename, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    count = 1
    for rows in csv_reader:
        if count > 100:
            break
        if count == 1 or count%2 == 1:
            count += 1
            continue
        count += 1
        files.append(rows['Filename'])
        authors.append(rows['Author'])
        dates.append(datetime.strptime((rows['Date'].replace('T', ' ' )).replace('Z', ''), '%Y-%m-%d %H:%M:%S' ))

dictFilesNames = {}
dictFilesDates = {}
dictNamesColors = {}
filesWithNames = []
filesWithDates = np.zeros(50)
namesWithColors = []

count = 1
for file in files:
    if file in dictFilesNames:
        filesWithNames.append(dictFilesNames[file])
    else:
        dictFilesNames[file] = 'file ' + str(count)
        count += 1
        filesWithNames.append(dictFilesNames[file])

for i in range(49, -1, -1):
    if not files[i] in dictFilesDates:
        dictFilesDates[files[i]]=dates[i]
    filesWithDates[i] = int((dates[i]-dictFilesDates[files[i]]).days / 7)

for author in authors:
    if not author in dictNamesColors:
         dictNamesColors[author] = "%06x" % random.randint(0, 0xFFFFFF)
    namesWithColors.append('#' + dictNamesColors[author])


plt.scatter(filesWithNames, filesWithDates, c=namesWithColors, s=50)
plt.show()