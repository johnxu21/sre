import json
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from datetime import datetime, timedelta
import pprint

# FILL THIS IN:

input_file = "rootbeer.json"



def parseTimestamp(string):
    return datetime.fromisoformat(string[:-1]) # strip 'Z' character, python can't handle...

with open(input_file, 'r') as file:
    x = json.load(file)
    files = x['files']
    authors = x['authors']

xs = []
ys = []
colors = []
fileIDs = {}
for filename, commits in files.items():
    fileID = fileIDs.setdefault(filename, len(fileIDs))
    for commit in commits:
        timestamp = parseTimestamp(commit[0])
        xs.append(fileID)
        ys.append(timestamp)
        colors.append(authors[commit[1]])

earliest = min(ys)
print(earliest)
ys_weeks = [(t - earliest).days/7.0 for t in ys]

print()
pprint.pprint(list(fileIDs.keys()))
print('Total number of files: ' + str(len(files)))
print()
pprint.pprint(list(authors.keys()))
print('Total number of authors: ' + str(len(authors)))

plt.scatter(x=xs, y=ys_weeks, c=colors, cmap="Set1")
plt.xlabel("file")
plt.ylabel("weeks")
plt.show()
