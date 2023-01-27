import csv
import os
import json
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
##TAKING DATA FROM ALL JSON FILES TO OUTPUT INTO OUTPUT FILE 
pathto = "jsonFiles\\"

json_files = [pos_json for pos_json in os.listdir(pathto) if pos_json.endswith(".json")]

fileName = json_files[0][:-5]
fileInt = int(fileName)

for f in json_files:
    mdata = pd.read_csv('jsonFiles\csvFiles\outputtemplate.csv')
    if fileInt in mdata.values:
        print("test")        
    else:
        mdata = mdata.append({'Name':fileName},ignore_index=True)
    print(mdata)
    
    with open("jsonFiles\\"+f,"r+") as json_fil:
        data = json.load(json_fil)
        print(data)
        for i in range(len(data['friends'])):
            inse = data['friends'][i]['steamid']
            if inse not in mdata.values:
                mdata = mdata.append({'Name':inse},ignore_index=True)
        print(mdata)
    mdata.to_csv("jsonFiles\csvFiles\output.csv")

print(json_files)

#for f in json_files: