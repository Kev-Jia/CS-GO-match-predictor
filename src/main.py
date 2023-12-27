import sys
sys.path.insert(1, "/home/kevin/Programming/EMC/hltv-api")

import api as hltv

# HLTV event IDs
# All S-Tier events listed on Liquipedia Counter-Strike from 01/2022 - 08/2023 inclusive
# ascending chronological order
eventIDs2022 = [6343, 6219, 6136, 6137, 6384, 6372, 6138, 6345, 6510, 6503, 6140, 6346, 6141, 6588, 6586, 6348, 6349]
eventIDs2023 = [6970, 6810, 6809, 6862, 6864, 6794, 6793, 6861, 6972, 6973, 6812, 6811, 7128]

eventIDs = eventIDs2022 + eventIDs2022

# Katowice, Cologne and Majors
# sublist of eventIDs
special_eventIDs = [6219, 6136, 6384, 6372, 6503, 6140, 6588, 6586, 6810, 6809, 6794, 6793, 6812, 6811]
