import json
import pandas
import numpy as np
import math
import requests
from demoparser import DemoParser
from random import sample as sample

FlareSolverrURL = "http://localhost:8191/v1"
FlareSolverrHeaders = {"Content-Type": "application/json"}

params = {"cmd": "request.get", "url": "https://www.hltv.org/matches/2353993/*", "maxTimeout": 60000}

# open events.json for parsing
with open("events.json", "r") as events:
    data = json.load(events)

# number of matches to download
n = 80

matchIDs = []
matchIDsToFetch = []
matchURLsToFetch = []
results = []
totalMaps = 0

# populate lists
for i in range(len(data)):
    matchIDs.append(data[i]["id"])
    if data[i]["format"] != "bo1":
        results.append([data[i]["result"]["team1"], data[i]["result"]["team2"]])
    else:
        if max(data[i]["result"], key = data[i]["result"].get) == "team1":
            results.append([1, 0])
        else:
            results.append([0, 1])

# total maps across 2022 Liquipedia S-tier tournaments
totalMaps = sum(np.array(results).sum(1))
print(totalMaps)

# getting an estimate for data size
# IEM Katowice 2022 grand final has multiple overtimes, 3:0 Bo5 comes out to 716 MB
# IEM Cologne 2022 grand final has fewer overtimes, 3:2 Bo5 comes out to 980 MB
# 750 MB per match is a good rough upper estimate of mean match file size
print(totalMaps / len(data))
print(math.ceil(n * (totalMaps / len(data))))
print(math.ceil(n * (totalMaps / len(data))) * 0.75)
print((math.ceil(n * (totalMaps / len(data))) * 0.75) / 0.01 / 60 / 60)

matchIDsToFetch = sample(matchIDs, n)

for i in range(n):
    matchURLsToFetch.append("https://www.hltv.org/matches/" + str(matchIDsToFetch) + "/*")


response = requests.post(FlareSolverrURL, headers = FlareSolverrHeaders, json = params)
print(str(response.content))
