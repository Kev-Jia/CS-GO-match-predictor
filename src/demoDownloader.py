import json
import pandas
from demoparser import DemoParser
from random import sample as sample

with open("events.json", "r") as events:
    data = json.load(events)

n = 500

matchIDs = []
matchIDsToFetch = []

for i in range(len(data)):
    matchIDs.append(data[i]["id"])

matchIDsToFetch = sample(range(len(matchIDs)), n)

print(matchIDsToFetch)
