import pandas as pd
import numpy as np
import datetime
from os.path import exists
import os
from fuzzywuzzy import fuzz
from helpers import standardizeTeamName

def preMatchAverages(league):
    stats = pd.read_csv("./csv_data/" + league + "/betting.csv", encoding = "ISO-8859-1")
    for i in range(len(stats.index)):
        stats.at[i, "Date"] = datetime.date(int(stats.at[i, "Date"].split("-")[0]), int(stats.at[i, "Date"].split("-")[1]), int(stats.at[i, "Date"].split("-")[2]))
    stats = stats.sort_values(by=["Date"], ignore_index = True)

    dict = {"H_proj":[],"A_proj":[],"H_GP":[],"A_GP":[]}
    for index, row in stats.iterrows():
        if (index == 0 or abs(row["Date"] - stats.at[index-1,"Date"]).days > 30):
            seasonDict = {}
        if (row["Home"] not in seasonDict):
            seasonDict[row["Home"]] = {"G":[],"GA":[],"GP":0}
        if (row["Away"] not in seasonDict):
            seasonDict[row["Away"]] = {"G":[],"GA":[],"GP":0}

        dict["H_GP"].append(seasonDict[row["Home"]]["GP"])
        dict["A_GP"].append(seasonDict[row["Away"]]["GP"])
        if (seasonDict[row["Away"]]["GP"] > 5 and seasonDict[row["Home"]]["GP"] > 5):
            dict["H_proj"].append((np.average(seasonDict[row["Home"]]["G"]) + np.average(seasonDict[row["Away"]]["GA"])) / 2)
            dict["A_proj"].append((np.average(seasonDict[row["Away"]]["G"]) + np.average(seasonDict[row["Home"]]["GA"])) / 2)
        else:
            dict["H_proj"].append(np.nan)
            dict["A_proj"].append(np.nan)

        seasonDict[row["Home"]]["G"].append(row["Home Score"])
        seasonDict[row["Away"]]["GA"].append(row["Home Score"])
        seasonDict[row["Away"]]["G"].append(row["Away Score"])
        seasonDict[row["Home"]]["GA"].append(row["Away Score"])
        seasonDict[row["Away"]]["GP"] += 1
        seasonDict[row["Home"]]["GP"] += 1

    for key in dict:
        stats[key] = dict[key]
    stats.to_csv("./csv_data/" + league + "/preMatchAverages.csv", index = False)

def train_test_split(league):
    data = pd.read_csv("./csv_data/" + league + "/preMatchAverages.csv", encoding = "ISO-8859-1")
    test = False
    trainRows = []
    testRows = []
    for index, row in data.iterrows():
        #used to be 2017
        if (row["Date"].split("-")[0] == "2017" and abs(datetime.date(int(row["Date"].split("-")[0]), int(row["Date"].split("-")[1]), int(row["Date"].split("-")[2])) - datetime.date(int(data.at[index-1,"Date"].split("-")[0]), int(data.at[index-1,"Date"].split("-")[1]), int(data.at[index-1,"Date"].split("-")[2]))).days > 30):
            test = True
        if (test):
            testRows.append(index)
        else:
            trainRows.append(index)
    data.iloc[trainRows].to_csv("./csv_data/" + league + "/train.csv", index = False)
    data.iloc[testRows].to_csv("./csv_data/" + league + "/test.csv", index = False)

def split_by_league(nation):
    pred = pd.read_csv("./csv_data/" + nation + "/bayes_predictions_experimental.csv", encoding = "ISO-8859-1")
    for league in pred.League.unique():
        if (not exists("./csv_data/" + nation + "/" + league)):
            os.makedirs("./csv_data/" + nation + "/" + league)
        pred.loc[pred["League"] == league].to_csv("./csv_data/" + nation + "/" + league + "/bayes_predictions_experimental.csv", index = False)

def merge_betting_footy(league):
    betting = pd.read_csv("./csv_data/" + league + "/betting.csv", encoding = "ISO-8859-1")
    for i in range(len(betting.index)):
        try:
            betting.at[i, "Date"] = datetime.date(int(betting.at[i, "Date"].split("-")[0]), int(betting.at[i, "Date"].split("-")[1]), int(betting.at[i, "Date"].split("-")[2]))
        except:
            betting.at[i, "Date"] = datetime.date(int(betting.at[i, "Date"].split("/")[2]), int(betting.at[i, "Date"].split("/")[0]), int(betting.at[i, "Date"].split("/")[1]))
    footy = pd.read_csv("./csv_data/" + league + "/footystats.csv", encoding = "ISO-8859-1")
    for i in range(len(footy.index)):
        footy.at[i, "Date"] = datetime.date(int(footy.at[i, "Date"].split()[0].split("-")[0]), int(footy.at[i, "Date"].split()[0].split("-")[1]), int(footy.at[i, "Date"].split()[0].split("-")[2]))
        footy.at[i, "Home"] = standardizeTeamName(footy.at[i, "Home"], league)
        footy.at[i, "Away"] = standardizeTeamName(footy.at[i, "Away"], league)
    betting_teams = betting.Home.unique()
    footy_teams = footy.Home.unique()
    team_map = {}
    for x in betting_teams:
        cur_best = 0
        for y in footy_teams:
            if (fuzz.ratio(x, y) > cur_best):
                cur_best = fuzz.ratio(x, y)
                team_map[x] = y
    print (team_map)
    print (betting_teams)
    print (footy_teams)

    newcols = {"h_xg":[],"a_xg":[],"Season":[]}
    match_inds = []
    for i in range(len(footy.index)):
        match_inds.append(i)
    for index, row in betting.iterrows():
        found = False
        for i in match_inds:
            if (footy.at[i, "Home"] == team_map[row["Home"]] and footy.at[i, "Away"] == team_map[row["Away"]] and abs(row["Date"] - footy.at[i, "Date"]).days <= 5):
                newcols["h_xg"].append(footy.at[i, "h_xg"])
                newcols["a_xg"].append(footy.at[i, "a_xg"])
                newcols["Season"].append(footy.at[i, "Season"])
                match_inds.remove(i)
                found = True
                break
        if (not found):
            newcols["h_xg"].append(row["Home Score"])
            newcols["a_xg"].append(row["Away Score"])
            newcols["Season"].append(np.nan)
    betting["h_xg"] = newcols["h_xg"]
    betting["a_xg"] = newcols["a_xg"]
    betting["Season"] = newcols["Season"]
    betting.to_csv("./csv_data/" + league + "/betting_xg.csv",index = False)
