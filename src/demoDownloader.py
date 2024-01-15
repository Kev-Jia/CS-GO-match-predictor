import json
import pandas
import numpy as np
import math
import sys
import requests
import urllib.request as url
import multiprocessing

from pathlib import Path
from bs4 import BeautifulSoup
from demoparser import DemoParser
from random import sample as sample
from random import randint as rand
from time import sleep as sleep

threads = 4

# define FlareSolverr variables for bypassing Cloudflare
FlareSolverrURL = "http://localhost:8191/v1"
FlareSolverrHeaders = {"Content-Type": "application/json"}

# match download function
def download(downloadURL, matchID):
    filePath = "/../demos/" + str(matchID)

    Path(fileLocation).mkdir(parents = True, exist_ok = True)

    # Cloudflare once again poses an issue; this time for downloading matches themselves
    # FlareSolverr is much harder to implement here
    # it's probably possible, but frankly i can't be bothered
    # a simple solution of opening the match download URL in the default browser is implemented here


    params = {"cmd": "request.get", "url": downloadURL, "maxTimeout": 60000}

    requests.get(downloadURL, verify=False,stream=True)

    # random delay to avoid bot detection
    sleep(rand(20, 30))

# open matches.json for parsing
with open("downloadURLs.json", "r") as events:
    data = json.load(events)

# populate lists
matchIDs = data.keys()
downloadURLs = data.values()
matches = np.column_stack((matchIDs, matchURLs))

Path("/../demos/" + str(matchIDs))
