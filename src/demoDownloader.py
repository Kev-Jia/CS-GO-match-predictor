import json
import pandas
import numpy as np
import math
import sys
import os
import requests
import urllib.request as url
import multiprocessing
import webbrowser

from pathlib import Path
from bs4 import BeautifulSoup
from demoparser import DemoParser
from random import sample as sample
from random import randint as rand
from time import sleep as sleep

threads = 4

webbrowser.open("", new = 0)

# define FlareSolverr variables for bypassing Cloudflare
FlareSolverrURL = "http://localhost:8191/v1"
FlareSolverrHeaders = {"Content-Type": "application/json"}

# match download function
def download(matchID, downloadURL):

    home = os.path.expanduser("~")
    filePath = "../demos/" + str(matchID)

    Path(filePath).mkdir(parents = True, exist_ok = True)

    params = {"cmd": "request.get", "url": downloadURL, "maxTimeout": 60000}

    # using FlareSolverr to bypass Cloudflare for hltv.org
    response = requests.post(FlareSolverrURL, headers = FlareSolverrHeaders, json = params)
    webbrowser.open(downloadURL, new = 2)

    os.chdir(home + "/Downloads")

    for

    with open(str(matchID) + ".rar", "wb") as archive:
        archive.write(response.content)

    # random delay to avoid bot detection
    sleep(rand(20, 30))

# open matches.json for parsing
with open("downloadURLs.json", "r") as downloads:
    data = json.load(downloads)

# populate lists
matchIDs = list(data.keys())
downloadURLs = list(data.values())
matches = np.column_stack((matchIDs, downloadURLs))

for i in range(1):
    download(matches[i][0], matches[i][1])
