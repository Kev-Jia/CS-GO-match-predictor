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
with open("matches.json", "r") as events:
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

    # filter for Bo3 matches only
    if data[i]["format"] == "bo3":
        results.append([data[i]["result"]["team1"], data[i]["result"]["team2"]])

# total maps across 2022 Liquipedia S-tier tournaments
totalMaps = sum(np.array(results).sum(1))
print("total maps for all Bo3's 2022:", totalMaps)

# getting an estimate for data size
# IEM Katowice 2022 grand final has multiple overtimes, 3:0 Bo5 comes out to ~700 MiB
# uncompressed it comes out to ~1.5 GiB
# 500 MiB is a good rough estimate for mean compressed match size
# 1 GiB is a good rough estimate for mean uncompressed match size
print("mean maps per match:", str("{:.3f}".format(totalMaps / len(data))))
print("expected total maps to download:", math.ceil(n * (totalMaps / len(data))))
print("download (compressed):", (math.ceil(n * (totalMaps / len(data))) * 0.5), "GiB")
print("download (uncompressed)/dataset size:", 2 * (math.ceil(n * (totalMaps / len(data))) * 0.5), "GiB")

time = (math.ceil(n * (totalMaps / len(data))) * 0.5 / 0.01 / 60 / 60)
print("download time:", int(math.modf(time)[1]), "h,", math.ceil(math.modf(time)[0] * 60), "min\n")

matchIDsToFetch = sample(matchIDs, n)

matchURLToFetch = ""
params = []
downloadURLs = []

# fetching download URLs for all the match IDs randomly sampled
for i in range(n):
    # creating match URLs to fetch
    matchURLToFetch = "https://www.hltv.org/matches/" + str(matchIDsToFetch[i]) + "/*"
    params.append({"cmd": "request.get", "url": matchURLToFetch, "maxTimeout": 60000})

    # using FlareSolverr to bypass Cloudflare for hltv.org
    response = requests.post(FlareSolverrURL, headers = FlareSolverrHeaders, json = params[i])

    # parsing HTML
    # searching HTML for all <a></a> tags
    html = BeautifulSoup(response.content, "html.parser")
    htmlLinks = html.find_all("a")

    # search all found <a></a> tags for download IDs
    # form download URLs from download IDs
    for j in htmlLinks:
        if "data-demo-link" in str(j):
            print(str(i + 1) + "/" + str(n) + ",", str(j)[44:64] + ",", matchURLToFetch)
            downloadURLs.append("https://www.hltv.org" + str(j)[44:64])

    # random delay to avoid bot detection
    sleep(rand(20, 30))

# dictionary matching match IDs to download URLs
downloadURLsJson = {matchIDsToFetch[i]:downloadURLs[i] for i in range(n)}

# save this dictionary to downloadURLs.json
with open("downloadURLs.json", "w") as download:
    json.dump(downloadURLsJson, download)





