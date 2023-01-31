#For Files Sorting
import csv
import os
import json
import pandas as pd
#For API call
from time import sleep
import requests
#remove warning
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

##TAKING DATA FROM ALL JSON FILES TO OUTPUT INTO OUTPUT FILE 
pathto = "jsonFiles\\"
steamApiKey = "AEC4752C93B5A9426B6096E8B60CE3D7"

def createNodes(json_files):
    mdata = pd.read_csv('jsonFiles\csvFiles\Nodetemplate.csv')
    for f in json_files:
        #Loads Json API data to then deposit it all into a new file
        with open("jsonFiles\\"+f,"r+") as json_fil:
            data = json.load(json_fil)
            if bool(data)==False:
                continue
            for i in range(len(data['friends'])):
                inse = data['friends'][i]['steamid']
                if inse not in mdata.values:
                    mdata = mdata.append({'Name':inse},ignore_index=True)
    print(mdata)
    mdata.to_csv("jsonFiles\csvFiles\outputNodes.csv")

    data = pd.read_csv('jsonFiles\csvFiles\outputNodes.csv')
    data.rename(columns={'Unnamed: 0':'ID'},inplace=True)
    data.to_csv("jsonFiles\csvFiles\outputNodes.csv",index=False)

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
                json_fil.truncate(0)
                json_fil.seek(0)
                #print("success")
                json_fil.write(json.dumps(data))

def APICall(sID):
    steamID = str(sID)

    sl1 = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key="
    sl2 = "&steamid=" + steamID + "&relationship=friend&format=json"
    slk = sl1 + steamApiKey + sl2
    r = requests.get(slk)

    steam = r.json()
    jFC = open(pathto+steamID+".json",'w')
    jFC.write(json.dumps(steam))
    jFC.close()

#Initial Indexing of folder
jFiles = [pos_json for pos_json in os.listdir(pathto) if pos_json.endswith(".json")]

#Starting Json File
jFile = input("Please Enter Valid Steam Id to search: ")
if jFile+'.json' not in jFiles:
    APICall(jFile)
removeFL([jFile+".json"])

#2nd indexing of folder after initial steam id is read
jFiles = [pos_json for pos_json in os.listdir(pathto) if pos_json.endswith(".json")]

#Calls all friends lists from base steamID to get 3 degrees of seperation
with open("jsonFiles\\"+jFile+'.json',"r") as json_fil:
    fridata = json.load(json_fil)
    for i in range(len(fridata['friends'])):
        if fridata['friends'][i]['steamid']+'.json' not in jFiles:
            APICall(fridata['friends'][i]['steamid'])
            print('NOT INTENDED')
            sleep(0.02)

#last Indexing to send all JSON File names to function
jFile = [pos_json for pos_json in os.listdir(pathto) if pos_json.endswith(".json")]
removeFL(jFile)
createNodes(jFile)

#CREATE EDGES