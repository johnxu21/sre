import json
from pip._vendor import requests
import csv


# @dictFiles empty dictionary of files
# @lstTokens GitHub authentication tokens
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter
    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            if ct == len(lstTokens):
                ct = 0
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + \
                         '&per_page=100&access_token=' + lsttokens[ct]
            ct += 1
            content = requests.get(commitsUrl)
            jsonCommits = json.loads(content.content)
            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in a page
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                if ct == len(lstTokens):
                    ct = 0
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha \
                         + '?access_token=' + lstTokens[ct]
                ct += 1
                content = requests.get(shaUrl)
                shaDetails = json.loads(content.content)
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    if filename.endswith('.xml') or filename.endswith('.java'):  # uncommented and modified this line
                        dictfiles[filename] = dictfiles.get(filename, 0) + 1
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)


repo = 'scottyab/rootbeer'
# put your tokens here
lstTokens = ['156278603c7a62242a141ff1f842c4753c3a74db']

dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)
print('Total number of files: ' + str(len(dictfiles)))

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = file + '.csv'
rows = ["Filename", "Touches"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

bigcount = None
bigfilename = None
for filename, count in dictfiles.items():
    rows = [filename, count]
    writer.writerow(rows)
    if bigcount is None or count > bigcount:
        bigcount = count
        bigfilename = filename
fileCSV.close()
print('The file ' + bigfilename + ' has been touched ' + str(bigcount) + ' times.')
