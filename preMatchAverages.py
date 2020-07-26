import pandas as pd
import numpy as np
import datetime
import gc

def last5scale(a, b):
    totalT = 1.5**0 + 1.5**1 + 1.5**2 + 1.5**3 + 1.5**4
    c = 0
    d = 0
    for i in range(5):
        c += a[i]*(1.5**(4-i))
        d += b[i]*(1.5**(4-i))
    return ((c+d)/(2*totalT))

data = pd.read_csv('./allRawData.csv', encoding = "ISO-8859-1")
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
    dict["E_" + side + "ball_winning"] = []
    dict["E_" + side + "chance_efficiency"] = []
    dict["E_" + side + "shooting_efficiency"] = []
    dict["E_" + side + "key_pass_pct"] = []
    dict["E_" + side + "pass_success"] = []
    dict["E_" + side + "dribble_success"] = []
    dict["E_" + side + "tackle_success"] = []
    dict["E_" + side + "xG"] = []
    dict["E_" + side + "xPts"] = []

beenSeptember = True
for index, row in data.iterrows():
    # for col in data.columns:
    #     print (col, row[col])
    print (index)
    gc.collect()
    if (int(row["Date"].split("/")[0]) == 9):
        beenSeptember = True
    #initialization
    if (int(row["Date"].split("/")[0]) == 8 and beenSeptember):
        seasonDict = {}
        curIndex = index
        while (curIndex < len(data.index) and (int(data.iat[curIndex, 0].split("/")[0]) != 8 or int(data.iat[curIndex, 0].split("/")[2]) != int(row["Date"].split("/")[2]) + 1)):
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
                    seasonDict[data.iat[curIndex, 1]]["E_" + side + "ball_winning"] = []
                    seasonDict[data.iat[curIndex, 1]]["E_" + side + "chance_efficiency"] = []
                    seasonDict[data.iat[curIndex, 1]]["E_" + side + "shooting_efficiency"] = []
                    seasonDict[data.iat[curIndex, 1]]["E_" + side + "key_pass_pct"] = []
                    seasonDict[data.iat[curIndex, 1]]["E_" + side + "pass_success"] = []
                    seasonDict[data.iat[curIndex, 1]]["E_" + side + "dribble_success"] = []
                    seasonDict[data.iat[curIndex, 1]]["E_" + side + "tackle_success"] = []
                    seasonDict[data.iat[curIndex, 1]]["E_" + side + "xG"] = []
                    seasonDict[data.iat[curIndex, 1]]["E_" + side + "xPts"] = []
            curIndex += 1
        beenSeptember = False
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
            dict["E_" + side + "ball_winning"].append(np.nan)
            dict["E_" + side + "chance_efficiency"].append(np.nan)
            dict["E_" + side + "shooting_efficiency"].append(np.nan)
            dict["E_" + side + "key_pass_pct"].append(np.nan)
            dict["E_" + side + "pass_success"].append(np.nan)
            dict["E_" + side + "dribble_success"].append(np.nan)
            dict["E_" + side + "tackle_success"].append(np.nan)
            dict["E_" + side + "xG"].append(np.nan)
            dict["E_" + side + "xPts"].append(np.nan)
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
                else:
                    if (len(seasonDict[row["Home"]]["" + "ball_winning"]) < 5 or len(seasonDict[row["Away"]]["" + "ball_winning"]) < 5):
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
                    elif (side == "home_expected_"):
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "ball_winning"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "ball_winning"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "ball_winning"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "chance_efficiency"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "chance_efficiency"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "chance_efficiency"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "shooting_efficiency"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "shooting_efficiency"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "shooting_efficiency"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "key_pass_pct"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "key_pass_pct"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "key_pass_pct"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "pass_success"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "pass_success"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "pass_success"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "dribble_success"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "dribble_success"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "dribble_success"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "tackle_success"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "tackle_success"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "tackle_success"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "xG"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "xG"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "xG"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "xPts"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "xPts"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "xPts"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "deep_pct"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "deep_pct"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "deep_pct"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "pass_to_touch_ratio"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "pass_to_touch_ratio"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "pass_to_touch_ratio"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "foul_rate"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "foul_rate"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "foul_rate"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "clear_rate"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "clear_rate"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "clear_rate"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "long_pass_pct"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "long_pass_pct"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "long_pass_pct"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "fwd_pass_pct"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "fwd_pass_pct"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "fwd_pass_pct"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "fwd_pass_aggressiveness"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "fwd_pass_aggressiveness"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "fwd_pass_aggressiveness"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "defensive_third_pct"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "defensive_third_pct"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "defensive_third_pct"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "final_third_pct"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "final_third_pct"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "final_third_pct"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Home"]]["" + "ppda"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Away"]]["X_" + "ppda"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "ppda"].append(last5scale(tempH, tempA))
                    else:
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "ball_winning"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "ball_winning"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "ball_winning"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "chance_efficiency"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "chance_efficiency"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "chance_efficiency"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "shooting_efficiency"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "shooting_efficiency"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "shooting_efficiency"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "key_pass_pct"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "key_pass_pct"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "key_pass_pct"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "pass_success"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "pass_success"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "pass_success"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "dribble_success"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "dribble_success"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "dribble_success"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "tackle_success"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "tackle_success"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "tackle_success"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "xG"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "xG"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "xG"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "xPts"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "xPts"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "xPts"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "deep_pct"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "deep_pct"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "deep_pct"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "pass_to_touch_ratio"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "pass_to_touch_ratio"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "pass_to_touch_ratio"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "foul_rate"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "foul_rate"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "foul_rate"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "clear_rate"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "clear_rate"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "clear_rate"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "long_pass_pct"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "long_pass_pct"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "long_pass_pct"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "fwd_pass_pct"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "fwd_pass_pct"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "fwd_pass_pct"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "fwd_pass_aggressiveness"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "fwd_pass_aggressiveness"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "fwd_pass_aggressiveness"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "defensive_third_pct"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "defensive_third_pct"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "defensive_third_pct"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "final_third_pct"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "final_third_pct"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "final_third_pct"].append(last5scale(tempH, tempA))
                        tempH = []
                        tempA = []
                        for stat in reversed(seasonDict[row["Away"]]["" + "ppda"]):
                            if (len(tempH) < 5):
                                tempH.append(stat)
                        for stat in reversed(seasonDict[row["Home"]]["X_" + "ppda"]):
                            if (len(tempA) < 5):
                                tempA.append(stat)
                        dict[tCat + side + "ppda"].append(last5scale(tempH, tempA))
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
            seasonDict[row["Home"]]["E_" + side + "ball_winning"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Interceptions"]) / float(row["Away Total Passes"]))
            seasonDict[row["Home"]]["E_" + side + "chance_efficiency"].append((float(row["Away Pre Elo"])/1500) * float(row["Home xG"]) * 100 / float(row["Home Possession"]))
            seasonDict[row["Home"]]["E_" + side + "shooting_efficiency"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Score"]) - float(row["Home xG"]))
            seasonDict[row["Home"]]["E_" + side + "key_pass_pct"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Key Passes"]) / float(row["Home passzone_final_third"]))
            seasonDict[row["Home"]]["E_" + side + "pass_success"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Accurate Passes"]) / float(row["Home Total Passes"]))
            seasonDict[row["Home"]]["E_" + side + "dribble_success"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Dribbles Won"]) / float(row["Home Dribbles Attempted"]))
            seasonDict[row["Home"]]["E_" + side + "tackle_success"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Successful Tackles"]) / float(row["Home Tackles Attempted"]))
            seasonDict[row["Home"]]["E_" + side + "xG"].append((float(row["Away Pre Elo"])/1500) * row["Home xG"])
            seasonDict[row["Home"]]["E_" + side + "xPts"].append((float(row["Away Pre Elo"])/1500) * row["Home xPts"])
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
            seasonDict[row["Away"]]["E_" + side + "ball_winning"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Interceptions"]) / float(row["Home Total Passes"]))
            seasonDict[row["Away"]]["E_" + side + "chance_efficiency"].append((float(row["Home Pre Elo"])/1500) * float(row["Away xG"]) * 100 / float(row["Away Possession"]))
            seasonDict[row["Away"]]["E_" + side + "shooting_efficiency"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Score"]) - float(row["Away xG"]))
            seasonDict[row["Away"]]["E_" + side + "key_pass_pct"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Key Passes"]) / float(row["Away passzone_final_third"]))
            seasonDict[row["Away"]]["E_" + side + "pass_success"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Accurate Passes"]) / float(row["Away Total Passes"]))
            seasonDict[row["Away"]]["E_" + side + "dribble_success"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Dribbles Won"]) / float(row["Away Dribbles Attempted"]))
            seasonDict[row["Away"]]["E_" + side + "tackle_success"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Successful Tackles"]) / float(row["Away Tackles Attempted"]))
            seasonDict[row["Away"]]["E_" + side + "xG"].append((float(row["Home Pre Elo"])/1500) * row["Away xG"])
            seasonDict[row["Away"]]["E_" + side + "xPts"].append((float(row["Home Pre Elo"])/1500) * row["Away xPts"])
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
            seasonDict[row["Away"]]["E_" + side + "ball_winning"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Interceptions"]) / float(row["Away Total Passes"]))
            seasonDict[row["Away"]]["E_" + side + "chance_efficiency"].append((float(row["Away Pre Elo"])/1500) * float(row["Home xG"]) * 100 / float(row["Home Possession"]))
            seasonDict[row["Away"]]["E_" + side + "shooting_efficiency"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Score"]) - float(row["Home xG"]))
            seasonDict[row["Away"]]["E_" + side + "key_pass_pct"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Key Passes"]) / float(row["Home passzone_final_third"]))
            seasonDict[row["Away"]]["E_" + side + "pass_success"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Accurate Passes"]) / float(row["Home Total Passes"]))
            seasonDict[row["Away"]]["E_" + side + "dribble_success"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Dribbles Won"]) / float(row["Home Dribbles Attempted"]))
            seasonDict[row["Away"]]["E_" + side + "tackle_success"].append((float(row["Away Pre Elo"])/1500) * float(row["Home Successful Tackles"]) / float(row["Home Tackles Attempted"]))
            seasonDict[row["Away"]]["E_" + side + "xG"].append((float(row["Away Pre Elo"])/1500) * row["Home xG"])
            seasonDict[row["Away"]]["E_" + side + "xPts"].append((float(row["Away Pre Elo"])/1500) * row["Home xPts"])
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
            seasonDict[row["Home"]]["E_" + side + "ball_winning"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Interceptions"]) / float(row["Home Total Passes"]))
            seasonDict[row["Home"]]["E_" + side + "chance_efficiency"].append((float(row["Home Pre Elo"])/1500) * float(row["Away xG"]) * 100 / float(row["Away Possession"]))
            seasonDict[row["Home"]]["E_" + side + "shooting_efficiency"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Score"]) - float(row["Away xG"]))
            seasonDict[row["Home"]]["E_" + side + "key_pass_pct"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Key Passes"]) / float(row["Away passzone_final_third"]))
            seasonDict[row["Home"]]["E_" + side + "pass_success"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Accurate Passes"]) / float(row["Away Total Passes"]))
            seasonDict[row["Home"]]["E_" + side + "dribble_success"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Dribbles Won"]) / float(row["Away Dribbles Attempted"]))
            seasonDict[row["Home"]]["E_" + side + "tackle_success"].append((float(row["Home Pre Elo"])/1500) * float(row["Away Successful Tackles"]) / float(row["Away Tackles Attempted"]))
            seasonDict[row["Home"]]["E_" + side + "xG"].append((float(row["Home Pre Elo"])/1500) * row["Away xG"])
            seasonDict[row["Home"]]["E_" + side + "xPts"].append((float(row["Home Pre Elo"])/1500) * row["Away xPts"])
    #print (seasonDict)
for key in dict:
    data[key] = dict[key]
data.to_csv("bigboy.csv")
