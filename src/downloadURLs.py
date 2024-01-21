import json
import pandas
import numpy as np
import math
import sys
import requests
import cloudscraper

from pathlib import Path
from bs4 import BeautifulSoup
from demoparser import DemoParser
from random import sample
from random import randint as rand
from time import sleep
from time import time as timeNow

# program start time
start = timeNow()

# set up scraper to bypass Cloudflare
scraper = cloudscraper.create_scraper()

def fetchDownloadURL(matchID):
    # creating match URL to fetch
    matchURL = "https://www.hltv.org/matches/" + str(matchID) + "/*"

    # fetch URL contents through scraper
    response = scraper.get(matchURL).content

    # parsing HTML
    # searching HTML for all <a> tags
    html = BeautifulSoup(response, "html.parser")
    htmlLinks = html.find_all("a")

    # search all found <a> tags for download IDs
    # return download URLs
    for link in htmlLinks:
        if "data-demo-link" in str(link):
            return ("https://www.hltv.org" + str(link)[38:58])

# open matches.json for parsing
with open("matches.json", "r") as events:
    data = json.load(events)

# number of matches to download
n = 80

# lists to store necessary data
matchIDs = []
matchIDsToFetch = []
results = []
totalMaps = 0

# populate lists
for i in range(len(data)):
    # filter for Bo3 matches only
    if data[i]["format"] == "bo3":
        results.append([data[i]["result"]["team1"], data[i]["result"]["team2"]])
        matchIDs.append(data[i]["id"])

# total Bo3's across 2022 Liquipedia S-tier tournaments
print("total Bo3's 2022:", len(results))

# total maps across 2022 Liquipedia S-tier tournaments Bo3 matches
totalMaps = sum(np.array(results).sum(1))
print("total maps for all Bo3's 2022:", totalMaps)

# getting an estimate for data size
# IEM Katowice 2022 grand final has multiple overtimes, 3:0 Bo5
# this Bo5 can effectively be treated as a rough upper bound for Bo3's length

# compressed it comes out to ~700 MiB
# uncompressed it comes out to ~1.5 GiB
# 500 MiB is a good rough estimate for upper mean compressed match size
# 1 GiB is a good rough estimate for upper mean uncompressed match size
print("mean maps per match:", str("{:.3f}".format(totalMaps / len(data))))
print("expected total maps to download:", math.ceil(n * (totalMaps / len(data))))
print("download (compressed):", (math.ceil(n * (totalMaps / len(data))) * 0.5), "GiB")
print("download (uncompressed)/dataset size:", 2 * (math.ceil(n * (totalMaps / len(data))) * 0.5), "GiB")

time = (math.ceil(n * (totalMaps / len(data))) * 0.5 / 0.01 / 60 / 60)
print("download time:", int(math.modf(time)[1]), "h", math.ceil(math.modf(time)[0] * 60), "min\n")

matchIDsToFetch = sample(matchIDs, n)
downloadURLs = []

# fetching download URLs for all the match IDs randomly sampled
for i in range(n):
    # stuff for progress indicator
    minsElapsed = str(int((timeNow() - start) // 60))
    secsElapsed = str("{:.1f}".format(timeNow() - start - (float(minsElapsed) * 60)))
    timeElapsed = minsElapsed + " min " + secsElapsed + " s"

    details = str(str(i + 1) + "/" + str(n) + ", " + timeElapsed + ", " + downloadURLs[i] + ", " + str(matchIDsToFetch[i]) + "    ")

    sys.stdout.write(str("\r [ %d" % ((i + 1) * (100 / n)) + "% ] ") + details)

    # add download URL to list
    downloadURLs.append(fetchDownloadURL(matchIDsToFetch[i]))

    # random delay to avoid bot detection
    sleep(rand(20, 30))

    sys.stdout.flush()

# dictionary matching match IDs to download URLs
downloadURLsJson = {matchIDsToFetch[i]:downloadURLs[i] for i in range(n)}

# save this dictionary to downloadURLs.json
with open("downloadURLs.json", "w") as download:
    json.dump(downloadURLsJson, download, indent = 2)

print("\n")



