import json
from pip._vendor import requests
import csv

# @dictFiles empty dictionary of files
# @lstTokens GitHub authentication tokens
def countfiles(lsttokens, repo, filenames, names, datas):
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
                files = shaDetails['files']
                print("---")
                for file in files:
                    filename = file['filename']
                    if filename.endswith('.java'):
                        name = shaObject['commit']['author']['name']
                        date = shaObject['commit']['author']['date']
                        filenames.append(filename)
                        names.append(name)
                        datas.append(date)

            ipage += 1
    except:
        print("Error receiving data")
        exit(0)

repo = 'scottyab/rootbeer'
# put your tokens here
lstTokens = ['f75bfa19d05bed6ea42036b0beb0192e7d96362a']


dictfiles = dict()
filenames = []
names = []
datas = []
countfiles(lstTokens, repo, filenames, names, datas)
print('Total number of files: ' + str(len(dictfiles)))

file = repo.split('/')[1]
#change this to the path of your file
fileOutput = '/home/jola/Documents/SoftwareReengineering/lab3/lab2_' +file+'.csv'
rows = ["Filename", "Authors", "Dates"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)


iteration = 0
for filename in filenames:
    rows = [filename, names[iteration], datas[iteration]]
    iteration += 1
    writer.writerow(rows)
fileCSV.close()