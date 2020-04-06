import csv
import matplotlib.pyplot as plot
import numpy as numpy
from datetime import datetime
import random

authors = []
touched_files = []
dates = []

with open("Davis_rootbeer.csv", mode='r') as rootbeer_csv:
    count = 1
    reader = csv.DictReader(rootbeer_csv)

    for rows in reader:
        if count == 1 or count % 2 == 1:
            count += 1
            continue

        if count > 100:
            break

        # Formatting the date
        good_commit_date = datetime.strptime((rows['Commit Date'].replace('T', ' ')).replace('Z', ''),
                                             '%Y-%m-%d %H:%M:%S')

        authors.append(rows['Author Name'])
        touched_files.append(rows['File Name'])
        dates.append(good_commit_date)

        count += 1

files_names_dict = {}
files_with_names = []

counter = 1
for file in touched_files:
    if file in files_names_dict:
        files_with_names.append(files_names_dict[file])
    else:
        files_names_dict[file] = 'F ' + str(counter)
        counter += 1
        files_with_names.append(files_names_dict[file])

names_colors_dict = {}
names_with_colors = []

for author in authors:
    if not author in names_colors_dict:
        names_colors_dict[author] = "%06x" % random.randint(0, 0xFFFFFF)
    names_with_colors.append('#' + names_colors_dict[author])

files_dates_dict = {}
files_with_dates = numpy.zeros(50)

for i in range(49, -1, -1):
    if not touched_files[i] in files_dates_dict:
        files_dates_dict[touched_files[i]] = dates[i]
    files_with_dates[i] = int((dates[i] - files_dates_dict[touched_files[i]]).days / 7)

plot.scatter(files_with_names, files_with_dates, c=names_with_colors, s=50)
plot.xlabel("Touched Files");
plot.ylabel("Weeks")
plot.show()
