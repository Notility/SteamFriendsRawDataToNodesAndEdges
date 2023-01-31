# SteamFriendsRawDataToNodesAndEdges
Imports data from steam API to create a network map's raw data files.

Instructions on how to use the code
1.  Read the python code and import all modules not installed on local computer
2.  Get a steam API key from the steam website and set the steamAPIKey variable to it
3.  figure out the steamID64 (Dec) of the person you want to get 3 degrees of friendship on (Looks like: 76561198132863364)
4.  run the sortingExistingData file and input steamID (Ignore that its named that, I dont want to rename it atm)

After that it should take a little bit and it should then generate 2 files in the csv files folder, a nodes file and an edges file

I havn't tested it with other programs, but I am currently using Gephi to visualize the data
