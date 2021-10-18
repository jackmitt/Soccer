import pandas as pd
import numpy as np
import datetime
import gc
import rpy2.robjects as robjects
import os
from WeibullCountModelFunctions.MLE import MLE
from WeibullCountModelFunctions.WeibullPMF import weibullPmf
from WeibullCountModelFunctions.frankCopula import copula
from sklearn.utils import shuffle
import random
import time

#just a helper function for preMatchAverages
def form(a, b, g):
    rA = []
    rB = []
    for i in reversed(a):
        rA.append(i)
        if (len(rA) == g):
            break
    for i in reversed(b):
        rB.append(i)
        if (len(rB) == g):
            break
    return ((np.average(rA) + np.average(rB))/2)

#needs the allRawData df, number of games to consider for form
#returns bigboy df
def preMatchAverages(data, g, fg = 3):
    print ("--preMatchAverages--")
    try:
        data = data.drop(columns=["Unnamed: 0"])
    except:
        pass
    dict = {}
    #X indicates opponent's stat, T adjusts for recent performance, E adjusts for quality of opponent
    sides = ["", "X_"]
    timeAdjCats = ["", "T_"]
    haSide = ["home_expected_", "away_expected_"]
    #initialization
    for side in haSide:
        for tCat in timeAdjCats:
            dict[tCat + side + "ball_winning"] = []
            dict[tCat + side + "chance_efficiency"] = []
            dict[tCat + side + "shooting_efficiency"] = []
            dict[tCat + side + "key_pass_pct"] = []
            dict[tCat + side + "pass_success"] = []
            dict[tCat + side + "dribble_success"] = []
            dict[tCat + side + "tackle_success"] = []
            dict[tCat + side + "xG"] = []
            dict[tCat + side + "xPts"] = []
            dict[tCat + side + "deep_pct"] = []
            dict[tCat + side + "pass_to_touch_ratio"] = []
            dict[tCat + side + "foul_rate"] = []
            dict[tCat + side + "clear_rate"] = []
            dict[tCat + side + "long_pass_pct"] = []
            dict[tCat + side + "fwd_pass_pct"] = []
            dict[tCat + side + "fwd_pass_aggressiveness"] = []
            dict[tCat + side + "defensive_third_pct"] = []
            dict[tCat + side + "final_third_pct"] = []
            dict[tCat + side + "ppda"] = []
            #newly added
            dict[tCat + side + "touch_aggression"] = []
            dict[tCat + side + "pass_aggression"] = []
            dict[tCat + side + "dribble_aggression"] = []
            dict[tCat + side + "tackle_aggression"] = []
            dict[tCat + side + "corner_rate"] = []
            dict[tCat + side + "dispossession_rate"] = []
            dict[tCat + side + "offsides_rate"] = []
            dict[tCat + side + "cross_rate"] = []
            dict[tCat + side + "through_rate"] = []
            dict[tCat + side + "xG_aggression_adjustment"] = []
            dict[tCat + side + "xG_efficiency"] = []
        dict["E_" + side + "ball_winning"] = []
        dict["E_" + side + "chance_efficiency"] = []
        dict["E_" + side + "shooting_efficiency"] = []
        dict["E_" + side + "key_pass_pct"] = []
        dict["E_" + side + "pass_success"] = []
        dict["E_" + side + "dribble_success"] = []
        dict["E_" + side + "tackle_success"] = []
        dict["E_" + side + "xG"] = []
        dict["E_" + side + "xPts"] = []
        #newly added
        dict["E_" + side + "xG_aggression_adjustment"] = []
        dict["E_" + side + "xG_efficiency"] = []

    droprows = []
    for index, row in data.iterrows():
        if (row["Home"] == row["Away"]):
            droprows.append(index)
    data = data.drop(droprows)
    data.to_csv("./EPL_Csvs/allRawData.csv")
    data = pd.read_csv('./EPL_Csvs/allRawData.csv', encoding = "ISO-8859-1").drop(columns=["Unnamed: 0"])

    beenSeptember = True
    for index, row in data.iterrows():
        # for col in data.columns:
        #     print (col, row[col])
        gc.collect()
        #initialization
        if (index == 0 or (row["Date"].split("-")[1] != "May" and data.at[index-1, "Date"].split("-")[1] == "May")):
            seasonDict = {}
            curIndex = index
            while (curIndex < len(data.index) and int(data.iat[curIndex, 0].split("-")[2]) != int(row["Date"].split("-")[2]) + 1):
                if (data.iat[curIndex, 1] not in seasonDict):
                    seasonDict[data.iat[curIndex, 1]] = {}
                    for side in sides:
                        seasonDict[data.iat[curIndex, 1]][side + "ball_winning"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "chance_efficiency"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "shooting_efficiency"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "key_pass_pct"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "pass_success"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "dribble_success"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "tackle_success"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "xG"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "xPts"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "deep_pct"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "pass_to_touch_ratio"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "foul_rate"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "clear_rate"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "long_pass_pct"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "fwd_pass_pct"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "fwd_pass_aggressiveness"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "defensive_third_pct"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "final_third_pct"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "ppda"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "touch_aggression"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "pass_aggression"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "dribble_aggression"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "tackle_aggression"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "corner_rate"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "dispossession_rate"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "offsides_rate"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "cross_rate"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "through_rate"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "xG_aggression_adjustment"] = []
                        seasonDict[data.iat[curIndex, 1]][side + "xG_efficiency"] = []
                        seasonDict[data.iat[curIndex, 1]]["E_" + side + "ball_winning"] = []
                        seasonDict[data.iat[curIndex, 1]]["E_" + side + "chance_efficiency"] = []
                        seasonDict[data.iat[curIndex, 1]]["E_" + side + "shooting_efficiency"] = []
                        seasonDict[data.iat[curIndex, 1]]["E_" + side + "key_pass_pct"] = []
                        seasonDict[data.iat[curIndex, 1]]["E_" + side + "pass_success"] = []
                        seasonDict[data.iat[curIndex, 1]]["E_" + side + "dribble_success"] = []
                        seasonDict[data.iat[curIndex, 1]]["E_" + side + "tackle_success"] = []
                        seasonDict[data.iat[curIndex, 1]]["E_" + side + "xG"] = []
                        seasonDict[data.iat[curIndex, 1]]["E_" + side + "xPts"] = []
                        seasonDict[data.iat[curIndex, 1]]["E_" + side + "xG_aggression_adjustment"] = []
                        seasonDict[data.iat[curIndex, 1]]["E_" + side + "xG_efficiency"] = []
                curIndex += 1
        #pre-match average calculations
        if (len(seasonDict[row["Home"]]["ball_winning"]) == 0 or len(seasonDict[row["Away"]]["ball_winning"]) == 0):
            for side in haSide:
                for tCat in timeAdjCats:
                    dict[tCat + side + "ball_winning"].append(np.nan)
                    dict[tCat + side + "chance_efficiency"].append(np.nan)
                    dict[tCat + side + "shooting_efficiency"].append(np.nan)
                    dict[tCat + side + "key_pass_pct"].append(np.nan)
                    dict[tCat + side + "pass_success"].append(np.nan)
                    dict[tCat + side + "dribble_success"].append(np.nan)
                    dict[tCat + side + "tackle_success"].append(np.nan)
                    dict[tCat + side + "xG"].append(np.nan)
                    dict[tCat + side + "xPts"].append(np.nan)
                    dict[tCat + side + "deep_pct"].append(np.nan)
                    dict[tCat + side + "pass_to_touch_ratio"].append(np.nan)
                    dict[tCat + side + "foul_rate"].append(np.nan)
                    dict[tCat + side + "clear_rate"].append(np.nan)
                    dict[tCat + side + "long_pass_pct"].append(np.nan)
                    dict[tCat + side + "fwd_pass_pct"].append(np.nan)
                    dict[tCat + side + "fwd_pass_aggressiveness"].append(np.nan)
                    dict[tCat + side + "defensive_third_pct"].append(np.nan)
                    dict[tCat + side + "final_third_pct"].append(np.nan)
                    dict[tCat + side + "ppda"].append(np.nan)
                    dict[tCat + side + "touch_aggression"].append(np.nan)
                    dict[tCat + side + "pass_aggression"].append(np.nan)
                    dict[tCat + side + "dribble_aggression"].append(np.nan)
                    dict[tCat + side + "tackle_aggression"].append(np.nan)
                    dict[tCat + side + "corner_rate"].append(np.nan)
                    dict[tCat + side + "dispossession_rate"].append(np.nan)
                    dict[tCat + side + "offsides_rate"].append(np.nan)
                    dict[tCat + side + "cross_rate"].append(np.nan)
                    dict[tCat + side + "through_rate"].append(np.nan)
                    dict[tCat + side + "xG_aggression_adjustment"].append(np.nan)
                    dict[tCat + side + "xG_efficiency"].append(np.nan)
                dict["E_" + side + "ball_winning"].append(np.nan)
                dict["E_" + side + "chance_efficiency"].append(np.nan)
                dict["E_" + side + "shooting_efficiency"].append(np.nan)
                dict["E_" + side + "key_pass_pct"].append(np.nan)
                dict["E_" + side + "pass_success"].append(np.nan)
                dict["E_" + side + "dribble_success"].append(np.nan)
                dict["E_" + side + "tackle_success"].append(np.nan)
                dict["E_" + side + "xG"].append(np.nan)
                dict["E_" + side + "xPts"].append(np.nan)
                dict["E_" + side + "xG_aggression_adjustment"].append(np.nan)
                dict["E_" + side + "xG_efficiency"].append(np.nan)
        else:
            for side in haSide:
                for tCat in timeAdjCats:
                    if (side == "home_expected_" and tCat == ""):
                        dict[tCat + side + "ball_winning"].append((np.average(seasonDict[row["Home"]]["" + "ball_winning"]) + np.average(seasonDict[row["Away"]]["X_" + "ball_winning"])) / 2)
                        dict[tCat + side + "chance_efficiency"].append((np.average(seasonDict[row["Home"]]["" + "chance_efficiency"]) + np.average(seasonDict[row["Away"]]["X_" + "chance_efficiency"])) / 2)
                        dict[tCat + side + "shooting_efficiency"].append((np.average(seasonDict[row["Home"]]["" + "shooting_efficiency"]) + np.average(seasonDict[row["Away"]]["X_" + "shooting_efficiency"])) / 2)
                        dict[tCat + side + "key_pass_pct"].append((np.average(seasonDict[row["Home"]]["" + "key_pass_pct"]) + np.average(seasonDict[row["Away"]]["X_" + "key_pass_pct"])) / 2)
                        dict[tCat + side + "pass_success"].append((np.average(seasonDict[row["Home"]]["" + "pass_success"]) + np.average(seasonDict[row["Away"]]["X_" + "pass_success"])) / 2)
                        dict[tCat + side + "dribble_success"].append((np.average(seasonDict[row["Home"]]["" + "dribble_success"]) + np.average(seasonDict[row["Away"]]["X_" + "dribble_success"])) / 2)
                        dict[tCat + side + "tackle_success"].append((np.average(seasonDict[row["Home"]]["" + "tackle_success"]) + np.average(seasonDict[row["Away"]]["X_" + "tackle_success"])) / 2)
                        dict[tCat + side + "xG"].append((np.average(seasonDict[row["Home"]]["" + "xG"]) + np.average(seasonDict[row["Away"]]["X_" + "xG"])) / 2)
                        dict[tCat + side + "xPts"].append((np.average(seasonDict[row["Home"]]["" + "xPts"]) + np.average(seasonDict[row["Away"]]["X_" + "xPts"])) / 2)
                        dict[tCat + side + "deep_pct"].append((np.average(seasonDict[row["Home"]]["" + "deep_pct"]) + np.average(seasonDict[row["Away"]]["X_" + "deep_pct"])) / 2)
                        dict[tCat + side + "pass_to_touch_ratio"].append((np.average(seasonDict[row["Home"]]["" + "pass_to_touch_ratio"]) + np.average(seasonDict[row["Away"]]["X_" + "pass_to_touch_ratio"])) / 2)
                        dict[tCat + side + "foul_rate"].append((np.average(seasonDict[row["Home"]]["" + "foul_rate"]) + np.average(seasonDict[row["Away"]]["X_" + "foul_rate"])) / 2)
                        dict[tCat + side + "clear_rate"].append((np.average(seasonDict[row["Home"]]["" + "clear_rate"]) + np.average(seasonDict[row["Away"]]["X_" + "clear_rate"])) / 2)
                        dict[tCat + side + "long_pass_pct"].append((np.average(seasonDict[row["Home"]]["" + "long_pass_pct"]) + np.average(seasonDict[row["Away"]]["X_" + "long_pass_pct"])) / 2)
                        dict[tCat + side + "fwd_pass_pct"].append((np.average(seasonDict[row["Home"]]["" + "fwd_pass_pct"]) + np.average(seasonDict[row["Away"]]["X_" + "fwd_pass_pct"])) / 2)
                        dict[tCat + side + "fwd_pass_aggressiveness"].append((np.average(seasonDict[row["Home"]]["" + "fwd_pass_aggressiveness"]) + np.average(seasonDict[row["Away"]]["X_" + "fwd_pass_aggressiveness"])) / 2)
                        dict[tCat + side + "defensive_third_pct"].append((np.average(seasonDict[row["Home"]]["" + "defensive_third_pct"]) + np.average(seasonDict[row["Away"]]["X_" + "defensive_third_pct"])) / 2)
                        dict[tCat + side + "final_third_pct"].append((np.average(seasonDict[row["Home"]]["" + "final_third_pct"]) + np.average(seasonDict[row["Away"]]["X_" + "final_third_pct"])) / 2)
                        dict[tCat + side + "ppda"].append((np.average(seasonDict[row["Home"]]["" + "ppda"]) + np.average(seasonDict[row["Away"]]["X_" + "ppda"])) / 2)
                        dict[tCat + side + "touch_aggression"].append((np.average(seasonDict[row["Home"]]["" + "touch_aggression"]) + np.average(seasonDict[row["Away"]]["X_" + "touch_aggression"])) / 2)
                        dict[tCat + side + "pass_aggression"].append((np.average(seasonDict[row["Home"]]["" + "pass_aggression"]) + np.average(seasonDict[row["Away"]]["X_" + "pass_aggression"])) / 2)
                        dict[tCat + side + "dribble_aggression"].append((np.average(seasonDict[row["Home"]]["" + "dribble_aggression"]) + np.average(seasonDict[row["Away"]]["X_" + "dribble_aggression"])) / 2)
                        dict[tCat + side + "tackle_aggression"].append((np.average(seasonDict[row["Home"]]["" + "tackle_aggression"]) + np.average(seasonDict[row["Away"]]["X_" + "tackle_aggression"])) / 2)
                        dict[tCat + side + "corner_rate"].append((np.average(seasonDict[row["Home"]]["" + "corner_rate"]) + np.average(seasonDict[row["Away"]]["X_" + "corner_rate"])) / 2)
                        dict[tCat + side + "dispossession_rate"].append((np.average(seasonDict[row["Home"]]["" + "dispossession_rate"]) + np.average(seasonDict[row["Away"]]["X_" + "dispossession_rate"])) / 2)
                        dict[tCat + side + "offsides_rate"].append((np.average(seasonDict[row["Home"]]["" + "offsides_rate"]) + np.average(seasonDict[row["Away"]]["X_" + "offsides_rate"])) / 2)
                        dict[tCat + side + "cross_rate"].append((np.average(seasonDict[row["Home"]]["" + "cross_rate"]) + np.average(seasonDict[row["Away"]]["X_" + "cross_rate"])) / 2)
                        dict[tCat + side + "through_rate"].append((np.average(seasonDict[row["Home"]]["" + "through_rate"]) + np.average(seasonDict[row["Away"]]["X_" + "through_rate"])) / 2)
                        dict[tCat + side + "xG_aggression_adjustment"].append((np.average(seasonDict[row["Home"]]["" + "xG_aggression_adjustment"]) + np.average(seasonDict[row["Away"]]["X_" + "xG_aggression_adjustment"])) / 2)
                        dict[tCat + side + "xG_efficiency"].append((np.average(seasonDict[row["Home"]]["" + "xG_efficiency"]) + np.average(seasonDict[row["Away"]]["X_" + "xG_efficiency"])) / 2)
                    elif (side == "away_expected_" and tCat == ""):
                        dict[tCat + side + "ball_winning"].append((np.average(seasonDict[row["Away"]]["" + "ball_winning"]) + np.average(seasonDict[row["Home"]]["X_" + "ball_winning"])) / 2)
                        dict[tCat + side + "chance_efficiency"].append((np.average(seasonDict[row["Away"]]["" + "chance_efficiency"]) + np.average(seasonDict[row["Home"]]["X_" + "chance_efficiency"])) / 2)
                        dict[tCat + side + "shooting_efficiency"].append((np.average(seasonDict[row["Away"]]["" + "shooting_efficiency"]) + np.average(seasonDict[row["Home"]]["X_" + "shooting_efficiency"])) / 2)
                        dict[tCat + side + "key_pass_pct"].append((np.average(seasonDict[row["Away"]]["" + "key_pass_pct"]) + np.average(seasonDict[row["Home"]]["X_" + "key_pass_pct"])) / 2)
                        dict[tCat + side + "pass_success"].append((np.average(seasonDict[row["Away"]]["" + "pass_success"]) + np.average(seasonDict[row["Home"]]["X_" + "pass_success"])) / 2)
                        dict[tCat + side + "dribble_success"].append((np.average(seasonDict[row["Away"]]["" + "dribble_success"]) + np.average(seasonDict[row["Home"]]["X_" + "dribble_success"])) / 2)
                        dict[tCat + side + "tackle_success"].append((np.average(seasonDict[row["Away"]]["" + "tackle_success"]) + np.average(seasonDict[row["Home"]]["X_" + "tackle_success"])) / 2)
                        dict[tCat + side + "xG"].append((np.average(seasonDict[row["Away"]]["" + "xG"]) + np.average(seasonDict[row["Home"]]["X_" + "xG"])) / 2)
                        dict[tCat + side + "xPts"].append((np.average(seasonDict[row["Away"]]["" + "xPts"]) + np.average(seasonDict[row["Home"]]["X_" + "xPts"])) / 2)
                        dict[tCat + side + "deep_pct"].append((np.average(seasonDict[row["Away"]]["" + "deep_pct"]) + np.average(seasonDict[row["Home"]]["X_" + "deep_pct"])) / 2)
                        dict[tCat + side + "pass_to_touch_ratio"].append((np.average(seasonDict[row["Away"]]["" + "pass_to_touch_ratio"]) + np.average(seasonDict[row["Home"]]["X_" + "pass_to_touch_ratio"])) / 2)
                        dict[tCat + side + "foul_rate"].append((np.average(seasonDict[row["Away"]]["" + "foul_rate"]) + np.average(seasonDict[row["Home"]]["X_" + "foul_rate"])) / 2)
                        dict[tCat + side + "clear_rate"].append((np.average(seasonDict[row["Away"]]["" + "clear_rate"]) + np.average(seasonDict[row["Home"]]["X_" + "clear_rate"])) / 2)
                        dict[tCat + side + "long_pass_pct"].append((np.average(seasonDict[row["Away"]]["" + "long_pass_pct"]) + np.average(seasonDict[row["Home"]]["X_" + "long_pass_pct"])) / 2)
                        dict[tCat + side + "fwd_pass_pct"].append((np.average(seasonDict[row["Away"]]["" + "fwd_pass_pct"]) + np.average(seasonDict[row["Home"]]["X_" + "fwd_pass_pct"])) / 2)
                        dict[tCat + side + "fwd_pass_aggressiveness"].append((np.average(seasonDict[row["Away"]]["" + "fwd_pass_aggressiveness"]) + np.average(seasonDict[row["Home"]]["X_" + "fwd_pass_aggressiveness"])) / 2)
                        dict[tCat + side + "defensive_third_pct"].append((np.average(seasonDict[row["Away"]]["" + "defensive_third_pct"]) + np.average(seasonDict[row["Home"]]["X_" + "defensive_third_pct"])) / 2)
                        dict[tCat + side + "final_third_pct"].append((np.average(seasonDict[row["Away"]]["" + "final_third_pct"]) + np.average(seasonDict[row["Home"]]["X_" + "final_third_pct"])) / 2)
                        dict[tCat + side + "ppda"].append((np.average(seasonDict[row["Away"]]["" + "ppda"]) + np.average(seasonDict[row["Home"]]["X_" + "ppda"])) / 2)
                        dict[tCat + side + "touch_aggression"].append((np.average(seasonDict[row["Away"]]["" + "touch_aggression"]) + np.average(seasonDict[row["Home"]]["X_" + "touch_aggression"])) / 2)
                        dict[tCat + side + "pass_aggression"].append((np.average(seasonDict[row["Away"]]["" + "pass_aggression"]) + np.average(seasonDict[row["Home"]]["X_" + "pass_aggression"])) / 2)
                        dict[tCat + side + "dribble_aggression"].append((np.average(seasonDict[row["Away"]]["" + "dribble_aggression"]) + np.average(seasonDict[row["Home"]]["X_" + "dribble_aggression"])) / 2)
                        dict[tCat + side + "tackle_aggression"].append((np.average(seasonDict[row["Away"]]["" + "tackle_aggression"]) + np.average(seasonDict[row["Home"]]["X_" + "tackle_aggression"])) / 2)
                        dict[tCat + side + "corner_rate"].append((np.average(seasonDict[row["Away"]]["" + "corner_rate"]) + np.average(seasonDict[row["Home"]]["X_" + "corner_rate"])) / 2)
                        dict[tCat + side + "dispossession_rate"].append((np.average(seasonDict[row["Away"]]["" + "dispossession_rate"]) + np.average(seasonDict[row["Home"]]["X_" + "dispossession_rate"])) / 2)
                        dict[tCat + side + "offsides_rate"].append((np.average(seasonDict[row["Away"]]["" + "offsides_rate"]) + np.average(seasonDict[row["Home"]]["X_" + "offsides_rate"])) / 2)
                        dict[tCat + side + "cross_rate"].append((np.average(seasonDict[row["Away"]]["" + "cross_rate"]) + np.average(seasonDict[row["Home"]]["X_" + "cross_rate"])) / 2)
                        dict[tCat + side + "through_rate"].append((np.average(seasonDict[row["Away"]]["" + "through_rate"]) + np.average(seasonDict[row["Home"]]["X_" + "through_rate"])) / 2)
                        dict[tCat + side + "xG_aggression_adjustment"].append((np.average(seasonDict[row["Away"]]["" + "xG_aggression_adjustment"]) + np.average(seasonDict[row["Home"]]["X_" + "xG_aggression_adjustment"])) / 2)
                        dict[tCat + side + "xG_efficiency"].append((np.average(seasonDict[row["Away"]]["" + "xG_efficiency"]) + np.average(seasonDict[row["Home"]]["X_" + "xG_efficiency"])) / 2)
                    else:
                        if (len(seasonDict[row["Home"]]["" + "ball_winning"]) < g or len(seasonDict[row["Away"]]["" + "ball_winning"]) < g):
                            dict[tCat + side + "ball_winning"].append(np.nan)
                            dict[tCat + side + "chance_efficiency"].append(np.nan)
                            dict[tCat + side + "shooting_efficiency"].append(np.nan)
                            dict[tCat + side + "key_pass_pct"].append(np.nan)
                            dict[tCat + side + "pass_success"].append(np.nan)
                            dict[tCat + side + "dribble_success"].append(np.nan)
                            dict[tCat + side + "tackle_success"].append(np.nan)
                            dict[tCat + side + "xG"].append(np.nan)
                            dict[tCat + side + "xPts"].append(np.nan)
                            dict[tCat + side + "deep_pct"].append(np.nan)
                            dict[tCat + side + "pass_to_touch_ratio"].append(np.nan)
                            dict[tCat + side + "foul_rate"].append(np.nan)
                            dict[tCat + side + "clear_rate"].append(np.nan)
                            dict[tCat + side + "long_pass_pct"].append(np.nan)
                            dict[tCat + side + "fwd_pass_pct"].append(np.nan)
                            dict[tCat + side + "fwd_pass_aggressiveness"].append(np.nan)
                            dict[tCat + side + "defensive_third_pct"].append(np.nan)
                            dict[tCat + side + "final_third_pct"].append(np.nan)
                            dict[tCat + side + "ppda"].append(np.nan)
                            dict[tCat + side + "touch_aggression"].append(np.nan)
                            dict[tCat + side + "pass_aggression"].append(np.nan)
                            dict[tCat + side + "dribble_aggression"].append(np.nan)
                            dict[tCat + side + "tackle_aggression"].append(np.nan)
                            dict[tCat + side + "corner_rate"].append(np.nan)
                            dict[tCat + side + "dispossession_rate"].append(np.nan)
                            dict[tCat + side + "offsides_rate"].append(np.nan)
                            dict[tCat + side + "cross_rate"].append(np.nan)
                            dict[tCat + side + "through_rate"].append(np.nan)
                            dict[tCat + side + "xG_aggression_adjustment"].append(np.nan)
                            dict[tCat + side + "xG_efficiency"].append(np.nan)
                        elif (side == "home_expected_"):
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "ball_winning"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "ball_winning"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "ball_winning"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "chance_efficiency"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "chance_efficiency"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "chance_efficiency"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "shooting_efficiency"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "shooting_efficiency"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "shooting_efficiency"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "key_pass_pct"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "key_pass_pct"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "key_pass_pct"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "pass_success"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "pass_success"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "pass_success"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "dribble_success"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "dribble_success"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "dribble_success"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "tackle_success"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "tackle_success"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "tackle_success"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "xG"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "xG"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "xG"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "xPts"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "xPts"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "xPts"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "deep_pct"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "deep_pct"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "deep_pct"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "pass_to_touch_ratio"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "pass_to_touch_ratio"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "pass_to_touch_ratio"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "foul_rate"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "foul_rate"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "foul_rate"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "clear_rate"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "clear_rate"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "clear_rate"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "long_pass_pct"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "long_pass_pct"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "long_pass_pct"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "fwd_pass_pct"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "fwd_pass_pct"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "fwd_pass_pct"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "fwd_pass_aggressiveness"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "fwd_pass_aggressiveness"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "fwd_pass_aggressiveness"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "defensive_third_pct"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "defensive_third_pct"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "defensive_third_pct"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "final_third_pct"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "final_third_pct"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "final_third_pct"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "ppda"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "ppda"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "ppda"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "touch_aggression"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "touch_aggression"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "touch_aggression"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "pass_aggression"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "pass_aggression"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "pass_aggression"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "dribble_aggression"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "dribble_aggression"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "dribble_aggression"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "tackle_aggression"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "tackle_aggression"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "tackle_aggression"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "corner_rate"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "corner_rate"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "corner_rate"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "dispossession_rate"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "dispossession_rate"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "dispossession_rate"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "offsides_rate"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "offsides_rate"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "offsides_rate"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "cross_rate"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "cross_rate"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "cross_rate"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "through_rate"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "through_rate"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "through_rate"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "xG_aggression_adjustment"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "xG_aggression_adjustment"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "xG_aggression_adjustment"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Home"]]["" + "xG_efficiency"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Away"]]["X_" + "xG_efficiency"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "xG_efficiency"].append(form(tempH, tempA, fg))
                        else:
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "ball_winning"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "ball_winning"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "ball_winning"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "chance_efficiency"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "chance_efficiency"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "chance_efficiency"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "shooting_efficiency"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "shooting_efficiency"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "shooting_efficiency"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "key_pass_pct"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "key_pass_pct"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "key_pass_pct"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "pass_success"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "pass_success"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "pass_success"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "dribble_success"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "dribble_success"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "dribble_success"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "tackle_success"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "tackle_success"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "tackle_success"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "xG"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "xG"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "xG"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "xPts"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "xPts"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "xPts"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "deep_pct"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "deep_pct"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "deep_pct"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "pass_to_touch_ratio"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "pass_to_touch_ratio"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "pass_to_touch_ratio"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "foul_rate"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "foul_rate"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "foul_rate"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "clear_rate"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "clear_rate"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "clear_rate"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "long_pass_pct"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "long_pass_pct"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "long_pass_pct"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "fwd_pass_pct"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "fwd_pass_pct"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "fwd_pass_pct"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "fwd_pass_aggressiveness"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "fwd_pass_aggressiveness"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "fwd_pass_aggressiveness"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "defensive_third_pct"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "defensive_third_pct"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "defensive_third_pct"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "final_third_pct"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "final_third_pct"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "final_third_pct"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "ppda"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "ppda"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "ppda"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "touch_aggression"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "touch_aggression"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "touch_aggression"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "pass_aggression"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "pass_aggression"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "pass_aggression"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "dribble_aggression"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "dribble_aggression"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "dribble_aggression"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "tackle_aggression"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "tackle_aggression"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "tackle_aggression"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "corner_rate"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "corner_rate"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "corner_rate"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "dispossession_rate"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "dispossession_rate"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "dispossession_rate"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "offsides_rate"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "offsides_rate"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "offsides_rate"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "cross_rate"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "cross_rate"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "cross_rate"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "through_rate"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "through_rate"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "through_rate"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "xG_aggression_adjustment"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "xG_aggression_adjustment"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "xG_aggression_adjustment"].append(form(tempH, tempA, fg))
                            tempH = []
                            tempA = []
                            for stat in reversed(seasonDict[row["Away"]]["" + "xG_efficiency"]):
                                if (len(tempH) < g):
                                    tempH.append(stat)
                            for stat in reversed(seasonDict[row["Home"]]["X_" + "xG_efficiency"]):
                                if (len(tempA) < g):
                                    tempA.append(stat)
                            dict[tCat + side + "xG_efficiency"].append(form(tempH, tempA, fg))
                if (side == "home_expected_"):
                    dict["E_" + side + "ball_winning"].append((np.average(seasonDict[row["Home"]]["E_" + "ball_winning"]) + np.average(seasonDict[row["Away"]]["E_X_" + "ball_winning"])) / 2)
                    dict["E_" + side + "chance_efficiency"].append((np.average(seasonDict[row["Home"]]["E_" + "chance_efficiency"]) + np.average(seasonDict[row["Away"]]["E_X_" + "chance_efficiency"])) / 2)
                    dict["E_" + side + "shooting_efficiency"].append((np.average(seasonDict[row["Home"]]["E_" + "shooting_efficiency"]) + np.average(seasonDict[row["Away"]]["E_X_" + "shooting_efficiency"])) / 2)
                    dict["E_" + side + "key_pass_pct"].append((np.average(seasonDict[row["Home"]]["E_" + "key_pass_pct"]) + np.average(seasonDict[row["Away"]]["E_X_" + "key_pass_pct"])) / 2)
                    dict["E_" + side + "pass_success"].append((np.average(seasonDict[row["Home"]]["E_" + "pass_success"]) + np.average(seasonDict[row["Away"]]["E_X_" + "pass_success"])) / 2)
                    dict["E_" + side + "dribble_success"].append((np.average(seasonDict[row["Home"]]["E_" + "dribble_success"]) + np.average(seasonDict[row["Away"]]["E_X_" + "dribble_success"])) / 2)
                    dict["E_" + side + "tackle_success"].append((np.average(seasonDict[row["Home"]]["E_" + "tackle_success"]) + np.average(seasonDict[row["Away"]]["E_X_" + "tackle_success"])) / 2)
                    dict["E_" + side + "xG"].append((np.average(seasonDict[row["Home"]]["E_" + "xG"]) + np.average(seasonDict[row["Away"]]["E_X_" + "xG"])) / 2)
                    dict["E_" + side + "xPts"].append((np.average(seasonDict[row["Home"]]["E_" + "xPts"]) + np.average(seasonDict[row["Away"]]["E_X_" + "xPts"])) / 2)
                    dict["E_" + side + "xG_aggression_adjustment"].append((np.average(seasonDict[row["Home"]]["E_" + "xG_aggression_adjustment"]) + np.average(seasonDict[row["Away"]]["E_X_" + "xG_aggression_adjustment"])) / 2)
                    dict["E_" + side + "xG_efficiency"].append((np.average(seasonDict[row["Home"]]["E_" + "xG_efficiency"]) + np.average(seasonDict[row["Away"]]["E_X_" + "xG_efficiency"])) / 2)
                else:
                    dict["E_" + side + "ball_winning"].append((np.average(seasonDict[row["Away"]]["E_" + "ball_winning"]) + np.average(seasonDict[row["Home"]]["E_X_" + "ball_winning"])) / 2)
                    dict["E_" + side + "chance_efficiency"].append((np.average(seasonDict[row["Away"]]["E_" + "chance_efficiency"]) + np.average(seasonDict[row["Home"]]["E_X_" + "chance_efficiency"])) / 2)
                    dict["E_" + side + "shooting_efficiency"].append((np.average(seasonDict[row["Away"]]["E_" + "shooting_efficiency"]) + np.average(seasonDict[row["Home"]]["E_X_" + "shooting_efficiency"])) / 2)
                    dict["E_" + side + "key_pass_pct"].append((np.average(seasonDict[row["Away"]]["E_" + "key_pass_pct"]) + np.average(seasonDict[row["Home"]]["E_X_" + "key_pass_pct"])) / 2)
                    dict["E_" + side + "pass_success"].append((np.average(seasonDict[row["Away"]]["E_" + "pass_success"]) + np.average(seasonDict[row["Home"]]["E_X_" + "pass_success"])) / 2)
                    dict["E_" + side + "dribble_success"].append((np.average(seasonDict[row["Away"]]["E_" + "dribble_success"]) + np.average(seasonDict[row["Home"]]["E_X_" + "dribble_success"])) / 2)
                    dict["E_" + side + "tackle_success"].append((np.average(seasonDict[row["Away"]]["E_" + "tackle_success"]) + np.average(seasonDict[row["Home"]]["E_X_" + "tackle_success"])) / 2)
                    dict["E_" + side + "xG"].append((np.average(seasonDict[row["Away"]]["E_" + "xG"]) + np.average(seasonDict[row["Home"]]["E_X_" + "xG"])) / 2)
                    dict["E_" + side + "xPts"].append((np.average(seasonDict[row["Away"]]["E_" + "xPts"]) + np.average(seasonDict[row["Home"]]["E_X_" + "xPts"])) / 2)
                    dict["E_" + side + "xG_aggression_adjustment"].append((np.average(seasonDict[row["Away"]]["E_" + "xG_aggression_adjustment"]) + np.average(seasonDict[row["Home"]]["E_X_" + "xG_aggression_adjustment"])) / 2)
                    dict["E_" + side + "xG_efficiency"].append((np.average(seasonDict[row["Away"]]["E_" + "xG_efficiency"]) + np.average(seasonDict[row["Home"]]["E_X_" + "xG_efficiency"])) / 2)
        #print (dict)
        #addition of the current game to the lists for each team
        for side in sides:
            if (side == ""):
                seasonDict[row["Home"]][side + "ball_winning"].append(float(row["Home Interceptions"]) / float(row["Away Total Passes"]))
                seasonDict[row["Home"]][side + "chance_efficiency"].append(float(row["Home xG"]) * 100 / float(row["Home Possession"]))
                seasonDict[row["Home"]][side + "shooting_efficiency"].append(float(row["Home Score"]) - float(row["Home xG"]))
                seasonDict[row["Home"]][side + "key_pass_pct"].append(float(row["Home Key Passes"]) / float(row["Home passzone_final_third"]))
                seasonDict[row["Home"]][side + "pass_success"].append(float(row["Home Accurate Passes"]) / float(row["Home Total Passes"]))
                seasonDict[row["Home"]][side + "dribble_success"].append(float(row["Home Dribbles Won"]) / float(row["Home Dribbles Attempted"]))
                seasonDict[row["Home"]][side + "tackle_success"].append(float(row["Home Successful Tackles"]) / float(row["Home Tackles Attempted"]))
                seasonDict[row["Home"]][side + "xG"].append(row["Home xG"])
                seasonDict[row["Home"]][side + "xPts"].append(row["Home xPts"])
                seasonDict[row["Home"]][side + "deep_pct"].append(float(row["Home deep"]) / float(row["Home Accurate Passes"]))
                seasonDict[row["Home"]][side + "pass_to_touch_ratio"].append(float(row["Home Total Passes"]) / float(row["Home Touches"]))
                seasonDict[row["Home"]][side + "foul_rate"].append(float(row["Home Fouls"]) / float(row["Away Possession"]))
                seasonDict[row["Home"]][side + "clear_rate"].append(float(row["Home Clearances"]) / float(row["Away passzone_final_third"]))
                seasonDict[row["Home"]][side + "long_pass_pct"].append(float(row["Home passlength_long"]) / (float(row["Home passlength_long"]) + float(row["Home passlength_short"])))
                seasonDict[row["Home"]][side + "fwd_pass_pct"].append(float(row["Home passdirection_forward"]) / (float(row["Home passdirection_backward"]) + float(row["Home passdirection_left"]) + float(row["Home passdirection_right"]) + float(row["Home passdirection_forward"])))
                seasonDict[row["Home"]][side + "fwd_pass_aggressiveness"].append(float(row["Home passdirection_forward"]) * float(row["Home Possession"]) / (float(row["Home passdirection_backward"]) + float(row["Home passdirection_left"]) + float(row["Home passdirection_right"])))
                seasonDict[row["Home"]][side + "defensive_third_pct"].append(float(row["Home passzone_defensive_third"]) / (float(row["Home passzone_defensive_third"]) + float(row["Home passzone_middle_third"]) + float(row["Home passzone_final_third"])))
                seasonDict[row["Home"]][side + "final_third_pct"].append(float(row["Home passzone_final_third"]) / (float(row["Home passzone_defensive_third"]) + float(row["Home passzone_middle_third"]) + float(row["Home passzone_final_third"])))
                seasonDict[row["Home"]][side + "ppda"].append(row["Home ppda"])
                seasonDict[row["Home"]][side + "touch_aggression"].append(float(row["Home Touches"]) / float(row["Home Possession"]))
                seasonDict[row["Home"]][side + "pass_aggression"].append(float(row["Home Total Passes"]) / float(row["Home Possession"]))
                seasonDict[row["Home"]][side + "dribble_aggression"].append(float(row["Home Dribbles Attempted"]) / float(row["Home Possession"]))
                seasonDict[row["Home"]][side + "tackle_aggression"].append(float(row["Home Tackles Attempted"]) / float(row["Away Possession"]))
                seasonDict[row["Home"]][side + "corner_rate"].append(float(row["Home passtype_corner"]) / float(row["Home passzone_final_third"]))
                seasonDict[row["Home"]][side + "dispossession_rate"].append(float(row["Home Dispossessed"]) / float(row["Home Possession"]))
                seasonDict[row["Home"]][side + "offsides_rate"].append(float(row["Home Offsides"]) / float(row["Home Total Passes"]))
                seasonDict[row["Home"]][side + "cross_rate"].append(float(row["Home passtype_cross"]) / float(row["Home passzone_final_third"]))
                seasonDict[row["Home"]][side + "through_rate"].append(float(row["Home passtype_through"]) / float(row["Home passzone_final_third"]))
                seasonDict[row["Home"]][side + "xG_aggression_adjustment"].append(float(row["Home xG"]) * float(row["Home ppda"]))
                seasonDict[row["Home"]][side + "xG_efficiency"].append(float(row["Home xG"]) / float(row["Home passzone_final_third"]))
                seasonDict[row["Home"]]["E_" + side + "ball_winning"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Interceptions"]) / float(row["Away Total Passes"]))
                seasonDict[row["Home"]]["E_" + side + "chance_efficiency"].append((float(row["Away Pre Elo"])/1500) * float(row["Home xG"]) * 100 / float(row["Home Possession"]))
                seasonDict[row["Home"]]["E_" + side + "shooting_efficiency"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Score"]) - float(row["Home xG"]))
                seasonDict[row["Home"]]["E_" + side + "key_pass_pct"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Key Passes"]) / float(row["Home passzone_final_third"]))
                seasonDict[row["Home"]]["E_" + side + "pass_success"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Accurate Passes"]) / float(row["Home Total Passes"]))
                seasonDict[row["Home"]]["E_" + side + "dribble_success"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Dribbles Won"]) / float(row["Home Dribbles Attempted"]))
                seasonDict[row["Home"]]["E_" + side + "tackle_success"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Successful Tackles"]) / float(row["Home Tackles Attempted"]))
                seasonDict[row["Home"]]["E_" + side + "xG"].append((float(row["Away Pre Elo"])/1500) * row["Home xG"])
                seasonDict[row["Home"]]["E_" + side + "xPts"].append((float(row["Away Pre Elo"])/1500) * row["Home xPts"])
                seasonDict[row["Home"]]["E_" + side + "xG_aggression_adjustment"].append((float(row["Away Pre Elo"])/1500)  * (float(row["Home xG"]) * float(row["Home ppda"])))
                seasonDict[row["Home"]]["E_" + side + "xG_efficiency"].append((float(row["Away Pre Elo"])/1500)  * (float(row["Home xG"]) / float(row["Home passzone_final_third"])))
                seasonDict[row["Away"]][side + "ball_winning"].append(float(row["Away Interceptions"]) / float(row["Home Total Passes"]))
                seasonDict[row["Away"]][side + "chance_efficiency"].append(float(row["Away xG"]) * 100 / float(row["Away Possession"]))
                seasonDict[row["Away"]][side + "shooting_efficiency"].append(float(row["Away Score"]) - float(row["Away xG"]))
                seasonDict[row["Away"]][side + "key_pass_pct"].append(float(row["Away Key Passes"]) / float(row["Away passzone_final_third"]))
                seasonDict[row["Away"]][side + "pass_success"].append(float(row["Away Accurate Passes"]) / float(row["Away Total Passes"]))
                seasonDict[row["Away"]][side + "dribble_success"].append(float(row["Away Dribbles Won"]) / float(row["Away Dribbles Attempted"]))
                seasonDict[row["Away"]][side + "tackle_success"].append(float(row["Away Successful Tackles"]) / float(row["Away Tackles Attempted"]))
                seasonDict[row["Away"]][side + "xG"].append(row["Away xG"])
                seasonDict[row["Away"]][side + "xPts"].append(row["Away xPts"])
                seasonDict[row["Away"]][side + "deep_pct"].append(float(row["Away deep"]) / float(row["Away Accurate Passes"]))
                seasonDict[row["Away"]][side + "pass_to_touch_ratio"].append(float(row["Away Total Passes"]) / float(row["Away Touches"]))
                seasonDict[row["Away"]][side + "foul_rate"].append(float(row["Away Fouls"]) / float(row["Home Possession"]))
                seasonDict[row["Away"]][side + "clear_rate"].append(float(row["Away Clearances"]) / float(row["Home passzone_final_third"]))
                seasonDict[row["Away"]][side + "long_pass_pct"].append(float(row["Away passlength_long"]) / (float(row["Away passlength_long"]) + float(row["Away passlength_short"])))
                seasonDict[row["Away"]][side + "fwd_pass_pct"].append(float(row["Away passdirection_forward"]) / (float(row["Away passdirection_backward"]) + float(row["Away passdirection_left"]) + float(row["Away passdirection_right"]) + float(row["Away passdirection_forward"])))
                seasonDict[row["Away"]][side + "fwd_pass_aggressiveness"].append(float(row["Away passdirection_forward"]) * float(row["Away Possession"]) / (float(row["Away passdirection_backward"]) + float(row["Away passdirection_left"]) + float(row["Away passdirection_right"])))
                seasonDict[row["Away"]][side + "defensive_third_pct"].append(float(row["Away passzone_defensive_third"]) / (float(row["Away passzone_defensive_third"]) + float(row["Away passzone_middle_third"]) + float(row["Away passzone_final_third"])))
                seasonDict[row["Away"]][side + "final_third_pct"].append(float(row["Away passzone_final_third"]) / (float(row["Away passzone_defensive_third"]) + float(row["Away passzone_middle_third"]) + float(row["Away passzone_final_third"])))
                seasonDict[row["Away"]][side + "ppda"].append(row["Away ppda"])
                seasonDict[row["Away"]][side + "touch_aggression"].append(float(row["Away Touches"]) / float(row["Away Possession"]))
                seasonDict[row["Away"]][side + "pass_aggression"].append(float(row["Away Total Passes"]) / float(row["Away Possession"]))
                seasonDict[row["Away"]][side + "dribble_aggression"].append(float(row["Away Dribbles Attempted"]) / float(row["Away Possession"]))
                seasonDict[row["Away"]][side + "tackle_aggression"].append(float(row["Away Tackles Attempted"]) / float(row["Home Possession"]))
                seasonDict[row["Away"]][side + "corner_rate"].append(float(row["Away passtype_corner"]) / float(row["Away passzone_final_third"]))
                seasonDict[row["Away"]][side + "dispossession_rate"].append(float(row["Away Dispossessed"]) / float(row["Away Possession"]))
                seasonDict[row["Away"]][side + "offsides_rate"].append(float(row["Away Offsides"]) / float(row["Away Total Passes"]))
                seasonDict[row["Away"]][side + "cross_rate"].append(float(row["Away passtype_cross"]) / float(row["Away passzone_final_third"]))
                seasonDict[row["Away"]][side + "through_rate"].append(float(row["Away passtype_through"]) / float(row["Away passzone_final_third"]))
                seasonDict[row["Away"]][side + "xG_aggression_adjustment"].append(float(row["Away xG"]) * float(row["Away ppda"]))
                seasonDict[row["Away"]][side + "xG_efficiency"].append(float(row["Away xG"]) / float(row["Away passzone_final_third"]))
                seasonDict[row["Away"]]["E_" + side + "ball_winning"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Interceptions"]) / float(row["Home Total Passes"]))
                seasonDict[row["Away"]]["E_" + side + "chance_efficiency"].append((float(row["Home Pre Elo"])/1500) * float(row["Away xG"]) * 100 / float(row["Away Possession"]))
                seasonDict[row["Away"]]["E_" + side + "shooting_efficiency"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Score"]) - float(row["Away xG"]))
                seasonDict[row["Away"]]["E_" + side + "key_pass_pct"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Key Passes"]) / float(row["Away passzone_final_third"]))
                seasonDict[row["Away"]]["E_" + side + "pass_success"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Accurate Passes"]) / float(row["Away Total Passes"]))
                seasonDict[row["Away"]]["E_" + side + "dribble_success"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Dribbles Won"]) / float(row["Away Dribbles Attempted"]))
                seasonDict[row["Away"]]["E_" + side + "tackle_success"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Successful Tackles"]) / float(row["Away Tackles Attempted"]))
                seasonDict[row["Away"]]["E_" + side + "xG"].append((float(row["Home Pre Elo"])/1500) * row["Away xG"])
                seasonDict[row["Away"]]["E_" + side + "xPts"].append((float(row["Home Pre Elo"])/1500) * row["Away xPts"])
                seasonDict[row["Away"]]["E_" + side + "xG_aggression_adjustment"].append((float(row["Home Pre Elo"])/1500)  * (float(row["Away xG"]) * float(row["Away ppda"])))
                seasonDict[row["Away"]]["E_" + side + "xG_efficiency"].append((float(row["Home Pre Elo"])/1500)  * (float(row["Away xG"]) / float(row["Away passzone_final_third"])))
            else:
                seasonDict[row["Away"]][side + "ball_winning"].append(float(row["Home Interceptions"]) / float(row["Away Total Passes"]))
                seasonDict[row["Away"]][side + "chance_efficiency"].append(float(row["Home xG"]) * 100 / float(row["Home Possession"]))
                seasonDict[row["Away"]][side + "shooting_efficiency"].append(float(row["Home Score"]) - float(row["Home xG"]))
                seasonDict[row["Away"]][side + "key_pass_pct"].append(float(row["Home Key Passes"]) / float(row["Home passzone_final_third"]))
                seasonDict[row["Away"]][side + "pass_success"].append(float(row["Home Accurate Passes"]) / float(row["Home Total Passes"]))
                seasonDict[row["Away"]][side + "dribble_success"].append(float(row["Home Dribbles Won"]) / float(row["Home Dribbles Attempted"]))
                seasonDict[row["Away"]][side + "tackle_success"].append(float(row["Home Successful Tackles"]) / float(row["Home Tackles Attempted"]))
                seasonDict[row["Away"]][side + "xG"].append(row["Home xG"])
                seasonDict[row["Away"]][side + "xPts"].append(row["Home xPts"])
                seasonDict[row["Away"]][side + "deep_pct"].append(float(row["Home deep"]) / float(row["Home Accurate Passes"]))
                seasonDict[row["Away"]][side + "pass_to_touch_ratio"].append(float(row["Home Total Passes"]) / float(row["Home Touches"]))
                seasonDict[row["Away"]][side + "foul_rate"].append(float(row["Home Fouls"]) / float(row["Away Possession"]))
                seasonDict[row["Away"]][side + "clear_rate"].append(float(row["Home Clearances"]) / float(row["Away passzone_final_third"]))
                seasonDict[row["Away"]][side + "long_pass_pct"].append(float(row["Home passlength_long"]) / (float(row["Home passlength_long"]) + float(row["Home passlength_short"])))
                seasonDict[row["Away"]][side + "fwd_pass_pct"].append(float(row["Home passdirection_forward"]) / (float(row["Home passdirection_backward"]) + float(row["Home passdirection_left"]) + float(row["Home passdirection_right"]) + float(row["Home passdirection_forward"])))
                seasonDict[row["Away"]][side + "fwd_pass_aggressiveness"].append(float(row["Home passdirection_forward"]) * float(row["Home Possession"]) / (float(row["Home passdirection_backward"]) + float(row["Home passdirection_left"]) + float(row["Home passdirection_right"])))
                seasonDict[row["Away"]][side + "defensive_third_pct"].append(float(row["Home passzone_defensive_third"]) / (float(row["Home passzone_defensive_third"]) + float(row["Home passzone_middle_third"]) + float(row["Home passzone_final_third"])))
                seasonDict[row["Away"]][side + "final_third_pct"].append(float(row["Home passzone_final_third"]) / (float(row["Home passzone_defensive_third"]) + float(row["Home passzone_middle_third"]) + float(row["Home passzone_final_third"])))
                seasonDict[row["Away"]][side + "ppda"].append(row["Home ppda"])
                seasonDict[row["Away"]][side + "touch_aggression"].append(float(row["Home Touches"]) / float(row["Home Possession"]))
                seasonDict[row["Away"]][side + "pass_aggression"].append(float(row["Home Total Passes"]) / float(row["Home Possession"]))
                seasonDict[row["Away"]][side + "dribble_aggression"].append(float(row["Home Dribbles Attempted"]) / float(row["Home Possession"]))
                seasonDict[row["Away"]][side + "tackle_aggression"].append(float(row["Home Tackles Attempted"]) / float(row["Away Possession"]))
                seasonDict[row["Away"]][side + "corner_rate"].append(float(row["Home passtype_corner"]) / float(row["Home passzone_final_third"]))
                seasonDict[row["Away"]][side + "dispossession_rate"].append(float(row["Home Dispossessed"]) / float(row["Home Possession"]))
                seasonDict[row["Away"]][side + "offsides_rate"].append(float(row["Home Offsides"]) / float(row["Home Total Passes"]))
                seasonDict[row["Away"]][side + "cross_rate"].append(float(row["Home passtype_cross"]) / float(row["Home passzone_final_third"]))
                seasonDict[row["Away"]][side + "through_rate"].append(float(row["Home passtype_through"]) / float(row["Home passzone_final_third"]))
                seasonDict[row["Away"]][side + "xG_aggression_adjustment"].append(float(row["Home xG"]) * float(row["Home ppda"]))
                seasonDict[row["Away"]][side + "xG_efficiency"].append(float(row["Home xG"]) / float(row["Home passzone_final_third"]))
                seasonDict[row["Away"]]["E_" + side + "ball_winning"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Interceptions"]) / float(row["Away Total Passes"]))
                seasonDict[row["Away"]]["E_" + side + "chance_efficiency"].append((float(row["Away Pre Elo"])/1500) * float(row["Home xG"]) * 100 / float(row["Home Possession"]))
                seasonDict[row["Away"]]["E_" + side + "shooting_efficiency"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Score"]) - float(row["Home xG"]))
                seasonDict[row["Away"]]["E_" + side + "key_pass_pct"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Key Passes"]) / float(row["Home passzone_final_third"]))
                seasonDict[row["Away"]]["E_" + side + "pass_success"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Accurate Passes"]) / float(row["Home Total Passes"]))
                seasonDict[row["Away"]]["E_" + side + "dribble_success"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Dribbles Won"]) / float(row["Home Dribbles Attempted"]))
                seasonDict[row["Away"]]["E_" + side + "tackle_success"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Successful Tackles"]) / float(row["Home Tackles Attempted"]))
                seasonDict[row["Away"]]["E_" + side + "xG"].append((float(row["Away Pre Elo"])/1500) * row["Home xG"])
                seasonDict[row["Away"]]["E_" + side + "xPts"].append((float(row["Away Pre Elo"])/1500) * row["Home xPts"])
                seasonDict[row["Away"]]["E_" + side + "xG_aggression_adjustment"].append((float(row["Away Pre Elo"])/1500)  * (float(row["Home xG"]) * float(row["Home ppda"])))
                seasonDict[row["Away"]]["E_" + side + "xG_efficiency"].append((float(row["Away Pre Elo"])/1500)  * (float(row["Home xG"]) / float(row["Home passzone_final_third"])))
                seasonDict[row["Home"]][side + "ball_winning"].append(float(row["Away Interceptions"]) / float(row["Home Total Passes"]))
                seasonDict[row["Home"]][side + "chance_efficiency"].append(float(row["Away xG"]) * 100 / float(row["Away Possession"]))
                seasonDict[row["Home"]][side + "shooting_efficiency"].append(float(row["Away Score"]) - float(row["Away xG"]))
                seasonDict[row["Home"]][side + "key_pass_pct"].append(float(row["Away Key Passes"]) / float(row["Away passzone_final_third"]))
                seasonDict[row["Home"]][side + "pass_success"].append(float(row["Away Accurate Passes"]) / float(row["Away Total Passes"]))
                seasonDict[row["Home"]][side + "dribble_success"].append(float(row["Away Dribbles Won"]) / float(row["Away Dribbles Attempted"]))
                seasonDict[row["Home"]][side + "tackle_success"].append(float(row["Away Successful Tackles"]) / float(row["Away Tackles Attempted"]))
                seasonDict[row["Home"]][side + "xG"].append(row["Away xG"])
                seasonDict[row["Home"]][side + "xPts"].append(row["Away xPts"])
                seasonDict[row["Home"]][side + "deep_pct"].append(float(row["Away deep"]) / float(row["Away Accurate Passes"]))
                seasonDict[row["Home"]][side + "pass_to_touch_ratio"].append(float(row["Away Total Passes"]) / float(row["Away Touches"]))
                seasonDict[row["Home"]][side + "foul_rate"].append(float(row["Away Fouls"]) / float(row["Home Possession"]))
                seasonDict[row["Home"]][side + "clear_rate"].append(float(row["Away Clearances"]) / float(row["Home passzone_final_third"]))
                seasonDict[row["Home"]][side + "long_pass_pct"].append(float(row["Away passlength_long"]) / (float(row["Away passlength_long"]) + float(row["Away passlength_short"])))
                seasonDict[row["Home"]][side + "fwd_pass_pct"].append(float(row["Away passdirection_forward"]) / (float(row["Away passdirection_backward"]) + float(row["Away passdirection_left"]) + float(row["Away passdirection_right"]) + float(row["Away passdirection_forward"])))
                seasonDict[row["Home"]][side + "fwd_pass_aggressiveness"].append(float(row["Away passdirection_forward"]) * float(row["Away Possession"]) / (float(row["Away passdirection_backward"]) + float(row["Away passdirection_left"]) + float(row["Away passdirection_right"])))
                seasonDict[row["Home"]][side + "defensive_third_pct"].append(float(row["Away passzone_defensive_third"]) / (float(row["Away passzone_defensive_third"]) + float(row["Away passzone_middle_third"]) + float(row["Away passzone_final_third"])))
                seasonDict[row["Home"]][side + "final_third_pct"].append(float(row["Away passzone_final_third"]) / (float(row["Away passzone_defensive_third"]) + float(row["Away passzone_middle_third"]) + float(row["Away passzone_final_third"])))
                seasonDict[row["Home"]][side + "ppda"].append(row["Away ppda"])
                seasonDict[row["Home"]][side + "touch_aggression"].append(float(row["Away Touches"]) / float(row["Away Possession"]))
                seasonDict[row["Home"]][side + "pass_aggression"].append(float(row["Away Total Passes"]) / float(row["Away Possession"]))
                seasonDict[row["Home"]][side + "dribble_aggression"].append(float(row["Away Dribbles Attempted"]) / float(row["Away Possession"]))
                seasonDict[row["Home"]][side + "tackle_aggression"].append(float(row["Away Tackles Attempted"]) / float(row["Home Possession"]))
                seasonDict[row["Home"]][side + "corner_rate"].append(float(row["Away passtype_corner"]) / float(row["Away passzone_final_third"]))
                seasonDict[row["Home"]][side + "dispossession_rate"].append(float(row["Away Dispossessed"]) / float(row["Away Possession"]))
                seasonDict[row["Home"]][side + "offsides_rate"].append(float(row["Away Offsides"]) / float(row["Away Total Passes"]))
                seasonDict[row["Home"]][side + "cross_rate"].append(float(row["Away passtype_cross"]) / float(row["Away passzone_final_third"]))
                seasonDict[row["Home"]][side + "through_rate"].append(float(row["Away passtype_through"]) / float(row["Away passzone_final_third"]))
                seasonDict[row["Home"]][side + "xG_aggression_adjustment"].append(float(row["Away xG"]) * float(row["Away ppda"]))
                seasonDict[row["Home"]][side + "xG_efficiency"].append(float(row["Away xG"]) / float(row["Away passzone_final_third"]))
                seasonDict[row["Home"]]["E_" + side + "ball_winning"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Interceptions"]) / float(row["Home Total Passes"]))
                seasonDict[row["Home"]]["E_" + side + "chance_efficiency"].append((float(row["Home Pre Elo"])/1500) * float(row["Away xG"]) * 100 / float(row["Away Possession"]))
                seasonDict[row["Home"]]["E_" + side + "shooting_efficiency"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Score"]) - float(row["Away xG"]))
                seasonDict[row["Home"]]["E_" + side + "key_pass_pct"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Key Passes"]) / float(row["Away passzone_final_third"]))
                seasonDict[row["Home"]]["E_" + side + "pass_success"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Accurate Passes"]) / float(row["Away Total Passes"]))
                seasonDict[row["Home"]]["E_" + side + "dribble_success"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Dribbles Won"]) / float(row["Away Dribbles Attempted"]))
                seasonDict[row["Home"]]["E_" + side + "tackle_success"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Successful Tackles"]) / float(row["Away Tackles Attempted"]))
                seasonDict[row["Home"]]["E_" + side + "xG"].append((float(row["Home Pre Elo"])/1500) * row["Away xG"])
                seasonDict[row["Home"]]["E_" + side + "xPts"].append((float(row["Home Pre Elo"])/1500) * row["Away xPts"])
                seasonDict[row["Home"]]["E_" + side + "xG_aggression_adjustment"].append((float(row["Home Pre Elo"])/1500)  * (float(row["Away xG"]) * float(row["Away ppda"])))
                seasonDict[row["Home"]]["E_" + side + "xG_efficiency"].append((float(row["Home Pre Elo"])/1500)  * (float(row["Away xG"]) / float(row["Away passzone_final_third"])))
        #print (seasonDict)
    for key in dict:
        data[key] = dict[key]
    data.to_csv("./tempPreMatchAverages.csv")
    return (data)

#needs bigboy df
#returns poisson formatted df
def poissonFormat(data, dropE = False, dropT = False):
    print ("--poissonFormat--")
    dict = {"Date":[], "Team":[], "Score":[], "Home Field":[]}
    sides = ["expected", "opponent_expected"]
    for col in data.columns:
        if ("home_expected" in col):
            for side in sides:
                dict[col.split("home_expected")[0] + side + col.split("home_expected")[1]] = []

    for index, row in data.iterrows():
        dict["Date"].append(row["Date"])
        dict["Team"].append(row["Home"])
        dict["Score"].append(row["Home Score"])
        dict["Home Field"].append(1)
        for col in data.columns:
            if ("home_expected" in col):
                dict[col.split("home_expected")[0] + "expected" + col.split("home_expected")[1]].append(row[col])
            elif ("away_expected" in col):
                dict[col.split("away_expected")[0] + "opponent_expected" + col.split("away_expected")[1]].append(row[col])
        dict["Date"].append(row["Date"])
        dict["Team"].append(row["Away"])
        dict["Score"].append(row["Away Score"])
        dict["Home Field"].append(0)
        for col in data.columns:
            if ("away_expected" in col):
                dict[col.split("away_expected")[0] + "expected" + col.split("away_expected")[1]].append(row[col])
            elif ("home_expected" in col):
                dict[col.split("home_expected")[0] + "opponent_expected" + col.split("home_expected")[1]].append(row[col])
    dfFinal = pd.DataFrame.from_dict(dict)
    dfFinal = dfFinal.dropna()
    if (dropE):
        colNames = []
        for col in dfFinal.columns:
            if ("E_" in col):
                colNames.append(col)
        dfFinal = dfFinal.drop(columns=colNames)
    if (dropT):
        colNames = []
        for col in dfFinal.columns:
            if ("T_" in col):
                colNames.append(col)
        dfFinal = dfFinal.drop(columns=colNames)
    dfFinal.to_csv("./tempPoissonFormat.csv")
    return(dfFinal)

#needs poisson formatted df, year to split the data (2017 would split after 2016-17 season, before 2017-18 season)
#returns tuple containing train df and test df
def trainTestSplit(data, year):
    print ("--trainTestSplit--")
    trainIndex = []
    testIndex = []
    switch = 0
    for index, row in data.iterrows():
        if ("-" + str(year%2000) in row["Date"] and ("Aug" in row["Date"] or "Sep" in row["Date"] or "Oct" in row["Date"])):
            switch = 1
        if (switch == 0):
            trainIndex.append(index)
        else:
            testIndex.append(index)
    train = data.loc[trainIndex]
    test = data.loc[testIndex]
    train.to_csv("./tempTrainX.csv")
    test.to_csv("./tempTestX.csv")
    return (train, test)

#needs train df and test df of poisson formatted data
#returns poisson predictions df for test set and train set (train set has predictions from cross validation)
def poissonRegression(train, test):
    print ("--poissonRegression--")
    train.to_csv("./temptrain.csv")
    test.to_csv("./temptest.csv")
    r = robjects.r
    r.source("poissonRegressionTrainTestSplit.R")
    train = pd.read_csv('./trainPredictions.csv', encoding = "ISO-8859-1")
    test = pd.read_csv('./testPredictions.csv', encoding = "ISO-8859-1")
    os.remove("./temptrain.csv")
    os.remove("./temptest.csv")
    os.remove('./testPredictions.csv')
    os.remove('./trainPredictions.csv')
    train.to_csv("./tempTrainPoissonRegression.csv")
    test.to_csv("./tempTestPoissonRegression.csv")
    return (train, test)

#needs train df and test df of poisson prediction data
#return weibull formatted train, test df
def PoissonMeansForWeibull(train, test):
    print ("--PoissonMeansForWeibull--")
    newDict = {}
    sides = ["H_", "A_"]
    for col in train.columns:
        for side in sides:
            newDict[side + col] = []
    cur = 0
    while (cur < len(train.index)):
        for col in train.columns:
            newDict["H_" + col].append(train.at[cur, col])
            newDict["A_" + col].append(train.at[cur+1,col])
        cur += 2
    train = pd.DataFrame.from_dict(newDict)

    newDict = {}
    sides = ["H_", "A_"]
    for col in test.columns:
        for side in sides:
            newDict[side + col] = []
    cur = 0
    while (cur < len(test.index)):
        for col in test.columns:
            newDict["H_" + col].append(test.at[cur, col])
            newDict["A_" + col].append(test.at[cur+1,col])
        cur += 2
    test = pd.DataFrame.from_dict(newDict)
    train.to_csv("./tempTrainPoissonMeansForWeibull.csv")
    test.to_csv("./tempTestPoissonMeansForWeibull.csv")
    return (train, test)

#Needs train and test df formatted for weibull
#returns the test df with predictions
def WeibullCountDist(train, test):
    print ("--WeibullCountDist--")
    games = len(train.index)
    dict = {}
    testCount = 0
    optimal = MLE(train)
    #optimal = [1.0308, 1.1188, 0.6489]
    alphaDictH = {}
    alphaDictA = {}
    cur = 0
    while (cur < len(test.index)):
        hCdf = []
        aCdf = []
        for j in range(11):
            if (j == 0):
                hCdf.append(weibullPmf(j, test.at[cur, "H_Poisson Mean Prediction"], optimal[0], alphaDictH))
                aCdf.append(weibullPmf(j, test.at[cur, "A_Poisson Mean Prediction"], optimal[1], alphaDictA))
            else:
                hCdf.append(weibullPmf(j, test.at[cur, "H_Poisson Mean Prediction"], optimal[0], alphaDictH) + hCdf[j-1])
                aCdf.append(weibullPmf(j, test.at[cur, "A_Poisson Mean Prediction"], optimal[1], alphaDictA) + aCdf[j-1])
        #Converts the distribution from joint CDF to joint PMF
        for j in range(11):
            if (j not in dict):
                dict[j] = {}
            for k in range(11):
                if (k not in dict[j]):
                    dict[j][k] = []
                if (j == 0 and k == 0):
                    dict[j][k].append(copula(hCdf[j], aCdf[k], optimal[2]))
                else:
                    tempProb = copula(hCdf[j], aCdf[k], optimal[2])
                    for p in range(j+1):
                        for q in range(k+1):
                            if (p == j and q == k):
                                break
                            tempProb -= dict[p][q][testCount]
                    dict[j][k].append(tempProb)
        cur += 1
        testCount += 1

    for j in range(11):
        for k in range(11):
            test[str(j) + " -- " + str(k)] = dict[j][k]
    test.to_csv("./tempTestWeibullCountDist.csv")
    return test

#Needs the df with predictions from weibull stuff
#returns betting predictions
def weibullBettingProbabilities(pred):
    print ("--weibullBettingProbabilities--")
    odds = pd.read_csv('./EPL_Csvs/bigboy.csv', encoding = "ISO-8859-1")
    dict = {"Date":[],"Home":[],"Away":[],"Home Score":[],"Away Score":[]}
    for col in odds.columns:
        if ("1" == col or "X" == col or "2" == col or "AH" in col or "Over" in col or "Under" in col):
            dict[col] = []
            dict["P(" + col + ")"] = []
    dict["P(AH 0.0 (1))"] = []
    dict["P(AH 0.0 (2))"] = []

    curIndex = 0
    goalDiffs = [-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6]
    ouList = [0,1,2,3,4,5,6,7,8,9]
    scoreLines = []
    for col in pred.columns:
        if ("--" in col):
            if (col not in dict):
                dict[col] = []
            scoreLines.append(col)
    while (curIndex < len(pred.index)):
        table = [[],[],[],[],[],[],[],[],[],[],[]]
        for score in scoreLines:
            table[int(score.split(" -- ")[0])].append(pred.at[curIndex, score])
            dict[score].append(pred.at[curIndex, score])
        for key in dict:
            if ("P(" in key):
                dict[key].append(0)
        for home in range(11):
            for away in range(11):
                if (home > away):
                    dict["P(1)"][-1] = dict["P(1)"][-1] + table[home][away]
                elif (away > home):
                    dict["P(2)"][-1] = dict["P(2)"][-1] + table[home][away]
                else:
                    dict["P(X)"][-1] = dict["P(X)"][-1] + table[home][away]
        for diff in goalDiffs:
            pHome = 0
            pAway = 0
            pDraw = 0
            if (diff == -6):
                for home in range(11):
                    for away in range(11):
                        if (home - 6 > away):
                            pHome += table[home][away]
                        elif (home - 6 < away):
                            pAway += table[home][away]
                        else:
                            pDraw += table[home][away]
                dict["P(AH -6.0 (1))"][-1] = pHome / (pHome + pAway)
                dict["P(AH -6.0 (2))"][-1] = pAway / (pHome + pAway)
                dict["P(AH -5.75 (1))"][-1] = ((1/2)*pDraw + pHome)/(1-(1/2)*pDraw)
                dict["P(AH -5.75 (2))"][-1] = pAway / (1-(1/2)*pDraw)
            elif (diff != 6):
                for home in range(11):
                    for away in range(11):
                        if (home + diff > away):
                            pHome += table[home][away]
                        elif (home + diff < away):
                            pAway += table[home][away]
                        else:
                            pDraw += table[home][away]
                dict["P(AH " + str(float(diff)) + " (1))"][-1] = pHome / (pHome + pAway)
                dict["P(AH " + str(float(diff)) + " (2))"][-1] = pAway / (pHome + pAway)
                dict["P(AH " + str(float(diff) + 0.25) + " (1))"][-1] = ((1/2)*pDraw + pHome)/(1-(1/2)*pDraw)
                dict["P(AH " + str(float(diff) + 0.25) + " (2))"][-1] = pAway / (1-(1/2)*pDraw)
                dict["P(AH " + str(float(diff) - 0.25) + " (1))"][-1] = pHome / (1-(1/2)*pDraw)
                dict["P(AH " + str(float(diff) - 0.25) + " (2))"][-1] = ((1/2)*pDraw + pAway)/(1-(1/2)*pDraw)
                dict["P(AH " + str(float(diff) - 0.5) + " (1))"][-1] = pHome
                dict["P(AH " + str(float(diff) - 0.5) + " (2))"][-1] = pAway + pDraw
            else:
                for home in range(11):
                    for away in range(11):
                        if (home + 6 > away):
                            pHome += table[home][away]
                        elif (home + 6 < away):
                            pAway += table[home][away]
                        else:
                            pDraw += table[home][away]
                dict["P(AH 6.0 (1))"][-1] = pHome / (pHome + pAway)
                dict["P(AH 6.0 (2))"][-1] = pAway / (pHome + pAway)
                dict["P(AH 5.75 (1))"][-1] = pHome / (1-(1/2)*pDraw)
                dict["P(AH 5.75 (2))"][-1] = ((1/2)*pDraw + pAway)/(1-(1/2)*pDraw)
        for total in ouList:
            pOver = 0
            pUnder = 0
            pDraw = 0
            if (total == 0):
                for home in range(11):
                    for away in range(11):
                        if (home + away > total):
                            pOver += table[home][away]
                        elif (home + away < total):
                            pUnder += table[home][away]
                        else:
                            pDraw += table[home][away]
                dict["P(Over 0.25)"][-1] = pOver / (1-(1/2)*pDraw)
                dict["P(Under 0.25)"][-1] = ((1/2)*pDraw + pUnder)/(1-(1/2)*pDraw)
            elif (total != 9):
                for home in range(11):
                    for away in range(11):
                        if (home + away > total):
                            pOver += table[home][away]
                        elif (home + away < total):
                            pUnder += table[home][away]
                        else:
                            pDraw += table[home][away]
                dict["P(Over " + str(float(total)) + ")"][-1] = pOver / (pOver + pUnder)
                dict["P(Under " + str(float(total)) + ")"][-1] = pUnder / (pOver + pUnder)
                dict["P(Over " + str(float(total) + 0.25) + ")"][-1] = pOver / (1-(1/2)*pDraw)
                dict["P(Under " + str(float(total) + 0.25) + ")"][-1] = ((1/2)*pDraw + pUnder)/(1-(1/2)*pDraw)
                dict["P(Over " + str(float(total) - 0.25) + ")"][-1] = ((1/2)*pDraw + pOver)/(1-(1/2)*pDraw)
                dict["P(Under " + str(float(total) - 0.25) + ")"][-1] = pUnder / (1-(1/2)*pDraw)
                dict["P(Over " + str(float(total) - 0.5) + ")"][-1] = pOver + pDraw
                dict["P(Under " + str(float(total) - 0.5) + ")"][-1] = pUnder
            else:
                for home in range(11):
                    for away in range(11):
                        if (home + away > total):
                            pOver += table[home][away]
                        elif (home + away < total):
                            pUnder += table[home][away]
                        else:
                            pDraw += table[home][away]
                dict["P(Over 9.0)"][-1] = pOver / (pOver + pUnder)
                dict["P(Under 9.0)"][-1] = pUnder / (pOver + pUnder)
                dict["P(Over 8.75)"][-1] = ((1/2)*pDraw + pOver)/(1-(1/2)*pDraw)
                dict["P(Under 8.75)"][-1] = pUnder / (1-(1/2)*pDraw)
                dict["P(Over 8.5)"][-1] = pOver + pDraw
                dict["P(Under 8.5)"][-1] = pUnder
        for index, row in odds.iterrows():
            if (row["Home"] == pred.at[curIndex, "H_Team"] and row["Away"] == pred.at[curIndex, "A_Team"] and row["Date"] == pred.at[curIndex, "H_Date"]):
                for col in odds.columns:
                    if ("1" == col or "X" == col or "2" == col or "AH" in col or "Over" in col or "Under" in col or "Date" == col or "Home Score" == col or "Away Score" == col):
                        dict[col].append(row[col])
                dict["Home"].append(pred.at[curIndex, "H_Team"])
                dict["Away"].append(pred.at[curIndex, "A_Team"])
        curIndex += 1
    dfFinal = pd.DataFrame.from_dict(dict)
    dfFinal.to_csv("./tempBetPred.csv")
    return dfFinal

#takes betting predictions
#removes options that were collected incorrectly by oddsportal, returns betting predictions
def cleanOdds(pred):
    for index, row in pred.iterrows():
        dict = {"ah":[],"ou":[]}
        for col in pred.columns:
            if ("AH" in col and "P(" not in col and not np.isnan(row[col]) and row[col] != 1):
                #if (row["P(" + col + ")"] - (1/row[col]) > 0):
                dict["ah"].append(row["P(" + col + ")"] - (1/row[col]))
            if (("Over" in col or "Under" in col) and "P(" not in col and not np.isnan(row[col]) and row[col] != 1):
                #if (row["P(" + col + ")"] - (1/row[col]) > 0):
                dict["ou"].append(row["P(" + col + ")"] - (1/row[col]))
        if (dict["ah"]):
            ahMean = np.average(dict["ah"])
            ahStd = np.std(dict["ah"])
        if (dict["ou"]):
            ouMean = np.average(dict["ou"])
            ouStd = np.std(dict["ou"])
        for col in pred.columns:
            if ("AH" in col and "P(" not in col and not np.isnan(row[col]) and row[col] != 1):
                if (dict["ah"] and abs((row["P(" + col + ")"] - (1/row[col]) - ahMean)/ahStd) > 3.5 and row["P(" + col + ")"] - (1/row[col]) > 0):
                    row[col] = np.nan
            if (("Over" in col or "Under" in col) and "P(" not in col and not np.isnan(row[col]) and row[col] != 1):
                if (dict["ou"] and abs((row["P(" + col + ")"] - (1/row[col]) - ouMean)/ouStd) > 3.5 and row["P(" + col + ")"] - (1/row[col]) > 0):
                    row[col] = np.nan
    return pred

#takes betting predictions
#returns something
def naiveEvaluation(pred, unique=False):
    print ("--naiveEvaluation--")
    mlDict = {"Bet":[],"Book Prob":[],"Edge":[],"Result":[],"P":[],"Kelly":[]}
    ahDict = {"Bet":[],"Book Prob":[],"Edge":[],"Result":[],"P":[],"Kelly":[]}
    ouDict = {"Bet":[],"Book Prob":[],"Edge":[],"Result":[],"P":[],"Kelly":[]}
    #pred = pred.sample(frac=1).reset_index(drop=True)
    bankroll = 30000
    resultsByEdge =[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    resultsByKK = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    ouresultsByKK = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    mloddsTaken = []
    mlresults = []
    ahoddsTaken = []
    ahresults = []
    ouoddsTaken = []
    ouresults = []
    ml = {"edge":0,"colName":"","netWin":0,"netWinFixed":0}
    ah = {"edge":0,"colName":"","netWin":0,"netWinFixed":0}
    ou = {"edge":0,"colName":"","netWin":0,"netWinFixed":0}
    for index, row in pred.iterrows():
        ml["edge"] = 0
        ml["colName"] = ""
        ah["edge"] = 0
        ah["colName"] = ""
        ou["edge"] = 0
        ou["colName"] = ""
        for col in pred.columns:
            #(row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]]))
            if (("1" == col or "X" == col or "2" == col) and "P(" not in col):
                if ((row["P(" + col + ")"] - (1/row[col])) > ml["edge"]):
                    ml["edge"] = (row["P(" + col + ")"] - (1/row[col]))
                    ml["colName"] = col
            if ("AH" in col and "P(" not in col and not np.isnan(row[col]) and row[col] != 1):
                if ((row["P(" + col + ")"] - (1/row[col]))> ah["edge"]):
                    ah["edge"] = (row["P(" + col + ")"] - (1/row[col]))
                    ah["colName"] = col
            if (("Over" in col or "Under" in col) and "P(" not in col and not np.isnan(row[col]) and row[col] != 1):
                if ((row["P(" + col + ")"] - (1/row[col])) > ou["edge"]):
                    ou["edge"] = (row["P(" + col + ")"] - (1/row[col]))
                    ou["colName"] = col
        preBR = bankroll
        if (ml["edge"] > 0):
            mloddsTaken.append(row[ml["colName"]])
            mlDict["Bet"].append(ml["colName"])
            if (ml["colName"] == "1"):
                if (row["Home Score"] > row["Away Score"]):
                    bankroll += ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*preBR*(row[ml["colName"]] - 1)
                    ml["netWin"] += ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*30000*(row[ml["colName"]] - 1)
                    ml["netWinFixed"] += 300*(row[ml["colName"]] - 1)
                    mlresults.append(1)
                    mlDict["Result"].append(1)
                    mlDict["Book Prob"].append(1/row[ml["colName"]])
                    mlDict["Edge"].append(row["P(" + ml["colName"] + ")"] - 1/row[ml["colName"]])
                    mlDict["P"].append(row["P(" + ml["colName"] + ")"])
                    mlDict["Kelly"].append(((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]]))))
                else:
                    bankroll -= ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*preBR
                    ml["netWin"] -= ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*30000
                    ml["netWinFixed"] -= 300
                    mlresults.append(0)
                    mlDict["Result"].append(0)
                    mlDict["Book Prob"].append(1/row[ml["colName"]])
                    mlDict["Edge"].append(row["P(" + ml["colName"] + ")"] - 1/row[ml["colName"]])
                    mlDict["P"].append(row["P(" + ml["colName"] + ")"])
                    mlDict["Kelly"].append(((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]]))))
            elif (ml["colName"] == "2"):
                if (row["Away Score"] > row["Home Score"]):
                    bankroll += ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*preBR*(row[ml["colName"]] - 1)
                    ml["netWin"] += ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*30000*(row[ml["colName"]] - 1)
                    ml["netWinFixed"] += 300*(row[ml["colName"]] - 1)
                    mlresults.append(1)
                    mlDict["Result"].append(1)
                    mlDict["Book Prob"].append(1/row[ml["colName"]])
                    mlDict["Edge"].append(row["P(" + ml["colName"] + ")"] - 1/row[ml["colName"]])
                    mlDict["P"].append(row["P(" + ml["colName"] + ")"])
                    mlDict["Kelly"].append(((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]]))))
                else:
                    bankroll -= ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*preBR
                    ml["netWin"] -= ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*30000
                    ml["netWinFixed"] -= 300
                    mlresults.append(0)
                    mlDict["Result"].append(0)
                    mlDict["Book Prob"].append(1/row[ml["colName"]])
                    mlDict["Edge"].append(row["P(" + ml["colName"] + ")"] - 1/row[ml["colName"]])
                    mlDict["P"].append(row["P(" + ml["colName"] + ")"])
                    mlDict["Kelly"].append(((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]]))))
            else:
                if (row["Away Score"] == row["Home Score"]):
                    bankroll += ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*preBR*(row[ml["colName"]] - 1)
                    ml["netWin"] += ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*30000*(row[ml["colName"]] - 1)
                    ml["netWinFixed"] += 300*(row[ml["colName"]] - 1)
                    mlresults.append(1)
                    mlDict["Result"].append(1)
                    mlDict["Book Prob"].append(1/row[ml["colName"]])
                    mlDict["Edge"].append(row["P(" + ml["colName"] + ")"] - 1/row[ml["colName"]])
                    mlDict["P"].append(row["P(" + ml["colName"] + ")"])
                    mlDict["Kelly"].append(((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]]))))
                else:
                    bankroll -= ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*preBR
                    ml["netWin"] -= ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*30000
                    ml["netWinFixed"] -= 300
                    mlresults.append(0)
                    mlDict["Result"].append(0)
                    mlDict["Book Prob"].append(1/row[ml["colName"]])
                    mlDict["Edge"].append(row["P(" + ml["colName"] + ")"] - 1/row[ml["colName"]])
                    mlDict["P"].append(row["P(" + ml["colName"] + ")"])
                    mlDict["Kelly"].append(((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]]))))
        else:
            mlDict["Result"].append(np.nan)
            mlDict["Book Prob"].append(np.nan)
            mlDict["Edge"].append(np.nan)
            mlDict["P"].append(np.nan)
            mlDict["Bet"].append(np.nan)
            mlDict["Kelly"].append(np.nan)
        if (ah["edge"] > 0 and ah["edge"]):
            ahoddsTaken.append(row[ah["colName"]])
            ahDict["Bet"].append(ah["colName"])
            if (ah["colName"].split()[1].split(".")[1] != "25" and ah["colName"].split()[1].split(".")[1] != "75"):
                if ("(1)" in ah["colName"]):
                    if (row["Away Score"] - row["Home Score"] < float(ah["colName"].split()[1])):
                        bankroll += ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR*(row[ah["colName"]] - 1)
                        ah["netWin"] += ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000*(row[ah["colName"]] - 1)
                        ah["netWinFixed"] += 300*(row[ah["colName"]] - 1)
                        ahresults.append(1)
                        ahDict["Result"].append(1)
                        ahDict["Book Prob"].append(1/row[ah["colName"]])
                        ahDict["Edge"].append((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])))
                        ahDict["P"].append(1/row[ah["colName"]] + ah["edge"])
                        ahDict["Kelly"].append(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]]))))
                    elif (row["Away Score"] - row["Home Score"] > float(ah["colName"].split()[1])):
                        bankroll -= ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR
                        ah["netWin"] -= ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000
                        ah["netWinFixed"] -= 300
                        ahresults.append(0)
                        ahDict["Result"].append(0)
                        ahDict["Book Prob"].append(1/row[ah["colName"]])
                        ahDict["Edge"].append((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])))
                        ahDict["P"].append(1/row[ah["colName"]] + ah["edge"])
                        ahDict["Kelly"].append(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]]))))
                    else:
                        ahresults.append(np.nan)
                        ahDict["Result"].append(np.nan)
                        ahDict["Book Prob"].append(1/row[ah["colName"]])
                        ahDict["Edge"].append((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])))
                        ahDict["P"].append(1/row[ah["colName"]] + ah["edge"])
                        ahDict["Kelly"].append(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]]))))
                else:
                    if (row["Home Score"] - row["Away Score"] < 0-float(ah["colName"].split()[1])):
                        bankroll += ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR*(row[ah["colName"]] - 1)
                        ah["netWin"] += ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000*(row[ah["colName"]] - 1)
                        ah["netWinFixed"] += 300*(row[ah["colName"]] - 1)
                        ahresults.append(1)
                        ahDict["Result"].append(1)
                        ahDict["Book Prob"].append(1/row[ah["colName"]])
                        ahDict["Edge"].append((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])))
                        ahDict["P"].append(1/row[ah["colName"]] + ah["edge"])
                        ahDict["Kelly"].append(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]]))))
                    elif (row["Home Score"] - row["Away Score"] > 0-float(ah["colName"].split()[1])):
                        bankroll -= ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR
                        ah["netWin"] -= ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000
                        ah["netWinFixed"] -= 300
                        ahresults.append(0)
                        ahDict["Result"].append(0)
                        ahDict["Book Prob"].append(1/row[ah["colName"]])
                        ahDict["Edge"].append((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])))
                        ahDict["P"].append(1/row[ah["colName"]] + ah["edge"])
                        ahDict["Kelly"].append(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]]))))
                    else:
                        ahresults.append(np.nan)
                        ahDict["Result"].append(np.nan)
                        ahDict["Book Prob"].append(1/row[ah["colName"]])
                        ahDict["Edge"].append((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])))
                        ahDict["P"].append(1/row[ah["colName"]] + ah["edge"])
                        ahDict["Kelly"].append(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]]))))
            else:
                if (ah["colName"].split()[1][0] == "-" and ah["colName"].split()[1].split(".")[1] == "75"):
                    toAdd = -0.25
                elif (ah["colName"].split()[1][0] != "-" and ah["colName"].split()[1].split(".")[1] == "25"):
                    toAdd = -0.25
                else:
                    toAdd = 0.25
                if ("(1)" in ah["colName"]):
                    if (row["Away Score"] - row["Home Score"] < float(ah["colName"].split()[1]) + toAdd):
                        bankroll += ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR*(row[ah["colName"]] - 1)
                        ah["netWin"] += ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000*(row[ah["colName"]] - 1)
                        ah["netWinFixed"] += 300*(row[ah["colName"]] - 1)
                        ahresults.append(1)
                        ahDict["Result"].append(1)
                        ahDict["Book Prob"].append(1/row[ah["colName"]])
                        ahDict["Edge"].append((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])))
                        ahDict["P"].append(row["P(" + ah["colName"] + ")"])
                        ahDict["Kelly"].append(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]]))))
                    elif (row["Away Score"] - row["Home Score"] > float(ah["colName"].split()[1]) + toAdd):
                        bankroll -= ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR
                        ah["netWin"] -= ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000
                        ah["netWinFixed"] -= 300
                        ahresults.append(0)
                        ahDict["Result"].append(0)
                        ahDict["Book Prob"].append(1/row[ah["colName"]])
                        ahDict["Edge"].append((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])))
                        ahDict["P"].append(row["P(" + ah["colName"] + ")"])
                        ahDict["Kelly"].append(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]]))))
                    else:
                        if ((ah["colName"].split()[1][0] == "-" and ah["colName"].split()[1].split(".")[1] == "75") or (ah["colName"].split()[1][0] != "-" and ah["colName"].split()[1].split(".")[1] == "25")):
                            bankroll += (((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR*(row[ah["colName"]] - 1))/2
                            ah["netWin"] += (((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000*(row[ah["colName"]] - 1))/2
                            ah["netWinFixed"] += 300*(row[ah["colName"]] - 1)/2
                            ahresults.append(1)
                            ahDict["Result"].append(1)
                            ahDict["Book Prob"].append(1/row[ah["colName"]])
                            ahDict["Edge"].append((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])))
                            ahDict["P"].append(row["P(" + ah["colName"] + ")"])
                            ahDict["Kelly"].append(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]]))))
                        else:
                            bankroll -= (((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR)/2
                            ah["netWin"] -= (((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000)/2
                            ah["netWinFixed"] -= 300/2
                            ahresults.append(0)
                            ahDict["Result"].append(0)
                            ahDict["Book Prob"].append(1/row[ah["colName"]])
                            ahDict["Edge"].append((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])))
                            ahDict["P"].append(row["P(" + ah["colName"] + ")"])
                            ahDict["Kelly"].append(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]]))))
                else:
                    if (row["Home Score"] - row["Away Score"] < 0-float(ah["colName"].split()[1]) - toAdd):
                        bankroll += ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR*(row[ah["colName"]] - 1)
                        ah["netWin"] += ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000*(row[ah["colName"]] - 1)
                        ah["netWinFixed"] += 300*(row[ah["colName"]] - 1)
                        ahresults.append(1)
                        ahDict["Result"].append(1)
                        ahDict["Book Prob"].append(1/row[ah["colName"]])
                        ahDict["Edge"].append((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])))
                        ahDict["P"].append(row["P(" + ah["colName"] + ")"])
                        ahDict["Kelly"].append(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]]))))
                    elif (row["Home Score"] - row["Away Score"] > 0-float(ah["colName"].split()[1]) - toAdd):
                        bankroll -= ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR
                        ah["netWin"] -= ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000
                        ah["netWinFixed"] -= 300
                        ahresults.append(0)
                        ahDict["Result"].append(0)
                        ahDict["Book Prob"].append(1/row[ah["colName"]])
                        ahDict["Edge"].append((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])))
                        ahDict["P"].append(row["P(" + ah["colName"] + ")"])
                        ahDict["Kelly"].append(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]]))))
                    else:
                        if ((ah["colName"].split()[1][0] == "-" and ah["colName"].split()[1].split(".")[1] == "25") or (ah["colName"].split()[1][0] != "-" and ah["colName"].split()[1].split(".")[1] == "75")):
                            bankroll += (((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR*(row[ah["colName"]] - 1))/2
                            ah["netWin"] += (((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000*(row[ah["colName"]] - 1))/2
                            ah["netWinFixed"] += 300*(row[ah["colName"]] - 1)/2
                            ahresults.append(1)
                            ahDict["Result"].append(1)
                            ahDict["Book Prob"].append(1/row[ah["colName"]])
                            ahDict["Edge"].append((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])))
                            ahDict["P"].append(row["P(" + ah["colName"] + ")"])
                            ahDict["Kelly"].append(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]]))))
                        else:
                            bankroll -= (((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR)/2
                            ah["netWin"] -= (((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000)/2
                            ah["netWinFixed"] -= 300/2
                            ahresults.append(0)
                            ahDict["Result"].append(0)
                            ahDict["Book Prob"].append(1/row[ah["colName"]])
                            ahDict["Edge"].append((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])))
                            ahDict["P"].append(row["P(" + ah["colName"] + ")"])
                            ahDict["Kelly"].append(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]]))))
        else:
            ahDict["Result"].append(np.nan)
            ahDict["Book Prob"].append(np.nan)
            ahDict["Edge"].append(np.nan)
            ahDict["P"].append(np.nan)
            ahDict["Bet"].append(np.nan)
            ahDict["Kelly"].append(np.nan)
        if (ou["edge"] > 0 and ou["edge"]):
            ouoddsTaken.append(row[ou["colName"]])
            ouDict["Bet"].append(ou["colName"])
            if (ou["colName"].split()[1].split(".")[1] != "25" and ou["colName"].split()[1].split(".")[1] != "75"):
                if ("Over" in ou["colName"]):
                    if (row["Home Score"] + row["Away Score"] > float(ou["colName"].split()[1])):
                        bankroll += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR*(row[ou["colName"]] - 1)
                        ou["netWin"] += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000*(row[ou["colName"]] - 1)
                        ou["netWinFixed"] += 300*(row[ou["colName"]] - 1)
                        ouresults.append(1)
                        ouDict["Result"].append(1)
                        ouDict["Book Prob"].append(1/row[ou["colName"]])
                        ouDict["Edge"].append((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])))
                        ouDict["P"].append(row["P(" + ou["colName"] + ")"])
                        ouDict["Kelly"].append(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]]))))
                    elif (row["Home Score"] + row["Away Score"] < float(ou["colName"].split()[1])):
                        bankroll -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR
                        ou["netWin"] -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000
                        ou["netWinFixed"] -= 300
                        ouresults.append(0)
                        ouDict["Result"].append(0)
                        ouDict["Book Prob"].append(1/row[ou["colName"]])
                        ouDict["Edge"].append((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])))
                        ouDict["P"].append(row["P(" + ou["colName"] + ")"])
                        ouDict["Kelly"].append(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]]))))
                    else:
                        ouresults.append(np.nan)
                        ouDict["Result"].append(np.nan)
                        ouDict["Book Prob"].append(1/row[ou["colName"]])
                        ouDict["Edge"].append((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])))
                        ouDict["P"].append(row["P(" + ou["colName"] + ")"])
                        ouDict["Kelly"].append(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]]))))
                else:
                    if (row["Home Score"] + row["Away Score"] < float(ou["colName"].split()[1])):
                        bankroll += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR*(row[ou["colName"]] - 1)
                        ou["netWin"] += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000*(row[ou["colName"]] - 1)
                        ou["netWinFixed"] += 300*(row[ou["colName"]] - 1)
                        ouresults.append(1)
                        ouDict["Result"].append(1)
                        ouDict["Book Prob"].append(1/row[ou["colName"]])
                        ouDict["Edge"].append((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])))
                        ouDict["P"].append(row["P(" + ou["colName"] + ")"])
                        ouDict["Kelly"].append(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]]))))
                    elif (row["Home Score"] + row["Away Score"] > float(ou["colName"].split()[1])):
                        bankroll -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR
                        ou["netWin"] -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000
                        ou["netWinFixed"] -= 300
                        ouresults.append(0)
                        ouDict["Result"].append(0)
                        ouDict["Book Prob"].append(1/row[ou["colName"]])
                        ouDict["Edge"].append((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])))
                        ouDict["P"].append(row["P(" + ou["colName"] + ")"])
                        ouDict["Kelly"].append(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]]))))
                    else:
                        ouresults.append(np.nan)
                        ouDict["Result"].append(np.nan)
                        ouDict["Book Prob"].append(1/row[ou["colName"]])
                        ouDict["Edge"].append((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])))
                        ouDict["P"].append(row["P(" + ou["colName"] + ")"])
                        ouDict["Kelly"].append(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]]))))
            elif (ou["colName"].split()[1].split(".")[1] == "25"):
                if ("Over" in ou["colName"]):
                    if (row["Home Score"] + row["Away Score"] == float(ou["colName"].split()[1]) - 0.25):
                        bankroll -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR/2
                        ou["netWin"] -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000/2
                        ou["netWinFixed"] -= 300/2
                        ouresults.append(0)
                        ouDict["Result"].append(0)
                        ouDict["Book Prob"].append(1/row[ou["colName"]])
                        ouDict["Edge"].append((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])))
                        ouDict["P"].append(row["P(" + ou["colName"] + ")"])
                        ouDict["Kelly"].append(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]]))))
                    elif (row["Home Score"] + row["Away Score"] > float(ou["colName"].split()[1])):
                        bankroll += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR*(row[ou["colName"]] - 1)
                        ou["netWin"] += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000*(row[ou["colName"]] - 1)
                        ou["netWinFixed"] += 300*(row[ou["colName"]] - 1)
                        ouresults.append(1)
                        ouDict["Result"].append(1)
                        ouDict["Book Prob"].append(1/row[ou["colName"]])
                        ouDict["Edge"].append((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])))
                        ouDict["P"].append(row["P(" + ou["colName"] + ")"])
                        ouDict["Kelly"].append(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]]))))
                    else:
                        bankroll -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR
                        ou["netWin"] -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000
                        ou["netWinFixed"] -= 300
                        ouresults.append(0)
                        ouDict["Result"].append(0)
                        ouDict["Book Prob"].append(1/row[ou["colName"]])
                        ouDict["Edge"].append((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])))
                        ouDict["P"].append(row["P(" + ou["colName"] + ")"])
                        ouDict["Kelly"].append(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]]))))
                else:
                    if (row["Home Score"] + row["Away Score"] == float(ou["colName"].split()[1]) - 0.25):
                        bankroll += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR*(row[ou["colName"]] - 1)/2
                        ou["netWin"] += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000*(row[ou["colName"]] - 1)/2
                        ou["netWinFixed"] += 300*(row[ou["colName"]] - 1)/2
                        ouresults.append(1)
                        ouDict["Result"].append(1)
                        ouDict["Book Prob"].append(1/row[ou["colName"]])
                        ouDict["Edge"].append((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])))
                        ouDict["P"].append(row["P(" + ou["colName"] + ")"])
                        ouDict["Kelly"].append(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]]))))
                    elif (row["Home Score"] + row["Away Score"] < float(ou["colName"].split()[1])):
                        bankroll += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR*(row[ou["colName"]] - 1)
                        ou["netWin"] += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000*(row[ou["colName"]] - 1)
                        ou["netWinFixed"] += 300*(row[ou["colName"]] - 1)
                        ouresults.append(1)
                        ouDict["Result"].append(1)
                        ouDict["Book Prob"].append(1/row[ou["colName"]])
                        ouDict["Edge"].append((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])))
                        ouDict["P"].append(row["P(" + ou["colName"] + ")"])
                        ouDict["Kelly"].append(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]]))))
                    else:
                        bankroll -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR
                        ou["netWin"] -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000
                        ou["netWinFixed"] -= 300
                        ouresults.append(0)
                        ouDict["Result"].append(0)
                        ouDict["Book Prob"].append(1/row[ou["colName"]])
                        ouDict["Edge"].append((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])))
                        ouDict["P"].append(row["P(" + ou["colName"] + ")"])
                        ouDict["Kelly"].append(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]]))))
            else:
                if ("Over" in ou["colName"]):
                    if (row["Home Score"] + row["Away Score"] == float(ou["colName"].split()[1]) + 0.25):
                        bankroll += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR*(row[ou["colName"]] - 1)/2
                        ou["netWin"] += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000*(row[ou["colName"]] - 1)/2
                        ou["netWinFixed"] += 300*(row[ou["colName"]] - 1)/2
                        ouresults.append(1)
                        ouDict["Result"].append(1)
                        ouDict["Book Prob"].append(1/row[ou["colName"]])
                        ouDict["Edge"].append((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])))
                        ouDict["P"].append(row["P(" + ou["colName"] + ")"])
                        ouDict["Kelly"].append(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]]))))
                    elif (row["Home Score"] + row["Away Score"] > float(ou["colName"].split()[1])):
                        bankroll += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR*(row[ou["colName"]] - 1)
                        ou["netWin"] += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000*(row[ou["colName"]] - 1)
                        ou["netWinFixed"] += 300*(row[ou["colName"]] - 1)
                        ouresults.append(1)
                        ouDict["Result"].append(1)
                        ouDict["Book Prob"].append(1/row[ou["colName"]])
                        ouDict["Edge"].append((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])))
                        ouDict["P"].append(row["P(" + ou["colName"] + ")"])
                        ouDict["Kelly"].append(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]]))))
                    else:
                        bankroll -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR
                        ou["netWin"] -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000
                        ou["netWinFixed"] -= 300
                        ouresults.append(0)
                        ouDict["Result"].append(0)
                        ouDict["Book Prob"].append(1/row[ou["colName"]])
                        ouDict["Edge"].append((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])))
                        ouDict["P"].append(row["P(" + ou["colName"] + ")"])
                        ouDict["Kelly"].append(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]]))))
                else:
                    if (row["Home Score"] + row["Away Score"] == float(ou["colName"].split()[1]) + 0.25):
                        bankroll -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR/2
                        ou["netWin"] -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000/2
                        ou["netWinFixed"] -= 300/2
                        ouresults.append(0)
                        ouDict["Result"].append(0)
                        ouDict["Book Prob"].append(1/row[ou["colName"]])
                        ouDict["Edge"].append((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])))
                        ouDict["P"].append(row["P(" + ou["colName"] + ")"])
                        ouDict["Kelly"].append(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]]))))
                    elif (row["Home Score"] + row["Away Score"] < float(ou["colName"].split()[1])):
                        bankroll += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR*(row[ou["colName"]] - 1)
                        ou["netWin"] += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000*(row[ou["colName"]] - 1)
                        ou["netWinFixed"] += 300*(row[ou["colName"]] - 1)
                        ouresults.append(1)
                        ouDict["Result"].append(1)
                        ouDict["Book Prob"].append(1/row[ou["colName"]])
                        ouDict["Edge"].append((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])))
                        ouDict["P"].append(row["P(" + ou["colName"] + ")"])
                        ouDict["Kelly"].append(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]]))))
                    else:
                        bankroll -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR
                        ou["netWin"] -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000
                        ou["netWinFixed"] -= 300
                        ouresults.append(0)
                        ouDict["Result"].append(0)
                        ouDict["Book Prob"].append(1/row[ou["colName"]])
                        ouDict["Edge"].append((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])))
                        ouDict["P"].append(row["P(" + ou["colName"] + ")"])
                        ouDict["Kelly"].append(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]]))))
        else:
            ouDict["Result"].append(np.nan)
            ouDict["Book Prob"].append(np.nan)
            ouDict["Edge"].append(np.nan)
            ouDict["P"].append(np.nan)
            ouDict["Bet"].append(np.nan)
            ouDict["Kelly"].append(np.nan)
        #print (bankroll, ml["netWin"])
    print ("------------------------")
    print ("Final Bankroll:", bankroll)
    print ("ML Odds Taken:", 1/np.average(mloddsTaken))
    print ("ML Results:", np.average(mlresults))
    print ("ML Net Win:", ml["netWin"])
    print ("ML Net Win Fixed Betting:", ml["netWinFixed"])
    print ("AH Odds Taken:", 1/np.average(ahoddsTaken))
    print ("AH Results:", np.average(ahresults))
    print ("AH Net Win:", ah["netWin"])
    print ("AH Net Win Fixed Betting:", ah["netWinFixed"])
    print ("OU Odds Taken:", 1/np.average(ouoddsTaken))
    print ("OU Results:",np.average(ouresults))
    print ("OU Net Win:", ou["netWin"])
    print ("OU Net Win Fixed Betting:", ou["netWinFixed"])
    for key in mlDict:
        pred["ML " + key] = mlDict[key]
        pred["AH " + key] = ahDict[key]
        pred["OU " + key] = ouDict[key]

    mlAdj = []
    ahAdj = []
    ouAdj = []
    betTypes = ["ML ", "AH ", "OU "]
    for index, row in pred.iterrows():
        td = {}
        for t in betTypes:
            td[t + "Success"] = []
            td[t + "Fail"] = []
            td[t + "P"] = 0
        for col in pred.columns:
            if (" -- " in col):
                if (row["ML Bet"] == row["ML Bet"]):
                    if (row["ML Bet"] == "1"):
                        if (int(col.split(" -- ")[0]) > int(col.split(" -- ")[1])):
                            td["ML Success"].append(col)
                        else:
                            td["ML Fail"].append(col)
                    elif (row["ML Bet"] == "2"):
                        if (int(col.split(" -- ")[1]) > int(col.split(" -- ")[0])):
                            td["ML Success"].append(col)
                        else:
                            td["ML Fail"].append(col)
                    elif (row["ML Bet"] == "X"):
                        if (int(col.split(" -- ")[1]) == int(col.split(" -- ")[0])):
                            td["ML Success"].append(col)
                        else:
                            td["ML Fail"].append(col)

                if (row["AH Bet"] == row["AH Bet"]):
                    if (row["AH Bet"].split()[1].split(".")[1] != "25" and row["AH Bet"].split()[1].split(".")[1] != "75"):
                        if ("(1)" in row["AH Bet"]):
                            if (int(col.split(" -- ")[1]) - int(col.split(" -- ")[0]) < float(row["AH Bet"].split()[1])):
                                td["AH Success"].append(col)
                            elif (int(col.split(" -- ")[1]) - int(col.split(" -- ")[0]) > float(row["AH Bet"].split()[1])):
                                td["AH Fail"].append(col)
                        else:
                            if (int(col.split(" -- ")[0]) - int(col.split(" -- ")[1]) < 0-float(row["AH Bet"].split()[1])):
                                td["AH Success"].append(col)
                            elif (int(col.split(" -- ")[0]) - int(col.split(" -- ")[1]) > 0-float(row["AH Bet"].split()[1])):
                                td["AH Fail"].append(col)
                    else:
                        if (row["AH Bet"].split()[1][0] == "-" and row["AH Bet"].split()[1].split(".")[1] == "75"):
                            toAdd = -0.25
                        elif (row["AH Bet"].split()[1][0] != "-" and row["AH Bet"].split()[1].split(".")[1] == "25"):
                            toAdd = -0.25
                        else:
                            toAdd = 0.25
                        if ("(1)" in row["AH Bet"]):
                            if (int(col.split(" -- ")[1]) - int(col.split(" -- ")[0]) < float(row["AH Bet"].split()[1]) + toAdd):
                                td["AH Success"].append(col)
                            elif (int(col.split(" -- ")[1]) - int(col.split(" -- ")[0]) > float(row["AH Bet"].split()[1]) + toAdd):
                                td["AH Fail"].append(col)
                            else:
                                if ((row["AH Bet"].split()[1][0] == "-" and row["AH Bet"].split()[1].split(".")[1] == "75") or (row["AH Bet"].split()[1][0] != "-" and row["AH Bet"].split()[1].split(".")[1] == "25")):
                                    td["AH Success"].append(col)
                                else:
                                    td["AH Fail"].append(col)
                        else:
                            if (int(col.split(" -- ")[0]) - int(col.split(" -- ")[1]) < 0-float(row["AH Bet"].split()[1]) - toAdd):
                                td["AH Success"].append(col)
                            elif (int(col.split(" -- ")[0]) - int(col.split(" -- ")[1]) > 0-float(row["AH Bet"].split()[1]) - toAdd):
                                td["AH Fail"].append(col)
                            else:
                                if ((row["AH Bet"].split()[1][0] == "-" and row["AH Bet"].split()[1].split(".")[1] == "25") or (row["AH Bet"].split()[1][0] != "-" and row["AH Bet"].split()[1].split(".")[1] == "75")):
                                    td["AH Success"].append(col)
                                else:
                                    td["AH Fail"].append(col)

                if (row["OU Bet"] == row["OU Bet"]):
                    if ("Over" in row["OU Bet"] or "Under" in row["OU Bet"]):
                        if (row["OU Bet"].split()[1].split(".")[1] != "25" and row["OU Bet"].split()[1].split(".")[1] != "75"):
                            if ("Over" in row["OU Bet"]):
                                if (int(col.split(" -- ")[0]) + int(col.split(" -- ")[1]) > float(row["OU Bet"].split()[1])):
                                    td["OU Success"].append(col)
                                elif (int(col.split(" -- ")[0]) + int(col.split(" -- ")[1]) < float(row["OU Bet"].split()[1])):
                                    td["OU Fail"].append(col)
                            else:
                                if (int(col.split(" -- ")[0]) + int(col.split(" -- ")[1]) < float(row["OU Bet"].split()[1])):
                                    td["OU Success"].append(col)
                                elif (int(col.split(" -- ")[0]) + int(col.split(" -- ")[1]) > float(row["OU Bet"].split()[1])):
                                    td["OU Fail"].append(col)
                        elif (row["OU Bet"].split()[1].split(".")[1] == "25"):
                            if ("Over" in row["OU Bet"]):
                                if (int(col.split(" -- ")[0]) + int(col.split(" -- ")[1]) == float(row["OU Bet"].split()[1]) - 0.25):
                                    td["OU Fail"].append(col)
                                elif (int(col.split(" -- ")[0]) + int(col.split(" -- ")[1]) > float(row["OU Bet"].split()[1])):
                                    td["OU Success"].append(col)
                                else:
                                    td["OU Fail"].append(col)
                            else:
                                if (int(col.split(" -- ")[0]) + int(col.split(" -- ")[1]) == float(row["OU Bet"].split()[1]) - 0.25):
                                    td["OU Success"].append(col)
                                elif (int(col.split(" -- ")[0]) + int(col.split(" -- ")[1]) < float(row["OU Bet"].split()[1])):
                                    td["OU Success"].append(col)
                                else:
                                    td["OU Fail"].append(col)
                        else:
                            if ("Over" in row["OU Bet"]):
                                if (int(col.split(" -- ")[0]) + int(col.split(" -- ")[1]) == float(row["OU Bet"].split()[1]) + 0.25):
                                    td["OU Success"].append(col)
                                elif (int(col.split(" -- ")[0]) + int(col.split(" -- ")[1]) > float(row["OU Bet"].split()[1])):
                                    td["OU Success"].append(col)
                                else:
                                    td["OU Fail"].append(col)
                            else:
                                if (int(col.split(" -- ")[0]) + int(col.split(" -- ")[1]) == float(row["OU Bet"].split()[1]) + 0.25):
                                    td["OU Fail"].append(col)
                                elif (int(col.split(" -- ")[0]) + int(col.split(" -- ")[1]) < float(row["OU Bet"].split()[1])):
                                    td["OU Success"].append(col)
                                else:
                                    td["OU Fail"].append(col)
        for score in td["ML Success"]:
            td["ML P"] += row[score]
        for score in td["AH Success"]:
            td["AH P"] += row[score]
        for score in td["OU Success"]:
            td["OU P"] += row[score]
        div = td["ML P"] + td["AH P"] + td["OU P"]
        if (div == 0):
            mlAdj.append(0)
            ahAdj.append(0)
            ouAdj.append(0)
            continue
    if (not unique):
        pred.to_csv("./tempNaiveEval.csv")
    if (unique):
        now = datetime.datetime.now()
        pred.to_csv("./tempNaiveEval" + now.strftime("%H_%M_%S") + ".csv")
    return pred

#Takes the betting predictions after naive evaluation, a divisor for the kelly criterion to start at, number of divisors to try, how much to increment divisor by each loop
def seasonSim(pred, start, numLoops, inc, gamesToSim, noML = False, noAH = False, noOU = False, edgeExc = 1, superSim = False):
    print ("---SEASON SIM--------------------------------------------------------------------------------------------------------------------------------------------------------------")
    if (superSim):
        iter = 100000
    else:
        iter = 1000
    div = start
    betTypes = []
    if (not noML):
        betTypes.append("ML ")
    if (not noAH):
        betTypes.append("AH ")
    if (not noOU):
        betTypes.append("OU ")
    bestMed = -100
    for k in range(numLoops):
        #Season loop
        curIter = 0
        lowestReturn = 1000
        highestReturn = -1
        endingReturns = []
        betSizes = []
        weekWagers = []
        while (curIter < iter):
            # if (curIter % 100 == 0):
            #     print (curIter)
            pred = pred.sample(frac=1).reset_index(drop=True)
            bankroll = 1
            for i in range(gamesToSim):
                if (i % 10 == 0):
                    temp = 1
                    curWeekWagers = []
                for t in betTypes:
                    if (not np.isnan(pred.at[i, t + "Kelly"]) and not np.isnan(pred.at[i, t + "Edge"]) and np.isnan(pred.at[i, t + "Edge"]) < edgeExc):
                        if (np.isnan(pred.at[i, t + "Result"])):
                            betSizes.append(pred.at[i, t + "Kelly"]/div)
                            curWeekWagers.append(pred.at[i, t + "Kelly"]/div)
                        elif (pred.at[i, t + "Result"] == 1):
                            temp += (pred.at[i, t + "Kelly"]*((1/pred.at[i, t + "Book Prob"]) - 1)/div)
                            betSizes.append(pred.at[i, t + "Kelly"]/div)
                            curWeekWagers.append(pred.at[i, t + "Kelly"]/div)
                        else:
                            temp -= (pred.at[i, t + "Kelly"]/div)
                            betSizes.append(pred.at[i, t + "Kelly"]/div)
                            curWeekWagers.append(pred.at[i, t + "Kelly"]/div)
                if (i % 10 == 9):
                    bankroll = bankroll * temp
                    weekWagers.append(np.sum(curWeekWagers))
            curIter += 1
            if (bankroll - 1 > highestReturn):
                highestReturn = bankroll - 1
            if (bankroll - 1 < lowestReturn):
                lowestReturn = bankroll - 1
            endingReturns.append((bankroll - 1))
        print ("Level", k, "with div of", div)
        print ("Average Seasonal Return:", str(np.average(endingReturns)))
        print ("Median Seasonal Return:", str(np.median(endingReturns)))
        if (np.median(endingReturns) > bestMed):
            bestMed = np.median(endingReturns)
        print ("Standard Deviation:", np.std(endingReturns))
        print ("Lowest Observed Return:", max(lowestReturn,-1))
        print ("Highest Observed Return:", highestReturn)
        print ("Average Bet Size:", np.average(betSizes))
        print ("Average Bankroll Bets per Week:", np.average(weekWagers))
        temp = []
        for r in endingReturns:
            if (r <= 0):
                temp.append(1)
            else:
                temp.append(0)
        print ("Percent of Seasons Ending with less than 100% of bankroll:", np.average(temp))
        temp = []
        for r in endingReturns:
            if (r <= -0.25):
                temp.append(1)
            else:
                temp.append(0)
        print ("Percent of Seasons Ending with less than 75% of bankroll:", np.average(temp))
        temp = []
        for r in endingReturns:
            if (r <= -0.5):
                temp.append(1)
            else:
                temp.append(0)
        print ("Percent of Seasons Ending with less than 50% of bankroll:", np.average(temp))
        temp = []
        for r in endingReturns:
            if (r <= -0.75):
                temp.append(1)
            else:
                temp.append(0)
        print ("Percent of Seasons Ending with less than 25% of bankroll:", np.average(temp))
        print ("------------------------------------------------------------------------------------------------")
        div += inc
    return bestMed
