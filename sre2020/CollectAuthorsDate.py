import json
from pip._vendor import requests
import csv

def repofiles (repofilenames, filecsv):
    with open(filecsv, newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        line = 0
        for row in csv_reader:
            if line > 0:
                print(row[0])
            line += 1



filecsv = 'csv/file_backpack.csv'
repofilenames = list()
repofiles(repofilenames, filecsv)