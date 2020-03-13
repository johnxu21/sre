
import json
from pip._vendor import requests
import csv

# @dictFiles empty dictionary of files
# @lstTokens GitHub authentication tokens
def countfiles( lsttokens, repo, filenames, names, dates):
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
                    if filename.endswith('.java'):
                        name = shaDetails['commit']['author']['name']
                        date = shaDetails['commit']['author']['date']
                        names.append(name)
                        dates.append(date)
                        filenames.append(filename)
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)

repo = 'scottyab/rootbeer'
# put your tokens here
lstTokens = ['69ad9d0be4967e0b5cb1b010f96180eb3c858992']

names = []
dates = []
dictfiles = dict()
filenames = []
countfiles(lstTokens, repo, filenames, names, dates)
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