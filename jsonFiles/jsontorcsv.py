import json
import os
import csv
from cherrypicker import CherryPicker 
import pandas as pd

path_to_json = "jsonFiles\\"
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith(".json")]

print(json_files)

def removeFL(jsonFileNs):
    for p in jsonFileNs:
        with open("jsonFiles\\"+p,"r+") as json_fil:
            data = json.load(json_fil)
            #print(data['friendslist']['friends'][5]['steamid'])
            if "friendslist" in data:
                data.update(data.pop("friendslist"))
                for i in range(len(data['friends'])):
                    del data['friends'][i]['relationship']
                    del data['friends'][i]['friend_since']
                print(data['friends'])
                json_fil.truncate(0)
                json_fil.seek(0)
                print("success")
                json_fil.write(json.dumps(data))


def cvsPharm(jsonFileN):
    with open("jsonFiles\\"+jsonFileN) as file:
        data = json.load(file)

    picker = CherryPicker(data)
    flat = picker['friends'].flatten().get()
    df = pd.DataFrame(flat)
    df.to_csv("jsonFiles\csvFiles\\"+jsonFileN[:-5]+".csv", index=False)

removeFL(json_files)


for p in json_files:
    cvsPharm(p)