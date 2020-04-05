import json
from pip._vendor import requests
import csv


# @dictFiles empty dictionary of files
# @lstTokens GitHub authentication tokens

def countfiles(lsttokens, repo, filenames, authornames, commitdates):
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

                for file in files:
                    filename = file['filename']

                    if filename.endswith('.xml') or filename.endswith('.java'):
                        authorname = shaDetails['commit']['author']['name']
                        commitdate = shaDetails['commit']['author']['date']

                        authornames.append(authorname)
                        commitdates.append(commitdate)

                        filenames.append(filename)
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)


repo = 'scottyab/rootbeer'
# put your tokens here
lstTokens = ['156278603c7a62242a141ff1f842c4753c3a74db']

authornames = []
commitdates = []
dictfiles = dict()
filenames = []

countfiles(lstTokens, repo, filenames, authornames, commitdates)

print('Total number of files: ' + str(len(filenames)))

file = repo.split('/')[1]

# change this to the path of your file
fileOutput = 'Davis_' + file + '.csv'  # /Users/businge/Documents/00Mercy/sre2020/file_'+file+'.csv'
rows = ["File Name", "Author Name", "Commit Date"]

fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

iterator = 0;
for filename in filenames:
    rows = [filename, authornames[iterator], commitdates[iterator]]
    iterator += 1
    writer.writerow(rows)
fileCSV.close()
