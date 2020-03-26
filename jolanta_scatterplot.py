import csv
import numpy as np
import datetime
import matplotlib.pyplot as plt

filenames = []
authors = []
dates = []

with open('lab2_rootbeer.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            filenames.append(row[0])
            authors.append(row[1])
            dates.append(row[2])
            line_count += 1
    print(f'Processed {line_count} lines.')

changeDates = []
dateTimeObj = []
iter = 0
for i in dates:
    i = i.split("-")
    z = i[2].split("T")
    i[2] = z[0]
    z = z[1].split(":")
    for elem in z:
        i.append(elem)
    i[5] = i[5][:2]
    dateTimeStr = i[0] + '-' + i[1] + '-' + i[2] + ' ' + i[3] + ':' + i[4] + ':' + i[5] + '.000000'
    print(dateTimeStr)
    dateTimeObj.append(datetime.datetime.strptime(dateTimeStr, '%Y-%m-%d %H:%M:%S.%f'))


minDate = min(dateTimeObj)
maxDate = max(dateTimeObj)
maxValueOfY = maxDate - minDate



uniqueAuthors = list(set(authors))
numberOfAuthors = len(uniqueAuthors)

uniqueFilenames = list(set(filenames))
numberOfFilenames = len(uniqueFilenames)

uniqueFilenames1 = []
for elem in uniqueFilenames:
    s = elem.split("/")
    uniqueFilenames1.append(s[-1])

X = []
for elem in filenames:
    iterator = uniqueFilenames.index(elem)
    X.append(uniqueFilenames1[iterator])

Y = []
for elem in dateTimeObj:
    timeDiff = abs(elem - minDate).total_seconds() / 3600
    print(timeDiff)
    Y.append(timeDiff)

Z = []
for elem in authors:
    iterator = uniqueAuthors.index(elem)
    color = str((iterator + 1) * len(uniqueAuthors) / 255)
    Z.append(color)

plt.scatter(X, Y, s=250, c=Z)
plt.xlabel('Name of the file')
plt.ylabel('Number of days from first commit')
plt.show()