import json
import pandas
import numpy as np
import math
import requests
import urllib.request as url
from bs4 import BeautifulSoup
from demoparser import DemoParser
from random import sample as sample
from random import randint as rand
from time import sleep as sleep

# define FlareSolverr variables for bypassing Cloudflare
FlareSolverrURL = "http://localhost:8191/v1"
FlareSolverrHeaders = {"Content-Type": "application/json"}

# open events.json for parsing
with open("events.json", "r") as events:
    data = json.load(events)

# number of matches to download
n = 80

matchIDs = []
matchIDsToFetch = []
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
print("mean maps per match: ", "{:,.3f}".(totalMaps / len(data)))
print("total maps to download: ", math.ceil(n * (totalMaps / len(data))))
print("total GB to download: ", (math.ceil(n * (totalMaps / len(data))) * 0.75))
print("download time: ", math.floor(math.ceil(n * (totalMaps / len(data))) * 0.75 / 0.01 / 60 / 60))

matchIDsToFetch = sample(matchIDs, n)

matchURL = ""
params = []
downloadURLs = []

for i in range(n):
    matchURL = "https://www.hltv.org/matches/" + str(matchIDsToFetch[i]) + "/*"
    params.append({"cmd": "request.get", "url": matchURL, "maxTimeout": 60000})
    response = requests.post(FlareSolverrURL, headers = FlareSolverrHeaders, json = params[i])

    html = BeautifulSoup(response.content, "html.parser")
    htmlLinks = html.find_all("a")

    for j in htmlLinks:
        if "data-demo-link" in str(j):
            print(str(j)[44:64])
            downloadURLs.append("https://www.hltv.org" + str(j)[44:64])

    sleep(rand(20, 30))
