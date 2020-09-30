import pandas as pd
import numpy as np
import datetime
import gc

def last5scale(a, b):
    if (len(a)<=5 or len(b)<=5):
        return (0)
    scaleBy = 1.05
    totalT = scaleBy**0 + scaleBy**1 + scaleBy**2 + scaleBy**3 + scaleBy**4
    c = 0
    d = 0
    for i in range(5):
        c += a[i]*(scaleBy**(4-i))
        d += b[i]*(scaleBy**(4-i))
    #c = 0.15*a[4] + 0.175*a[3] + 0.2*a[2] + 0.225*a[1] + 0.25*a[0]
    #d = 0.15*b[4] + 0.175*b[3] + 0.2*b[2] + 0.225*b[1] + 0.25*b[0]
    if (len(a) < 10 or len(b) < 10):
        return ((c+d)/(2*totalT))
        #return ((c+d)/2)
    e = []
    f = []
    for i in reversed(range(len(a))):
        if (i == 4):
            break
        e.append(a[i])
    for i in reversed(range(len(b))):
        if (i == 4):
            break
        f.append(b[i])
    return ((((np.average(e) + np.average(f)) / 2)*.5 + ((c+d)/(2*totalT)))*.5)
    #return ((((np.average(e) + np.average(f)) / 2)*.5 + ((c+d)/(2)))*.5)

data = pd.read_csv('./EPL_Csvs/allRawData.csv', encoding = "ISO-8859-1")
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
    print (index)
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
                    #
                    #
                    #
                    #
                    #
                    # CHANGED FOR EXPERIMENT - NORMALLY IS 3
                    if (len(seasonDict[row["Home"]]["" + "ball_winning"]) < 3 or len(seasonDict[row["Away"]]["" + "ball_winning"]) < 3):
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
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "ball_winning"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "ball_winning"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "chance_efficiency"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "chance_efficiency"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "chance_efficiency"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "shooting_efficiency"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "shooting_efficiency"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "shooting_efficiency"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "key_pass_pct"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "key_pass_pct"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "key_pass_pct"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "pass_success"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "pass_success"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "pass_success"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "dribble_success"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "dribble_success"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "dribble_success"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "tackle_success"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "tackle_success"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "tackle_success"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "xG"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "xG"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "xG"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "xPts"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "xPts"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "xPts"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "deep_pct"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "deep_pct"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "deep_pct"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "pass_to_touch_ratio"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "pass_to_touch_ratio"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "pass_to_touch_ratio"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "foul_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "foul_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "foul_rate"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "clear_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "clear_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "clear_rate"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "long_pass_pct"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "long_pass_pct"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "long_pass_pct"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "fwd_pass_pct"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "fwd_pass_pct"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "fwd_pass_pct"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "fwd_pass_aggressiveness"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "fwd_pass_aggressiveness"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "fwd_pass_aggressiveness"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "defensive_third_pct"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "defensive_third_pct"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "defensive_third_pct"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "final_third_pct"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "final_third_pct"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "final_third_pct"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "ppda"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "ppda"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "ppda"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "touch_aggression"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "touch_aggression"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "touch_aggression"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "pass_aggression"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "pass_aggression"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "pass_aggression"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "dribble_aggression"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "dribble_aggression"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "dribble_aggression"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "tackle_aggression"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "tackle_aggression"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "tackle_aggression"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "corner_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "corner_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "corner_rate"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "dispossession_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "dispossession_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "dispossession_rate"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "offsides_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "offsides_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "offsides_rate"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "cross_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "cross_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "cross_rate"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "through_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "through_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "through_rate"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "xG_aggression_adjustment"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "xG_aggression_adjustment"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "xG_aggression_adjustment"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "xG_efficiency"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "xG_efficiency"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "xG_efficiency"].append(last5scale(tempH, tempA))
                    else:
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "ball_winning"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "ball_winning"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "ball_winning"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "chance_efficiency"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "chance_efficiency"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "chance_efficiency"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "shooting_efficiency"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "shooting_efficiency"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "shooting_efficiency"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "key_pass_pct"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "key_pass_pct"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "key_pass_pct"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "pass_success"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "pass_success"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "pass_success"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "dribble_success"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "dribble_success"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "dribble_success"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "tackle_success"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "tackle_success"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "tackle_success"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "xG"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "xG"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "xG"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "xPts"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "xPts"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "xPts"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "deep_pct"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "deep_pct"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "deep_pct"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "pass_to_touch_ratio"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "pass_to_touch_ratio"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "pass_to_touch_ratio"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "foul_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "foul_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "foul_rate"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "clear_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "clear_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "clear_rate"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "long_pass_pct"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "long_pass_pct"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "long_pass_pct"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "fwd_pass_pct"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "fwd_pass_pct"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "fwd_pass_pct"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "fwd_pass_aggressiveness"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "fwd_pass_aggressiveness"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "fwd_pass_aggressiveness"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "defensive_third_pct"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "defensive_third_pct"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "defensive_third_pct"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "final_third_pct"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "final_third_pct"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "final_third_pct"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "ppda"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "ppda"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "ppda"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "touch_aggression"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "touch_aggression"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "touch_aggression"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "pass_aggression"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "pass_aggression"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "pass_aggression"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "dribble_aggression"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "dribble_aggression"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "dribble_aggression"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "tackle_aggression"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "tackle_aggression"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "tackle_aggression"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "corner_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "corner_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "corner_rate"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "dispossession_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "dispossession_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "dispossession_rate"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "offsides_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "offsides_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "offsides_rate"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "cross_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "cross_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "cross_rate"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "through_rate"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "through_rate"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "through_rate"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "xG_aggression_adjustment"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "xG_aggression_adjustment"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "xG_aggression_adjustment"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "xG_efficiency"]):
                            if (len(tempH) < 9999):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "xG_efficiency"]):
                            if (len(tempA) < 9999):
                                tempA.append(stat)
                        dict[tCat + side + "xG_efficiency"].append(last5scale(tempH, tempA))
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
data.to_csv("./EPL_Csvs/bigboy4Games.csv")
