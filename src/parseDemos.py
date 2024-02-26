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
import json

def fetchMetadata(data, demoPath):
        lastRound = data["gameRounds"][-1]
        output = {}

        output["map"] = data["mapName"]
        output["winner"] = lastRound["winningTeam"]
        output["loser"] = lastRound["losingTeam"]
        output["winnerScore"] = max(lastRound["endTScore"], lastRound["endCTScore"])
        output["loserScore"] = min(lastRound["endTScore"], lastRound["endCTScore"])

        print(output, demoPath)

        return output

def fetchPlayerData(gameRoundData, rounds, demoPath):
    rawPlayerStats = player_stats(gameRoundData[:rounds])
    playerStatsDf = []
    playerStatsList = []
    players = {}

    for key in rawPlayerStats:
        playerStatsDf.append(rawPlayerStats[key])

    playerStatsDf = pd.DataFrame(playerStatsDf).to_dict("list")

    for i, j in zip(playerStatsDf["teamName"], playerStatsDf["playerName"]):
        players.setdefault(i, []).append(j)

    for i in range(10):
        steamID = str(playerStatsDf["steamID"][i])
        rawPlayer = rawPlayerStats[steamID]
        player = {}

        player["name"] = rawPlayer["playerName"]
        player["kpr"] = rawPlayer["kills"] / rounds
        player["dpr"] = rawPlayer["deaths"] / rounds
        player["adr"] = rawPlayer["adr"]
        player["kast"] = rawPlayer["kast"]
        player["rating"] = rawPlayer["rating"]

        # multikills per round, linearly weighted sum
        mkpr = ((0.2 * rawPlayer["kills1"]) + (0.4 * rawPlayer["kills2"]) + (0.6 * rawPlayer["kills3"]) + (0.8 * rawPlayer["kills4"]) + (1.0 * rawPlayer["kills5"])) / rounds
        apr = rawPlayer["assists"] / rounds # assists per round

        try:
            okpod = rawPlayer["firstKills"] / (rawPlayer["firstKills"] + rawPlayer["firstDeaths"]) # opening kills per opening duels taken
        except:
            okpod = 0

        cwpca = 0 # clutches won per clutch attempts, linearly weighted sum
        try:
            cwpca += 0.2 * (rawPlayer["success1v1"] / rawPlayer["attempts1v1"])
        except:
            cwpca += 0
        try:
            cwpca += 0.4 * (rawPlayer["success1v2"] / rawPlayer["attempts1v2"])
        except:
            cwpca += 0
        try:
            cwpca += 0.6 * (rawPlayer["success1v3"] / rawPlayer["attempts1v3"])
        except:
            cwpca += 0
        try:
            cwpca += 0.8 * (rawPlayer["success1v4"] / rawPlayer["attempts1v4"])
        except:
            cwpca += 0
        try:
            cwpca += 1.0 * (rawPlayer["success1v5"] / rawPlayer["attempts1v5"])
        except:
            cwpca += 0

        player["impact"] = mkpr + apr + okpod + cwpca # impact rating

        udr = rawPlayer["utilityDamage"] / rounds # utility damage per round
        btpr = rawPlayer["blindTime"] / rounds # blind time per round

        try:
            efpfb = rawPlayer["enemiesFlashed"] / rawPlayer["flashesThrown"] # enemies flashed per flashbang
        except:
            efpfb = 0

        try:
            tfpfb = rawPlayer["teammatesFlashed"] / rawPlayer["flashesThrown"] # teammates flashed per flashbang
        except:
            tfpfb = 0

        player["utility"] = (udr + btpr + efpfb - tfpfb) / 4 # utility rating

        playerStatsList.append(player)

    # players = ["teamName": [{player1 stats}, {player 2 stats}, etc]]
    playersKeys = list(players.keys())
    players[playersKeys[0]] = playerStatsList[:5]
    players[playersKeys[1]] = playerStatsList[5:]

    return players

def fetchTeamData(data, rounds, demoPath):
    buyTypes = {"Full Eco": 0.25, "Semi Eco": 0.5, "Semi Buy": 0.75, "Full Buy": 1.0}

    gameRoundData = data["gameRounds"]
    roundData = gameRoundData[rounds - 1]
    teamData = {}

    ct = {}
    t = {}

    ct["team"] = roundData["ctTeam"]
    ct["startScore"] = roundData["ctScore"]
    ct["equipmentValue"] = roundData["ctFreezeTimeEndEqVal"]
    ct["mapControl"] = 0
    ct["buy"] = buyTypes[roundData["ctBuyType"]]
    ct["players"] = []

    t["team"] = roundData["tTeam"]
    t["startScore"] = roundData["tScore"]
    t["equipmentValue"] = roundData["tFreezeTimeEndEqVal"]
    t["mapControl"] = 0
    t["buy"] = buyTypes[roundData["tBuyType"]]
    t["players"] = []

    # map control of last 5 rounds
    # unless less than 5 rounds have been played, in which case take all rounds up to that current
    # only calculate if more than 1 round has been played
    if rounds > 1:
        mapControl = 0
        if rounds < 5:
            for i in range(rounds):
                try:
                    mapControl += np.mean(calculate_round_map_control_metrics(data["mapName"], data["gameRounds"][rounds - (i + 1)]))
                except Exception as error:
                    print(error, demoPath)

            ct["mapControl"] = 1 + (mapControl / rounds)
            t["mapControl"] = 1 - (mapControl / rounds)
        else:
            for i in range(5):
                try:
                    mapControl += np.mean(calculate_round_map_control_metrics(data["mapName"], data["gameRounds"][rounds - (i + 1)]))
                except Exception as error:
                    print(error, demoPath)

            ct["mapControl"] = 1 + (mapControl / 5)
            t["mapControl"] = 1 - (mapControl / 5)

    teamData["round"] = roundData["roundNum"]
    teamData["ct_tBuyRatio"] = ct["buy"] / t["buy"]
    teamData["winningTeam"] = roundData["winningTeam"]
    teamData["winningSide"] = roundData["winningSide"]

    teamData["ct"] = ct
    teamData["t"] = t

    return teamData

def writeData(demoPath):
    jsonPath = str(demoPath[:-4] + "_PARSED.json")

    # if not Path(jsonPath).is_file():
    parser = DemoParser(demofile = demoPath, parse_rate = 128, buy_style = "hltv")
    data = parser.parse()

    gameRoundData = data["gameRounds"]

    output = fetchMetadata(data, demoPath)
    output["rounds"] = []

    for i in range(len(gameRoundData)):

        teamData = fetchTeamData(data, i + 1, demoPath)
        rawPlayers = fetchPlayerData(gameRoundData, i + 1, demoPath)
        rawPlayersKeys = list(rawPlayers.keys())

        if teamData["ct"]["team"] == rawPlayersKeys[0]:
            teamData["ct"]["players"] = rawPlayers[rawPlayersKeys[0]]
            teamData["t"]["players"] = rawPlayers[rawPlayersKeys[1]]

        if teamData["t"]["team"] == list(rawPlayers.keys())[0]:
            teamData["t"]["players"] = rawPlayers[rawPlayersKeys[0]]
            teamData["ct"]["players"] = rawPlayers[rawPlayersKeys[1]]

        output["rounds"].append(teamData)

    with open(jsonPath, "w") as parsedData:
        json.dump(output, parsedData, indent = 4)

    print("parsed", demoPath)
    #     return 0
    # else:
    #     print(demoPath)
    #
    #     return 1

if __name__ == "__main__":
    # number of threads
    # hence also number of "chunks", as below
    # must divide number of demos (80)
    n = 8

    files = [str(i) for i in Path(r"../demos/").glob("**/*") if i.is_file()]
    demoPaths = [i for i in files if ".dem" in i]

    # a = []
    #
    # for i in range(len(demoPaths)):
    #     status = writeData(demoPaths[i])
    #     if status == 0:
    #         a.append(demoPaths[i])
    #
    # print(len(a))

    # jsonPaths = [str(i[:-4] + "_PARSED.json") for i in files]
    # splitting lists of demo paths and JSON paths into chunks
    # chunkedDemoPaths = [demoPaths[i:i + n] for i in range(0, len(demoPaths), n)]

    output = writeData("../demos/test/g2-vs-faze-m1-inferno.dem")
    # mp.set_start_method("spawn")
    #
    # with mp.Pool(n) as pool:
    #     pool.map(writeData, demoPaths)

