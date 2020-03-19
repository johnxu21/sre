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
                    dictfiles[filename] = dictfiles.get(filename, 0) + 1
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)

repo = 'scottyab/rootbeer'
# put your tokens here
lstTokens = ['29f258c44f6bc4a4ffbc35e686f67f7aefe55395']



names = []
dates = []
dictfiles = dict()
filenames = []
countfiles(dictfiles, lstTokens, repo)
print('Total number of files: ' + str(len(dictfiles)))


file = repo.split('/')[1]
#change this to the path of your file
fileOutput = file+'.csv' #/Users/businge/Documents/00Mercy/sre2020/file_'+file+'.csv'
rows = ["Filename", "Author", "Date"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

iterator = 0;
for filename in filenames:
    rows = [filename,  names[iterator], dates[iterator]]
    iterator+=1
    writer.writerow(rows)
fileCSV.close()