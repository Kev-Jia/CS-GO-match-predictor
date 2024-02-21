from awpy import DemoParser
from awpy.analytics.stats import player_stats
from awpy.analytics.map_control import extract_teams_metadata, calc_frame_map_control_values, calculate_round_map_control_metrics
from awpy.visualization.plot import plot_frame_map_control, plot_round_map_control, plot_map_control_metrics
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
import multiprocessing as mp
import math
import logging
import logging.handlers
import json


files = [str(i) for i in Path(r"../demos/").glob("**/*") if i.is_file()]
demoPaths = [i for i in files if ".dem" in i]

for i in demoPaths:
    parser = DemoParser(demofile = i, parse_rate = 128, buy_style = "hltv")
    data = parser.parse()
    print(i)
