# FILL THIS IN:

filename_filter = lambda f: f.endswith(".java")
repo = 'scottyab/rootbeer'
lstTokens = ["2f8d9bd83ca6993febe56a0a42fffcecfac6ee84"]

# will outputs JSON file <repo_name>.json

import json
from pip._vendor import requests
from typing import *
import dataclasses
from datetime import datetime, timedelta
import pprint
import json

def countfiles():
    # Filename to list of Commit objects
    files = {}
    # Author to unique integer
    authors = {}

    ipage = 1  # url page counter
    ct = 0  # token counter
    
    while True:
        ct = ct % len(lstTokens)
        commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + str(ipage) + \
                     '&per_page=100&access_token=' + lstTokens[ct]
        ct += 1
        # print("request " + commitsUrl)
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

            authorEmail = shaDetails['commit']['author']['email']
            authorID = authors.setdefault(authorEmail, len(authors))
            commitTimestamp = shaDetails['commit']['author']['date']

            print("author " + authorEmail + " has ID " + str(authorID))

            commit = ( commitTimestamp, authorEmail )

            for file in shaDetails['files']:
                filename = file['filename']
                if not filename_filter(filename):
                    print("skip " + filename)
                    continue
                commits = files.setdefault(filename, [])
                commits.append(commit)
                print("commits for " + filename + ": " + str(len(commits)))
        ipage += 1
    return (files, authors)

print("starting")
files, authors = countfiles()
print("done")

print()
pprint.pprint(list(files.keys()))
print('Total number of files: ' + str(len(files)))
print()
pprint.pprint(list(authors.keys()))
print('Total number of authors: ' + str(len(authors)))

with open(repo.split("/")[1]+".json", 'w') as file:
    json.dump({
        "files": files,
        "authors": authors,
    }, file)
