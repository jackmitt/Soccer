import requests
import hashlib
import pandas as pd
import numpy as np
import datetime
import time
from helpers import standardizeTeamName
from helpers import convert_league
import pickle

my_key = "4f020f4a19a2a1edd72fa163b83db44c63fbff959fb9c1ee34144db6a6a3f715"

def save_season_ids():
    response = requests.get("https://api.football-data-api.com/league-list?key=" + my_key + "&chosen_leagues_only=true").json()
    for league in response["data"]:
        dict = {}
        cur_league = league["name"]
        for season in league["season"]:
            dict[str(season["year"])[0:4]] = season["id"]
        with open("./footy_stats_ids/" + cur_league + ".pkl", "wb") as f:
            pickle.dump(dict, f)

def construct_csvs():
    dict = {"Season":[],"Date":[],"h_id":[],"a_id":[],"Home":[],"Away":[],"h_goals":[],"a_goals":[],"h_xg":[],"a_xg":[]}
    with open("./footy_stats_ids/England Premier League.pkl","rb") as inputFile:
        season_ids = pickle.load(inputFile)
    for key in season_ids:
        response = requests.get("https://api.football-data-api.com/league-matches?key=" + my_key + "&season_id=" + str(season_ids[key])).json()
        for match in response["data"]:
            dict["Season"].append(key)
            dict["Date"].append(datetime.datetime.fromtimestamp(match["date_unix"]))
            dict["Home"].append(match["home_name"])
            dict["Away"].append(match["away_name"])
            dict["h_id"].append(match["homeID"])
            dict["a_id"].append(match["awayID"])
            dict["h_goals"].append(match["homeGoalCount"])
            dict["a_goals"].append(match["awayGoalCount"])
            if (match["team_a_xg"] == 0 and match["team_b_xg"] == 0):
                dict["h_xg"].append(match["homeGoalCount"])
                dict["a_xg"].append(match["awayGoalCount"])
            else:
                dict["h_xg"].append(match["team_a_xg"])
                dict["a_xg"].append(match["team_b_xg"])
    df = pd.DataFrame.from_dict(dict)
    df = df.sort_values(by=["Date"], ignore_index = True)
    df.to_csv("./csv_data/England1/footystats.csv", index = False)
