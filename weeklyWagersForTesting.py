import pandas as pd
import numpy as np
from miscFcns import standardizeTeamName
import rpy2.robjects as robjects
from WeibullCountModelFunctions.MLE import MLE
from WeibullCountModelFunctions.WeibullPMF import weibullPmf
from WeibullCountModelFunctions.frankCopula import copula
import itertools
import threading
import time
import sys

train = pd.read_csv('./EPL_Csvs/currentModelTrain/tempTrainPoissonMeansForWeibull.csv', encoding = "ISO-8859-1")
optimal = [1.2487857, 1.26181929, 0.11504448]
week = 6
while (week <= 11):
    mlDiv = 30
    ahDiv = 30
    ouDiv = 30

    def form(a, b, g = 3):
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

    mw2 = pd.read_csv('./EPL_Csvs/2020-21_Season/match_stats/MW2.csv', encoding = "ISO-8859-1")
    seasonDict = {}
    curIndex = 0
    while (curIndex < len(mw2.index)):
        if (standardizeTeamName(mw2.at[curIndex, "Home"]) not in seasonDict):
            seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])] = {}
            for side in sides:
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "ball_winning"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "chance_efficiency"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "shooting_efficiency"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "key_pass_pct"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "pass_success"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "dribble_success"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "tackle_success"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "xG"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "xPts"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "deep_pct"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "pass_to_touch_ratio"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "foul_rate"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "clear_rate"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "long_pass_pct"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "fwd_pass_pct"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "fwd_pass_aggressiveness"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "defensive_third_pct"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "final_third_pct"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "ppda"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "touch_aggression"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "pass_aggression"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "dribble_aggression"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "tackle_aggression"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "corner_rate"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "dispossession_rate"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "offsides_rate"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "cross_rate"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "through_rate"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "xG_aggression_adjustment"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])][side + "xG_efficiency"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])]["E_" + side + "ball_winning"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])]["E_" + side + "chance_efficiency"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])]["E_" + side + "shooting_efficiency"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])]["E_" + side + "key_pass_pct"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])]["E_" + side + "pass_success"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])]["E_" + side + "dribble_success"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])]["E_" + side + "tackle_success"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])]["E_" + side + "xG"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])]["E_" + side + "xPts"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])]["E_" + side + "xG_aggression_adjustment"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Home"])]["E_" + side + "xG_efficiency"] = []
        if (standardizeTeamName(mw2.at[curIndex, "Away"]) not in seasonDict):
            seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])] = {}
            for side in sides:
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "ball_winning"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "chance_efficiency"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "shooting_efficiency"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "key_pass_pct"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "pass_success"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "dribble_success"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "tackle_success"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "xG"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "xPts"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "deep_pct"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "pass_to_touch_ratio"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "foul_rate"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "clear_rate"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "long_pass_pct"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "fwd_pass_pct"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "fwd_pass_aggressiveness"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "defensive_third_pct"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "final_third_pct"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "ppda"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "touch_aggression"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "pass_aggression"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "dribble_aggression"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "tackle_aggression"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "corner_rate"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "dispossession_rate"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "offsides_rate"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "cross_rate"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "through_rate"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "xG_aggression_adjustment"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])][side + "xG_efficiency"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])]["E_" + side + "ball_winning"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])]["E_" + side + "chance_efficiency"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])]["E_" + side + "shooting_efficiency"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])]["E_" + side + "key_pass_pct"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])]["E_" + side + "pass_success"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])]["E_" + side + "dribble_success"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])]["E_" + side + "tackle_success"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])]["E_" + side + "xG"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])]["E_" + side + "xPts"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])]["E_" + side + "xG_aggression_adjustment"] = []
                seasonDict[standardizeTeamName(mw2.at[curIndex, "Away"])]["E_" + side + "xG_efficiency"] = []
        curIndex += 1


    for i in range(1,week):
        data = pd.read_csv('./EPL_Csvs/2020-21_Season/match_stats/MW' + str(i) + '.csv', encoding = "ISO-8859-1")
        #addition of the current game to the lists for each team
        for index, row in data.iterrows():
            for side in sides:
                if (side == ""):
                    seasonDict[standardizeTeamName(row["Home"])][side + "ball_winning"].append(float(row["Home Interceptions"]) / float(row["Away Total Passes"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "chance_efficiency"].append(float(row["Home xG"]) * 100 / float(row["Home Possession"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "shooting_efficiency"].append(float(row["Home Score"]) - float(row["Home xG"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "key_pass_pct"].append(float(row["Home Key Passes"]) / float(row["Home passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "pass_success"].append(float(row["Home Accurate Passes"]) / float(row["Home Total Passes"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "dribble_success"].append(float(row["Home Dribbles Won"]) / float(row["Home Dribbles Attempted"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "tackle_success"].append(float(row["Home Successful Tackles"]) / float(row["Home Tackles Attempted"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "xG"].append(row["Home xG"])
                    seasonDict[standardizeTeamName(row["Home"])][side + "xPts"].append(row["Home xPts"])
                    seasonDict[standardizeTeamName(row["Home"])][side + "deep_pct"].append(float(row["Home deep"]) / float(row["Home Accurate Passes"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "pass_to_touch_ratio"].append(float(row["Home Total Passes"]) / float(row["Home Touches"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "foul_rate"].append(float(row["Home Fouls"]) / float(row["Away Possession"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "clear_rate"].append(float(row["Home Clearances"]) / float(row["Away passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "long_pass_pct"].append(float(row["Home passlength_long"]) / (float(row["Home passlength_long"]) + float(row["Home passlength_short"])))
                    seasonDict[standardizeTeamName(row["Home"])][side + "fwd_pass_pct"].append(float(row["Home passdirection_forward"]) / (float(row["Home passdirection_backward"]) + float(row["Home passdirection_left"]) + float(row["Home passdirection_right"]) + float(row["Home passdirection_forward"])))
                    seasonDict[standardizeTeamName(row["Home"])][side + "fwd_pass_aggressiveness"].append(float(row["Home passdirection_forward"]) * float(row["Home Possession"]) / (float(row["Home passdirection_backward"]) + float(row["Home passdirection_left"]) + float(row["Home passdirection_right"])))
                    seasonDict[standardizeTeamName(row["Home"])][side + "defensive_third_pct"].append(float(row["Home passzone_defensive_third"]) / (float(row["Home passzone_defensive_third"]) + float(row["Home passzone_middle_third"]) + float(row["Home passzone_final_third"])))
                    seasonDict[standardizeTeamName(row["Home"])][side + "final_third_pct"].append(float(row["Home passzone_final_third"]) / (float(row["Home passzone_defensive_third"]) + float(row["Home passzone_middle_third"]) + float(row["Home passzone_final_third"])))
                    seasonDict[standardizeTeamName(row["Home"])][side + "ppda"].append(row["Home ppda"])
                    seasonDict[standardizeTeamName(row["Home"])][side + "touch_aggression"].append(float(row["Home Touches"]) / float(row["Home Possession"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "pass_aggression"].append(float(row["Home Total Passes"]) / float(row["Home Possession"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "dribble_aggression"].append(float(row["Home Dribbles Attempted"]) / float(row["Home Possession"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "tackle_aggression"].append(float(row["Home Tackles Attempted"]) / float(row["Away Possession"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "corner_rate"].append(float(row["Home passtype_corner"]) / float(row["Home passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "dispossession_rate"].append(float(row["Home Dispossessed"]) / float(row["Home Possession"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "offsides_rate"].append(float(row["Home Offsides"]) / float(row["Home Total Passes"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "cross_rate"].append(float(row["Home passtype_cross"]) / float(row["Home passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "through_rate"].append(float(row["Home passtype_through"]) / float(row["Home passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "xG_aggression_adjustment"].append(float(row["Home xG"]) * float(row["Home ppda"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "xG_efficiency"].append(float(row["Home xG"]) / float(row["Home passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Home"])]["E_" + side + "ball_winning"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Interceptions"]) / float(row["Away Total Passes"]))
                    seasonDict[standardizeTeamName(row["Home"])]["E_" + side + "chance_efficiency"].append((float(row["Away Pre Elo"])/1500) * float(row["Home xG"]) * 100 / float(row["Home Possession"]))
                    seasonDict[standardizeTeamName(row["Home"])]["E_" + side + "shooting_efficiency"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Score"]) - float(row["Home xG"]))
                    seasonDict[standardizeTeamName(row["Home"])]["E_" + side + "key_pass_pct"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Key Passes"]) / float(row["Home passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Home"])]["E_" + side + "pass_success"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Accurate Passes"]) / float(row["Home Total Passes"]))
                    seasonDict[standardizeTeamName(row["Home"])]["E_" + side + "dribble_success"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Dribbles Won"]) / float(row["Home Dribbles Attempted"]))
                    seasonDict[standardizeTeamName(row["Home"])]["E_" + side + "tackle_success"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Successful Tackles"]) / float(row["Home Tackles Attempted"]))
                    seasonDict[standardizeTeamName(row["Home"])]["E_" + side + "xG"].append((float(row["Away Pre Elo"])/1500) * row["Home xG"])
                    seasonDict[standardizeTeamName(row["Home"])]["E_" + side + "xPts"].append((float(row["Away Pre Elo"])/1500) * row["Home xPts"])
                    seasonDict[standardizeTeamName(row["Home"])]["E_" + side + "xG_aggression_adjustment"].append((float(row["Away Pre Elo"])/1500)  * (float(row["Home xG"]) * float(row["Home ppda"])))
                    seasonDict[standardizeTeamName(row["Home"])]["E_" + side + "xG_efficiency"].append((float(row["Away Pre Elo"])/1500)  * (float(row["Home xG"]) / float(row["Home passzone_final_third"])))
                    seasonDict[standardizeTeamName(row["Away"])][side + "ball_winning"].append(float(row["Away Interceptions"]) / float(row["Home Total Passes"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "chance_efficiency"].append(float(row["Away xG"]) * 100 / float(row["Away Possession"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "shooting_efficiency"].append(float(row["Away Score"]) - float(row["Away xG"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "key_pass_pct"].append(float(row["Away Key Passes"]) / float(row["Away passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "pass_success"].append(float(row["Away Accurate Passes"]) / float(row["Away Total Passes"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "dribble_success"].append(float(row["Away Dribbles Won"]) / float(row["Away Dribbles Attempted"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "tackle_success"].append(float(row["Away Successful Tackles"]) / float(row["Away Tackles Attempted"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "xG"].append(row["Away xG"])
                    seasonDict[standardizeTeamName(row["Away"])][side + "xPts"].append(row["Away xPts"])
                    seasonDict[standardizeTeamName(row["Away"])][side + "deep_pct"].append(float(row["Away deep"]) / float(row["Away Accurate Passes"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "pass_to_touch_ratio"].append(float(row["Away Total Passes"]) / float(row["Away Touches"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "foul_rate"].append(float(row["Away Fouls"]) / float(row["Home Possession"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "clear_rate"].append(float(row["Away Clearances"]) / float(row["Home passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "long_pass_pct"].append(float(row["Away passlength_long"]) / (float(row["Away passlength_long"]) + float(row["Away passlength_short"])))
                    seasonDict[standardizeTeamName(row["Away"])][side + "fwd_pass_pct"].append(float(row["Away passdirection_forward"]) / (float(row["Away passdirection_backward"]) + float(row["Away passdirection_left"]) + float(row["Away passdirection_right"]) + float(row["Away passdirection_forward"])))
                    seasonDict[standardizeTeamName(row["Away"])][side + "fwd_pass_aggressiveness"].append(float(row["Away passdirection_forward"]) * float(row["Away Possession"]) / (float(row["Away passdirection_backward"]) + float(row["Away passdirection_left"]) + float(row["Away passdirection_right"])))
                    seasonDict[standardizeTeamName(row["Away"])][side + "defensive_third_pct"].append(float(row["Away passzone_defensive_third"]) / (float(row["Away passzone_defensive_third"]) + float(row["Away passzone_middle_third"]) + float(row["Away passzone_final_third"])))
                    seasonDict[standardizeTeamName(row["Away"])][side + "final_third_pct"].append(float(row["Away passzone_final_third"]) / (float(row["Away passzone_defensive_third"]) + float(row["Away passzone_middle_third"]) + float(row["Away passzone_final_third"])))
                    seasonDict[standardizeTeamName(row["Away"])][side + "ppda"].append(row["Away ppda"])
                    seasonDict[standardizeTeamName(row["Away"])][side + "touch_aggression"].append(float(row["Away Touches"]) / float(row["Away Possession"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "pass_aggression"].append(float(row["Away Total Passes"]) / float(row["Away Possession"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "dribble_aggression"].append(float(row["Away Dribbles Attempted"]) / float(row["Away Possession"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "tackle_aggression"].append(float(row["Away Tackles Attempted"]) / float(row["Home Possession"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "corner_rate"].append(float(row["Away passtype_corner"]) / float(row["Away passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "dispossession_rate"].append(float(row["Away Dispossessed"]) / float(row["Away Possession"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "offsides_rate"].append(float(row["Away Offsides"]) / float(row["Away Total Passes"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "cross_rate"].append(float(row["Away passtype_cross"]) / float(row["Away passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "through_rate"].append(float(row["Away passtype_through"]) / float(row["Away passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "xG_aggression_adjustment"].append(float(row["Away xG"]) * float(row["Away ppda"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "xG_efficiency"].append(float(row["Away xG"]) / float(row["Away passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Away"])]["E_" + side + "ball_winning"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Interceptions"]) / float(row["Home Total Passes"]))
                    seasonDict[standardizeTeamName(row["Away"])]["E_" + side + "chance_efficiency"].append((float(row["Home Pre Elo"])/1500) * float(row["Away xG"]) * 100 / float(row["Away Possession"]))
                    seasonDict[standardizeTeamName(row["Away"])]["E_" + side + "shooting_efficiency"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Score"]) - float(row["Away xG"]))
                    seasonDict[standardizeTeamName(row["Away"])]["E_" + side + "key_pass_pct"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Key Passes"]) / float(row["Away passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Away"])]["E_" + side + "pass_success"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Accurate Passes"]) / float(row["Away Total Passes"]))
                    seasonDict[standardizeTeamName(row["Away"])]["E_" + side + "dribble_success"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Dribbles Won"]) / float(row["Away Dribbles Attempted"]))
                    seasonDict[standardizeTeamName(row["Away"])]["E_" + side + "tackle_success"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Successful Tackles"]) / float(row["Away Tackles Attempted"]))
                    seasonDict[standardizeTeamName(row["Away"])]["E_" + side + "xG"].append((float(row["Home Pre Elo"])/1500) * row["Away xG"])
                    seasonDict[standardizeTeamName(row["Away"])]["E_" + side + "xPts"].append((float(row["Home Pre Elo"])/1500) * row["Away xPts"])
                    seasonDict[standardizeTeamName(row["Away"])]["E_" + side + "xG_aggression_adjustment"].append((float(row["Home Pre Elo"])/1500)  * (float(row["Away xG"]) * float(row["Away ppda"])))
                    seasonDict[standardizeTeamName(row["Away"])]["E_" + side + "xG_efficiency"].append((float(row["Home Pre Elo"])/1500)  * (float(row["Away xG"]) / float(row["Away passzone_final_third"])))
                else:
                    seasonDict[standardizeTeamName(row["Away"])][side + "ball_winning"].append(float(row["Home Interceptions"]) / float(row["Away Total Passes"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "chance_efficiency"].append(float(row["Home xG"]) * 100 / float(row["Home Possession"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "shooting_efficiency"].append(float(row["Home Score"]) - float(row["Home xG"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "key_pass_pct"].append(float(row["Home Key Passes"]) / float(row["Home passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "pass_success"].append(float(row["Home Accurate Passes"]) / float(row["Home Total Passes"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "dribble_success"].append(float(row["Home Dribbles Won"]) / float(row["Home Dribbles Attempted"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "tackle_success"].append(float(row["Home Successful Tackles"]) / float(row["Home Tackles Attempted"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "xG"].append(row["Home xG"])
                    seasonDict[standardizeTeamName(row["Away"])][side + "xPts"].append(row["Home xPts"])
                    seasonDict[standardizeTeamName(row["Away"])][side + "deep_pct"].append(float(row["Home deep"]) / float(row["Home Accurate Passes"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "pass_to_touch_ratio"].append(float(row["Home Total Passes"]) / float(row["Home Touches"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "foul_rate"].append(float(row["Home Fouls"]) / float(row["Away Possession"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "clear_rate"].append(float(row["Home Clearances"]) / float(row["Away passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "long_pass_pct"].append(float(row["Home passlength_long"]) / (float(row["Home passlength_long"]) + float(row["Home passlength_short"])))
                    seasonDict[standardizeTeamName(row["Away"])][side + "fwd_pass_pct"].append(float(row["Home passdirection_forward"]) / (float(row["Home passdirection_backward"]) + float(row["Home passdirection_left"]) + float(row["Home passdirection_right"]) + float(row["Home passdirection_forward"])))
                    seasonDict[standardizeTeamName(row["Away"])][side + "fwd_pass_aggressiveness"].append(float(row["Home passdirection_forward"]) * float(row["Home Possession"]) / (float(row["Home passdirection_backward"]) + float(row["Home passdirection_left"]) + float(row["Home passdirection_right"])))
                    seasonDict[standardizeTeamName(row["Away"])][side + "defensive_third_pct"].append(float(row["Home passzone_defensive_third"]) / (float(row["Home passzone_defensive_third"]) + float(row["Home passzone_middle_third"]) + float(row["Home passzone_final_third"])))
                    seasonDict[standardizeTeamName(row["Away"])][side + "final_third_pct"].append(float(row["Home passzone_final_third"]) / (float(row["Home passzone_defensive_third"]) + float(row["Home passzone_middle_third"]) + float(row["Home passzone_final_third"])))
                    seasonDict[standardizeTeamName(row["Away"])][side + "ppda"].append(row["Home ppda"])
                    seasonDict[standardizeTeamName(row["Away"])][side + "touch_aggression"].append(float(row["Home Touches"]) / float(row["Home Possession"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "pass_aggression"].append(float(row["Home Total Passes"]) / float(row["Home Possession"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "dribble_aggression"].append(float(row["Home Dribbles Attempted"]) / float(row["Home Possession"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "tackle_aggression"].append(float(row["Home Tackles Attempted"]) / float(row["Away Possession"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "corner_rate"].append(float(row["Home passtype_corner"]) / float(row["Home passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "dispossession_rate"].append(float(row["Home Dispossessed"]) / float(row["Home Possession"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "offsides_rate"].append(float(row["Home Offsides"]) / float(row["Home Total Passes"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "cross_rate"].append(float(row["Home passtype_cross"]) / float(row["Home passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "through_rate"].append(float(row["Home passtype_through"]) / float(row["Home passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "xG_aggression_adjustment"].append(float(row["Home xG"]) * float(row["Home ppda"]))
                    seasonDict[standardizeTeamName(row["Away"])][side + "xG_efficiency"].append(float(row["Home xG"]) / float(row["Home passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Away"])]["E_" + side + "ball_winning"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Interceptions"]) / float(row["Away Total Passes"]))
                    seasonDict[standardizeTeamName(row["Away"])]["E_" + side + "chance_efficiency"].append((float(row["Away Pre Elo"])/1500) * float(row["Home xG"]) * 100 / float(row["Home Possession"]))
                    seasonDict[standardizeTeamName(row["Away"])]["E_" + side + "shooting_efficiency"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Score"]) - float(row["Home xG"]))
                    seasonDict[standardizeTeamName(row["Away"])]["E_" + side + "key_pass_pct"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Key Passes"]) / float(row["Home passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Away"])]["E_" + side + "pass_success"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Accurate Passes"]) / float(row["Home Total Passes"]))
                    seasonDict[standardizeTeamName(row["Away"])]["E_" + side + "dribble_success"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Dribbles Won"]) / float(row["Home Dribbles Attempted"]))
                    seasonDict[standardizeTeamName(row["Away"])]["E_" + side + "tackle_success"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Successful Tackles"]) / float(row["Home Tackles Attempted"]))
                    seasonDict[standardizeTeamName(row["Away"])]["E_" + side + "xG"].append((float(row["Away Pre Elo"])/1500) * row["Home xG"])
                    seasonDict[standardizeTeamName(row["Away"])]["E_" + side + "xPts"].append((float(row["Away Pre Elo"])/1500) * row["Home xPts"])
                    seasonDict[standardizeTeamName(row["Away"])]["E_" + side + "xG_aggression_adjustment"].append((float(row["Away Pre Elo"])/1500)  * (float(row["Home xG"]) * float(row["Home ppda"])))
                    seasonDict[standardizeTeamName(row["Away"])]["E_" + side + "xG_efficiency"].append((float(row["Away Pre Elo"])/1500)  * (float(row["Home xG"]) / float(row["Home passzone_final_third"])))
                    seasonDict[standardizeTeamName(row["Home"])][side + "ball_winning"].append(float(row["Away Interceptions"]) / float(row["Home Total Passes"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "chance_efficiency"].append(float(row["Away xG"]) * 100 / float(row["Away Possession"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "shooting_efficiency"].append(float(row["Away Score"]) - float(row["Away xG"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "key_pass_pct"].append(float(row["Away Key Passes"]) / float(row["Away passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "pass_success"].append(float(row["Away Accurate Passes"]) / float(row["Away Total Passes"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "dribble_success"].append(float(row["Away Dribbles Won"]) / float(row["Away Dribbles Attempted"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "tackle_success"].append(float(row["Away Successful Tackles"]) / float(row["Away Tackles Attempted"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "xG"].append(row["Away xG"])
                    seasonDict[standardizeTeamName(row["Home"])][side + "xPts"].append(row["Away xPts"])
                    seasonDict[standardizeTeamName(row["Home"])][side + "deep_pct"].append(float(row["Away deep"]) / float(row["Away Accurate Passes"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "pass_to_touch_ratio"].append(float(row["Away Total Passes"]) / float(row["Away Touches"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "foul_rate"].append(float(row["Away Fouls"]) / float(row["Home Possession"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "clear_rate"].append(float(row["Away Clearances"]) / float(row["Home passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "long_pass_pct"].append(float(row["Away passlength_long"]) / (float(row["Away passlength_long"]) + float(row["Away passlength_short"])))
                    seasonDict[standardizeTeamName(row["Home"])][side + "fwd_pass_pct"].append(float(row["Away passdirection_forward"]) / (float(row["Away passdirection_backward"]) + float(row["Away passdirection_left"]) + float(row["Away passdirection_right"]) + float(row["Away passdirection_forward"])))
                    seasonDict[standardizeTeamName(row["Home"])][side + "fwd_pass_aggressiveness"].append(float(row["Away passdirection_forward"]) * float(row["Away Possession"]) / (float(row["Away passdirection_backward"]) + float(row["Away passdirection_left"]) + float(row["Away passdirection_right"])))
                    seasonDict[standardizeTeamName(row["Home"])][side + "defensive_third_pct"].append(float(row["Away passzone_defensive_third"]) / (float(row["Away passzone_defensive_third"]) + float(row["Away passzone_middle_third"]) + float(row["Away passzone_final_third"])))
                    seasonDict[standardizeTeamName(row["Home"])][side + "final_third_pct"].append(float(row["Away passzone_final_third"]) / (float(row["Away passzone_defensive_third"]) + float(row["Away passzone_middle_third"]) + float(row["Away passzone_final_third"])))
                    seasonDict[standardizeTeamName(row["Home"])][side + "ppda"].append(row["Away ppda"])
                    seasonDict[standardizeTeamName(row["Home"])][side + "touch_aggression"].append(float(row["Away Touches"]) / float(row["Away Possession"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "pass_aggression"].append(float(row["Away Total Passes"]) / float(row["Away Possession"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "dribble_aggression"].append(float(row["Away Dribbles Attempted"]) / float(row["Away Possession"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "tackle_aggression"].append(float(row["Away Tackles Attempted"]) / float(row["Home Possession"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "corner_rate"].append(float(row["Away passtype_corner"]) / float(row["Away passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "dispossession_rate"].append(float(row["Away Dispossessed"]) / float(row["Away Possession"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "offsides_rate"].append(float(row["Away Offsides"]) / float(row["Away Total Passes"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "cross_rate"].append(float(row["Away passtype_cross"]) / float(row["Away passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "through_rate"].append(float(row["Away passtype_through"]) / float(row["Away passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "xG_aggression_adjustment"].append(float(row["Away xG"]) * float(row["Away ppda"]))
                    seasonDict[standardizeTeamName(row["Home"])][side + "xG_efficiency"].append(float(row["Away xG"]) / float(row["Away passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Home"])]["E_" + side + "ball_winning"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Interceptions"]) / float(row["Home Total Passes"]))
                    seasonDict[standardizeTeamName(row["Home"])]["E_" + side + "chance_efficiency"].append((float(row["Home Pre Elo"])/1500) * float(row["Away xG"]) * 100 / float(row["Away Possession"]))
                    seasonDict[standardizeTeamName(row["Home"])]["E_" + side + "shooting_efficiency"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Score"]) - float(row["Away xG"]))
                    seasonDict[standardizeTeamName(row["Home"])]["E_" + side + "key_pass_pct"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Key Passes"]) / float(row["Away passzone_final_third"]))
                    seasonDict[standardizeTeamName(row["Home"])]["E_" + side + "pass_success"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Accurate Passes"]) / float(row["Away Total Passes"]))
                    seasonDict[standardizeTeamName(row["Home"])]["E_" + side + "dribble_success"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Dribbles Won"]) / float(row["Away Dribbles Attempted"]))
                    seasonDict[standardizeTeamName(row["Home"])]["E_" + side + "tackle_success"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Successful Tackles"]) / float(row["Away Tackles Attempted"]))
                    seasonDict[standardizeTeamName(row["Home"])]["E_" + side + "xG"].append((float(row["Home Pre Elo"])/1500) * row["Away xG"])
                    seasonDict[standardizeTeamName(row["Home"])]["E_" + side + "xPts"].append((float(row["Home Pre Elo"])/1500) * row["Away xPts"])
                    seasonDict[standardizeTeamName(row["Home"])]["E_" + side + "xG_aggression_adjustment"].append((float(row["Home Pre Elo"])/1500)  * (float(row["Away xG"]) * float(row["Away ppda"])))
                    seasonDict[standardizeTeamName(row["Home"])]["E_" + side + "xG_efficiency"].append((float(row["Home Pre Elo"])/1500)  * (float(row["Away xG"]) / float(row["Away passzone_final_third"])))


    mwp = pd.read_csv('./EPL_Csvs/2020-21_Season/match_odds/MW' + str(week) + '.csv', encoding = "ISO-8859-1")
    for index, row in mwp.iterrows():
        for side in haSide:
            for tCat in timeAdjCats:
                if (side == "home_expected_" and tCat == ""):
                    dict[tCat + side + "ball_winning"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "ball_winning"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "ball_winning"])) / 2)
                    dict[tCat + side + "chance_efficiency"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "chance_efficiency"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "chance_efficiency"])) / 2)
                    dict[tCat + side + "shooting_efficiency"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "shooting_efficiency"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "shooting_efficiency"])) / 2)
                    dict[tCat + side + "key_pass_pct"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "key_pass_pct"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "key_pass_pct"])) / 2)
                    dict[tCat + side + "pass_success"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "pass_success"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "pass_success"])) / 2)
                    dict[tCat + side + "dribble_success"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "dribble_success"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "dribble_success"])) / 2)
                    dict[tCat + side + "tackle_success"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "tackle_success"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "tackle_success"])) / 2)
                    dict[tCat + side + "xG"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "xG"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "xG"])) / 2)
                    dict[tCat + side + "xPts"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "xPts"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "xPts"])) / 2)
                    dict[tCat + side + "deep_pct"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "deep_pct"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "deep_pct"])) / 2)
                    dict[tCat + side + "pass_to_touch_ratio"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "pass_to_touch_ratio"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "pass_to_touch_ratio"])) / 2)
                    dict[tCat + side + "foul_rate"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "foul_rate"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "foul_rate"])) / 2)
                    dict[tCat + side + "clear_rate"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "clear_rate"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "clear_rate"])) / 2)
                    dict[tCat + side + "long_pass_pct"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "long_pass_pct"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "long_pass_pct"])) / 2)
                    dict[tCat + side + "fwd_pass_pct"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "fwd_pass_pct"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "fwd_pass_pct"])) / 2)
                    dict[tCat + side + "fwd_pass_aggressiveness"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "fwd_pass_aggressiveness"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "fwd_pass_aggressiveness"])) / 2)
                    dict[tCat + side + "defensive_third_pct"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "defensive_third_pct"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "defensive_third_pct"])) / 2)
                    dict[tCat + side + "final_third_pct"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "final_third_pct"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "final_third_pct"])) / 2)
                    dict[tCat + side + "ppda"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "ppda"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "ppda"])) / 2)
                    dict[tCat + side + "touch_aggression"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "touch_aggression"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "touch_aggression"])) / 2)
                    dict[tCat + side + "pass_aggression"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "pass_aggression"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "pass_aggression"])) / 2)
                    dict[tCat + side + "dribble_aggression"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "dribble_aggression"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "dribble_aggression"])) / 2)
                    dict[tCat + side + "tackle_aggression"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "tackle_aggression"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "tackle_aggression"])) / 2)
                    dict[tCat + side + "corner_rate"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "corner_rate"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "corner_rate"])) / 2)
                    dict[tCat + side + "dispossession_rate"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "dispossession_rate"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "dispossession_rate"])) / 2)
                    dict[tCat + side + "offsides_rate"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "offsides_rate"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "offsides_rate"])) / 2)
                    dict[tCat + side + "cross_rate"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "cross_rate"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "cross_rate"])) / 2)
                    dict[tCat + side + "through_rate"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "through_rate"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "through_rate"])) / 2)
                    dict[tCat + side + "xG_aggression_adjustment"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "xG_aggression_adjustment"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "xG_aggression_adjustment"])) / 2)
                    dict[tCat + side + "xG_efficiency"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["" + "xG_efficiency"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["X_" + "xG_efficiency"])) / 2)
                elif (side == "away_expected_" and tCat == ""):
                    dict[tCat + side + "ball_winning"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "ball_winning"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "ball_winning"])) / 2)
                    dict[tCat + side + "chance_efficiency"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "chance_efficiency"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "chance_efficiency"])) / 2)
                    dict[tCat + side + "shooting_efficiency"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "shooting_efficiency"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "shooting_efficiency"])) / 2)
                    dict[tCat + side + "key_pass_pct"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "key_pass_pct"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "key_pass_pct"])) / 2)
                    dict[tCat + side + "pass_success"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "pass_success"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "pass_success"])) / 2)
                    dict[tCat + side + "dribble_success"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "dribble_success"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "dribble_success"])) / 2)
                    dict[tCat + side + "tackle_success"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "tackle_success"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "tackle_success"])) / 2)
                    dict[tCat + side + "xG"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "xG"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "xG"])) / 2)
                    dict[tCat + side + "xPts"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "xPts"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "xPts"])) / 2)
                    dict[tCat + side + "deep_pct"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "deep_pct"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "deep_pct"])) / 2)
                    dict[tCat + side + "pass_to_touch_ratio"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "pass_to_touch_ratio"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "pass_to_touch_ratio"])) / 2)
                    dict[tCat + side + "foul_rate"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "foul_rate"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "foul_rate"])) / 2)
                    dict[tCat + side + "clear_rate"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "clear_rate"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "clear_rate"])) / 2)
                    dict[tCat + side + "long_pass_pct"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "long_pass_pct"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "long_pass_pct"])) / 2)
                    dict[tCat + side + "fwd_pass_pct"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "fwd_pass_pct"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "fwd_pass_pct"])) / 2)
                    dict[tCat + side + "fwd_pass_aggressiveness"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "fwd_pass_aggressiveness"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "fwd_pass_aggressiveness"])) / 2)
                    dict[tCat + side + "defensive_third_pct"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "defensive_third_pct"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "defensive_third_pct"])) / 2)
                    dict[tCat + side + "final_third_pct"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "final_third_pct"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "final_third_pct"])) / 2)
                    dict[tCat + side + "ppda"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "ppda"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "ppda"])) / 2)
                    dict[tCat + side + "touch_aggression"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "touch_aggression"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "touch_aggression"])) / 2)
                    dict[tCat + side + "pass_aggression"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "pass_aggression"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "pass_aggression"])) / 2)
                    dict[tCat + side + "dribble_aggression"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "dribble_aggression"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "dribble_aggression"])) / 2)
                    dict[tCat + side + "tackle_aggression"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "tackle_aggression"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "tackle_aggression"])) / 2)
                    dict[tCat + side + "corner_rate"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "corner_rate"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "corner_rate"])) / 2)
                    dict[tCat + side + "dispossession_rate"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "dispossession_rate"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "dispossession_rate"])) / 2)
                    dict[tCat + side + "offsides_rate"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "offsides_rate"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "offsides_rate"])) / 2)
                    dict[tCat + side + "cross_rate"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "cross_rate"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "cross_rate"])) / 2)
                    dict[tCat + side + "through_rate"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "through_rate"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "through_rate"])) / 2)
                    dict[tCat + side + "xG_aggression_adjustment"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "xG_aggression_adjustment"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "xG_aggression_adjustment"])) / 2)
                    dict[tCat + side + "xG_efficiency"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["" + "xG_efficiency"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["X_" + "xG_efficiency"])) / 2)
                else:
                    if (len(seasonDict[standardizeTeamName(row["Home"])]["" + "ball_winning"]) < 5 or len(seasonDict[standardizeTeamName(row["Away"])]["" + "ball_winning"]) < 5):
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
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "ball_winning"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "ball_winning"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "ball_winning"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "chance_efficiency"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "chance_efficiency"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "chance_efficiency"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "shooting_efficiency"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "shooting_efficiency"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "shooting_efficiency"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "key_pass_pct"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "key_pass_pct"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "key_pass_pct"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "pass_success"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "pass_success"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "pass_success"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "dribble_success"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "dribble_success"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "dribble_success"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "tackle_success"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "tackle_success"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "tackle_success"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "xG"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "xG"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "xG"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "xPts"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "xPts"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "xPts"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "deep_pct"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "deep_pct"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "deep_pct"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "pass_to_touch_ratio"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "pass_to_touch_ratio"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "pass_to_touch_ratio"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "foul_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "foul_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "foul_rate"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "clear_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "clear_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "clear_rate"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "long_pass_pct"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "long_pass_pct"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "long_pass_pct"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "fwd_pass_pct"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "fwd_pass_pct"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "fwd_pass_pct"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "fwd_pass_aggressiveness"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "fwd_pass_aggressiveness"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "fwd_pass_aggressiveness"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "defensive_third_pct"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "defensive_third_pct"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "defensive_third_pct"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "final_third_pct"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "final_third_pct"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "final_third_pct"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "ppda"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "ppda"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "ppda"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "touch_aggression"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "touch_aggression"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "touch_aggression"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "pass_aggression"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "pass_aggression"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "pass_aggression"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "dribble_aggression"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "dribble_aggression"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "dribble_aggression"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "tackle_aggression"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "tackle_aggression"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "tackle_aggression"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "corner_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "corner_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "corner_rate"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "dispossession_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "dispossession_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "dispossession_rate"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "offsides_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "offsides_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "offsides_rate"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "cross_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "cross_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "cross_rate"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "through_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "through_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "through_rate"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "xG_aggression_adjustment"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "xG_aggression_adjustment"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "xG_aggression_adjustment"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["" + "xG_efficiency"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["X_" + "xG_efficiency"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "xG_efficiency"].append(form(tempH, tempA))
                    else:
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "ball_winning"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "ball_winning"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "ball_winning"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "chance_efficiency"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "chance_efficiency"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "chance_efficiency"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "shooting_efficiency"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "shooting_efficiency"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "shooting_efficiency"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "key_pass_pct"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "key_pass_pct"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "key_pass_pct"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "pass_success"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "pass_success"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "pass_success"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "dribble_success"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "dribble_success"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "dribble_success"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "tackle_success"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "tackle_success"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "tackle_success"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "xG"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "xG"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "xG"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "xPts"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "xPts"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "xPts"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "deep_pct"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "deep_pct"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "deep_pct"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "pass_to_touch_ratio"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "pass_to_touch_ratio"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "pass_to_touch_ratio"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "foul_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "foul_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "foul_rate"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "clear_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "clear_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "clear_rate"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "long_pass_pct"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "long_pass_pct"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "long_pass_pct"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "fwd_pass_pct"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "fwd_pass_pct"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "fwd_pass_pct"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "fwd_pass_aggressiveness"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "fwd_pass_aggressiveness"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "fwd_pass_aggressiveness"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "defensive_third_pct"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "defensive_third_pct"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "defensive_third_pct"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "final_third_pct"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "final_third_pct"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "final_third_pct"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "ppda"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "ppda"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "ppda"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "touch_aggression"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "touch_aggression"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "touch_aggression"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "pass_aggression"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "pass_aggression"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "pass_aggression"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "dribble_aggression"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "dribble_aggression"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "dribble_aggression"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "tackle_aggression"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "tackle_aggression"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "tackle_aggression"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "corner_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "corner_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "corner_rate"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "dispossession_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "dispossession_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "dispossession_rate"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "offsides_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "offsides_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "offsides_rate"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "cross_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "cross_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "cross_rate"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "through_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "through_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "through_rate"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "xG_aggression_adjustment"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "xG_aggression_adjustment"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "xG_aggression_adjustment"].append(form(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[standardizeTeamName(row["Away"])]["" + "xG_efficiency"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[standardizeTeamName(row["Home"])]["X_" + "xG_efficiency"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "xG_efficiency"].append(form(tempH, tempA))
            if (side == "home_expected_"):
                dict["E_" + side + "ball_winning"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["E_" + "ball_winning"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["E_X_" + "ball_winning"])) / 2)
                dict["E_" + side + "chance_efficiency"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["E_" + "chance_efficiency"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["E_X_" + "chance_efficiency"])) / 2)
                dict["E_" + side + "shooting_efficiency"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["E_" + "shooting_efficiency"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["E_X_" + "shooting_efficiency"])) / 2)
                dict["E_" + side + "key_pass_pct"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["E_" + "key_pass_pct"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["E_X_" + "key_pass_pct"])) / 2)
                dict["E_" + side + "pass_success"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["E_" + "pass_success"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["E_X_" + "pass_success"])) / 2)
                dict["E_" + side + "dribble_success"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["E_" + "dribble_success"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["E_X_" + "dribble_success"])) / 2)
                dict["E_" + side + "tackle_success"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["E_" + "tackle_success"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["E_X_" + "tackle_success"])) / 2)
                dict["E_" + side + "xG"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["E_" + "xG"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["E_X_" + "xG"])) / 2)
                dict["E_" + side + "xPts"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["E_" + "xPts"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["E_X_" + "xPts"])) / 2)
                dict["E_" + side + "xG_aggression_adjustment"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["E_" + "xG_aggression_adjustment"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["E_X_" + "xG_aggression_adjustment"])) / 2)
                dict["E_" + side + "xG_efficiency"].append((np.average(seasonDict[standardizeTeamName(row["Home"])]["E_" + "xG_efficiency"]) + np.average(seasonDict[standardizeTeamName(row["Away"])]["E_X_" + "xG_efficiency"])) / 2)
            else:
                dict["E_" + side + "ball_winning"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["E_" + "ball_winning"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["E_X_" + "ball_winning"])) / 2)
                dict["E_" + side + "chance_efficiency"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["E_" + "chance_efficiency"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["E_X_" + "chance_efficiency"])) / 2)
                dict["E_" + side + "shooting_efficiency"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["E_" + "shooting_efficiency"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["E_X_" + "shooting_efficiency"])) / 2)
                dict["E_" + side + "key_pass_pct"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["E_" + "key_pass_pct"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["E_X_" + "key_pass_pct"])) / 2)
                dict["E_" + side + "pass_success"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["E_" + "pass_success"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["E_X_" + "pass_success"])) / 2)
                dict["E_" + side + "dribble_success"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["E_" + "dribble_success"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["E_X_" + "dribble_success"])) / 2)
                dict["E_" + side + "tackle_success"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["E_" + "tackle_success"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["E_X_" + "tackle_success"])) / 2)
                dict["E_" + side + "xG"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["E_" + "xG"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["E_X_" + "xG"])) / 2)
                dict["E_" + side + "xPts"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["E_" + "xPts"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["E_X_" + "xPts"])) / 2)
                dict["E_" + side + "xG_aggression_adjustment"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["E_" + "xG_aggression_adjustment"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["E_X_" + "xG_aggression_adjustment"])) / 2)
                dict["E_" + side + "xG_efficiency"].append((np.average(seasonDict[standardizeTeamName(row["Away"])]["E_" + "xG_efficiency"]) + np.average(seasonDict[standardizeTeamName(row["Home"])]["E_X_" + "xG_efficiency"])) / 2)
    for key in dict:
        mwp[key] = dict[key]


    dict = {"Date":[], "Team":[], "Home Field":[]}
    sides = ["expected", "opponent_expected"]
    for col in mwp.columns:
        if ("home_expected" in col):
            for side in sides:
                dict[col.split("home_expected")[0] + side + col.split("home_expected")[1]] = []

    for index, row in mwp.iterrows():
        dict["Date"].append(row["Date"])
        dict["Team"].append(row["Home"])
        dict["Home Field"].append(1)
        for col in mwp.columns:
            if ("home_expected" in col):
                dict[col.split("home_expected")[0] + "expected" + col.split("home_expected")[1]].append(row[col])
            elif ("away_expected" in col):
                dict[col.split("away_expected")[0] + "opponent_expected" + col.split("away_expected")[1]].append(row[col])
        dict["Date"].append(row["Date"])
        dict["Team"].append(row["Away"])
        dict["Home Field"].append(0)
        for col in mwp.columns:
            if ("away_expected" in col):
                dict[col.split("away_expected")[0] + "expected" + col.split("away_expected")[1]].append(row[col])
            elif ("home_expected" in col):
                dict[col.split("home_expected")[0] + "opponent_expected" + col.split("home_expected")[1]].append(row[col])

    dfFinal = pd.DataFrame.from_dict(dict)


    #Remove this when ready - this will remove teams who havent played 3 games
    #dfFinal = dfFinal.dropna()

    dfFinal.to_csv("./EPL_Csvs/2020-21_Season/intermediate.csv", index=False)

    r = robjects.r
    r.source("weeklyPoissonRegressionTEMPTEST.R")

    df = pd.read_csv('./EPL_Csvs/2020-21_Season/intermediate.csv', encoding = "ISO-8859-1")

    newDict = {}
    sides = ["H_", "A_"]
    for col in df.columns:
        for side in sides:
            newDict[side + col] = []
    cur = 0
    while (cur < len(df.index)):
        for col in df.columns:
            newDict["H_" + col].append(df.at[cur, col])
            newDict["A_" + col].append(df.at[cur+1,col])
        cur += 2


    df = pd.DataFrame.from_dict(newDict)

    dict = {}
    alphaDictH = {}
    alphaDictA = {}
    cur = 0
    n = 0
    while (cur < len(df.index)):
        hCdf = []
        aCdf = []
        for j in range(11):
            if (j == 0):
                hCdf.append(weibullPmf(j, df.at[cur, "H_Poisson Mean Prediction"], optimal[0], alphaDictH))
                aCdf.append(weibullPmf(j, df.at[cur, "A_Poisson Mean Prediction"], optimal[1], alphaDictA))
            else:
                hCdf.append(weibullPmf(j, df.at[cur, "H_Poisson Mean Prediction"], optimal[0], alphaDictH) + hCdf[j-1])
                aCdf.append(weibullPmf(j, df.at[cur, "A_Poisson Mean Prediction"], optimal[1], alphaDictA) + aCdf[j-1])
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
                            tempProb -= dict[p][q][n]
                    dict[j][k].append(tempProb)
        cur += 1
        n += 1

    for j in range(11):
        for k in range(11):
            df[str(j) + " -- " + str(k)] = dict[j][k]


    #weibullBettingProbabilities
    dict = {}
    for col in mwp.columns:
        if ("1" == col or "X" == col or "2" == col or "AH" in col or "Over" in col or "Under" in col):
            dict["P(" + col + ")"] = []
    dict["P(AH 0.0 (1))"] = []
    dict["P(AH 0.0 (2))"] = []

    curIndex = 0
    goalDiffs = [-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6]
    ouList = [0,1,2,3,4,5,6,7,8,9]
    scoreLines = []
    for col in df.columns:
        if ("--" in col):
            scoreLines.append(col)
    while (curIndex < len(df.index)):
        table = [[],[],[],[],[],[],[],[],[],[],[]]
        for score in scoreLines:
            table[int(score.split(" -- ")[0])].append(df.at[curIndex, score])
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
        curIndex += 1
    for key in dict:
        mwp[key] = dict[key]

    dict = {"Date":[],"Home":[],"Away":[],"Bet":[],"Book Odds":[],"Edge":[],"P":[],"Bet Size":[],"In Euros":[]}
    #I NEED TO CODE THIS SO I DONT HAVE TO ADJUST EVERY TIME
    bankroll = 30000*0.86 #in euros
    for index, row in mwp.iterrows():
        ml = {"edge":0,"colName":""}
        ah = {"edge":0,"colName":""}
        ou = {"edge":0,"colName":""}
        for col in mwp.columns:
            if (("1" == col or "X" == col or "2" == col) and "P(" not in col):
                if ((row["P(" + col + ")"] - (1/row[col])) > ml["edge"]):
                    ml["edge"] = row["P(" + col + ")"] - (1/row[col])
                    ml["colName"] = col
            if ("AH" in col and "P(" not in col and not np.isnan(row[col]) and row[col] != 1):
                if ((row["P(" + col + ")"] - (1/row[col])) > ah["edge"]):
                    ah["edge"] = row["P(" + col + ")"] - (1/row[col])
                    ah["colName"] = col
            if (("Over" in col or "Under" in col) and "P(" not in col and not np.isnan(row[col]) and row[col] != 1):
                if ((row["P(" + col + ")"] - (1/row[col])) > ou["edge"]):
                    ou["edge"] = row["P(" + col + ")"] - (1/row[col])
                    ou["colName"] = col
        if (ml["edge"] > 0):
            dict["Date"].append(row["Date"])
            dict["Home"].append(row["Home"])
            dict["Away"].append(row["Away"])
            dict["Bet"].append(ml["colName"])
            dict["Book Odds"].append(row[ml["colName"]])
            dict["Edge"].append(ml["edge"])
            dict["P"].append(row["P(" + ml["colName"] + ")"])
            dict["Bet Size"].append(((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))/mlDiv)
            dict["In Euros"].append(((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*bankroll/mlDiv)
        if (ah["edge"] > 0):
            dict["Date"].append(row["Date"])
            dict["Home"].append(row["Home"])
            dict["Away"].append(row["Away"])
            dict["Bet"].append(ah["colName"])
            dict["Book Odds"].append(row[ah["colName"]])
            dict["Edge"].append(ah["edge"])
            dict["P"].append(row["P(" + ah["colName"] + ")"])
            dict["Bet Size"].append(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))/ahDiv)
            dict["In Euros"].append(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*bankroll/ahDiv)
        if (ou["edge"] > 0):
            dict["Date"].append(row["Date"])
            dict["Home"].append(row["Home"])
            dict["Away"].append(row["Away"])
            dict["Bet"].append(ou["colName"])
            dict["Book Odds"].append(row[ou["colName"]])
            dict["Edge"].append(ou["edge"])
            dict["P"].append(row["P(" + ou["colName"] + ")"])
            dict["Bet Size"].append(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))/ouDiv)
            dict["In Euros"].append(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*bankroll/ouDiv)

    final = pd.DataFrame.from_dict(dict)
    final.to_csv("./EPL_Csvs/2020-21_Season/testPredictions/MW" + str(week) + ".csv")
    week += 1
