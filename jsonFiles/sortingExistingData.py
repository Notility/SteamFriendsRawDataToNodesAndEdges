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
steamApiKey = ""

def createNodes(json_files):
    mdata = pd.read_csv(pathto+'csvFiles\\Nodetemplate.csv')
    for f in json_files:
        #Loads Json API data to then deposit it all into a new file
        with open(pathto+f,"r") as json_fil:
            data = json.load(json_fil)
            if bool(data)==False:
                continue
            for i in range(len(data['friends'])):
                inse = data['friends'][i]['steamid']
                if inse not in mdata.values:
                    mdata = mdata.append({'Name':inse},ignore_index=True)
    print(mdata)
    mdata.to_csv(pathto+"csvFiles\outputNodes.csv")

    data = pd.read_csv(pathto+'csvFiles\outputNodes.csv')
    data.rename(columns={'Unnamed: 0':'ID'},inplace=True)
    data.to_csv(pathto+"csvFiles\outputNodes.csv",index=False)

def removeFL(jsonFileNs):
    for p in jsonFileNs:
        with open(pathto+p,"r+") as json_fil:
            data = json.load(json_fil)
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
    
def createEdges(json_files):
    odata = pd.read_csv(pathto+'csvFiles\EdgesTemplate.csv')
    mdata = pd.read_csv(pathto+'csvFiles\outputNodes.csv', dtype=str,index_col=None)
    for f in json_files:
        with open(pathto+f,"r") as json_fil:
            data = json.load(json_fil)
            if bool(data)==False:
                continue
            source = mdata.loc[mdata['Name'] == f[:-5]].index[0]
            for i in range(len(data['friends'])):
                inse = data['friends'][i]['steamid']
                target = mdata.loc[mdata['Name'] == inse].index[0]
                odata = odata.append({'Source':source,'Target':target,'Type':'Undirected','Weight':1},ignore_index=True)      
    odata.to_csv(pathto+"csvFiles\outputEdges.csv",index=False)

#Initial Indexing of folder
jFiles = [pos_json for pos_json in os.listdir(pathto) if pos_json.endswith(".json")]
createEdges(jFiles)
#Starting Json File
jFile = input("Please Enter Valid Steam Id to search: ")
if jFile+'.json' not in jFiles:
    APICall(jFile)
removeFL([jFile+".json"])

#2nd indexing of folder after initial steam id is read
jFiles = [pos_json for pos_json in os.listdir(pathto) if pos_json.endswith(".json")]

#Calls all friends lists from base steamID to get 3 degrees of seperation
with open(pathto+jFile+'.json',"r") as json_fil:
    fridata = json.load(json_fil)
    for i in range(len(fridata['friends'])):
        if fridata['friends'][i]['steamid']+'.json' not in jFiles:
            APICall(fridata['friends'][i]['steamid'])
            sleep(0.02)

#last Indexing to send all JSON File names to function
jFile = [pos_json for pos_json in os.listdir(pathto) if pos_json.endswith(".json")]
removeFL(jFile)
createNodes(jFile)