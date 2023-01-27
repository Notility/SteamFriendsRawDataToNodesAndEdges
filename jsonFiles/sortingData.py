import pandas as pd
import csv
import os
import json

pathto = "jsonFiles\\"

json_files = [pos_json for pos_json in os.listdir(pathto) if pos_json.endswith(".json")]
#with open('jsonFiles\csvFiles\output.csv','r+'):

fileName = json_files[0][:-5]

mdata = pd.read_csv('jsonFiles\csvFiles\output.csv', index_col='Id')

idnow = len(mdata)+1

mdata = mdata.append({'Name':fileName},ignore_index=True)

mdata.head()

print(mdata)

print(mdata)
for p in json_files:
        with open("jsonFiles\\"+p,"r+") as json_fil:
            data = json.load(json_fil)

            idnow = len(data['friends'])+1

            print(idnow)

print(json_files)

#for f in json_files:
    