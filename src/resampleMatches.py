import json
import pandas
import numpy as np
import math
import sys
import requests
import cloudscraper

import os
from bs4 import BeautifulSoup
from demoparser import DemoParser
from random import sample
from random import randint as rand
from time import sleep
from time import time as timeNow

# open matches.json for parsing
with open("matches.json", "r") as matches:
    data = json.load(matches)

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
        matchIDs.append(data[i]["id"])

matchIDs.remove(2357151)
matchIDs.remove(2354554)
matchIDs.remove(2353983)
matchIDs.remove(2356292)
matchIDs.remove(2357662)
matchIDs.remove(2360645)
matchIDs.remove(2356632)
matchIDs.remove(2357738)
matchIDs.remove(2357746)
matchIDs.remove(2356877)
matchIDs.remove(2354557)
matchIDs.remove(2356879)
matchIDs.remove(2356163)
matchIDs.remove(2360050)
matchIDs.remove(2354399)
matchIDs.remove(2356881)
matchIDs.remove(2354985)
matchIDs.remove(2353988)
matchIDs.remove(2356873)
matchIDs.remove(2357707)
matchIDs.remove(2354581)
matchIDs.remove(2354396)
matchIDs.remove(2354346)
matchIDs.remove(2359844)
matchIDs.remove(2359845)

for i in range(len(os.listdir("../demos"))):
    if int(os.listdir("../demos")[i]) in matchIDs:
        print(os.listdir("../demos")[i])
        matchIDs.remove(int(os.listdir("../demos")[i]))


print("")
print(len(matchIDs))
print("")
print(sample(matchIDs, 2))




