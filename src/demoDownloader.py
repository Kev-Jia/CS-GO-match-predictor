import json
import pandas
import numpy as np
import math
import sys
import os
import requests
import cloudscraper

from pathlib import Path
from bs4 import BeautifulSoup
from demoparser import DemoParser
from random import sample
from random import randint as rand
from time import sleep
from time import time as timeNow

# match directory
matchPath = os.getcwd() + "/" + "../demos/"

# program start time
start = timeNow()

# set up scraper to bypass Cloudflare
scraper = cloudscraper.create_scraper()

# match download function
def downloadMatch(matchID, downloadURL):
    # reset current working directory to match directory
    os.chdir(matchPath)

    # path for directory to store match archive
    archivePath = matchPath + str(matchID)

    # create directory to store match match archive
    Path(archivePath).mkdir(parents = True, exist_ok = True)

    # fetch match archive file from download URL
    matchArchive = scraper.get(downloadURL).content

    # save match archive file
    os.chdir(archivePath)
    with open(str(matchID) + ".rar", "wb") as match:
        match.write(matchArchive)

# open matches.json for parsing
with open("downloadURLs.json", "r") as downloads:
    data = json.load(downloads)

# populate lists
matchIDs = list(data.keys())
downloadURLs = list(data.values())
matches = np.column_stack((matchIDs, downloadURLs))

# number of matches
n = len(matches)

# download matches
for i in range(n):
    # stuff for progress indicator
    minsElapsed = str(int((timeNow() - start) // 60))
    secsElapsed = str("{:.1f}".format(timeNow() - start - (float(minsElapsed) * 60)))
    timeElapsed = minsElapsed + " min " + secsElapsed + " s"

    details = str(str(i + 1) + "/" + str(n) + ", " + timeElapsed + ", " + str(matches[i][0]) + "    ")

    sys.stdout.write(str("\r [ %d" % ((i + 1) * (100 / n)) + "% ] ") + details)

    # download match
    downloadMatch(matches[i][0], matches[i][1])

    # random delay to avoid bot detection
    sleep(rand(20, 30))

    sys.stdout.flush()
