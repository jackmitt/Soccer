import pandas as pd
import numpy as np

def kellyStake(p, decOdds, kellyDiv):
    return ((p - (1 - p)/(decOdds - 1)) / kellyDiv)

def analyzeWinRates(league, betType, timing):
    pred = pd.read_csv("./csv_data/" + league + "/bayes_predictions.csv", encoding = "ISO-8859-1")
    dict = {"<3%":[],"3-5%":[],"5-10%":[],"10-17.5%":[],"17.5-25%":[],"25-40%":[],"40%+":[]}
    for index, row in pred.iterrows():
        if (betType == "1X2"):
            if (row["p_1"] > 1 / row[timing + " 1"]):
                if ((row[timing + " 1"] - 1) * row["p_1"] - (1 - row["p_1"]) < 0.03):
                    if (row["Home Score"] > row["Away Score"]):
                        dict["<3%"].append(row[timing + " 1"] - 1)
                    else:
                        dict["<3%"].append(-1)
                elif ((row[timing + " 1"] - 1) * row["p_1"] - (1 - row["p_1"]) < 0.05):
                    if (row["Home Score"] > row["Away Score"]):
                        dict["3-5%"].append(row[timing + " 1"] - 1)
                    else:
                        dict["3-5%"].append(-1)
                elif ((row[timing + " 1"] - 1) * row["p_1"] - (1 - row["p_1"]) < 0.10):
                    if (row["Home Score"] > row["Away Score"]):
                        dict["5-10%"].append(row[timing + " 1"] - 1)
                    else:
                        dict["5-10%"].append(-1)
                elif ((row[timing + " 1"] - 1) * row["p_1"] - (1 - row["p_1"]) < 0.175):
                    if (row["Home Score"] > row["Away Score"]):
                        dict["10-17.5%"].append(row[timing + " 1"] - 1)
                    else:
                        dict["10-17.5%"].append(-1)
                elif ((row[timing + " 1"] - 1) * row["p_1"] - (1 - row["p_1"]) < 0.25):
                    if (row["Home Score"] > row["Away Score"]):
                        dict["17.5-25%"].append(row[timing + " 1"] - 1)
                    else:
                        dict["17.5-25%"].append(-1)
                elif ((row[timing + " 1"] - 1) * row["p_1"] - (1 - row["p_1"]) < 0.40):
                    if (row["Home Score"] > row["Away Score"]):
                        dict["25-40%"].append(row[timing + " 1"] - 1)
                    else:
                        dict["25-40%"].append(-1)
                else:
                    if (row["Home Score"] > row["Away Score"]):
                        dict["40%+"].append(row[timing + " 1"] - 1)
                    else:
                        dict["40%+"].append(-1)
            if (row["p_X"] > 1 / row[timing + " X"]):
                if ((row[timing + " X"] - 1) * row["p_X"] - (1 - row["p_X"]) < 0.03):
                    if (row["Home Score"] == row["Away Score"]):
                        dict["<3%"].append(row[timing + " X"] - 1)
                    else:
                        dict["<3%"].append(-1)
                elif ((row[timing + " X"] - 1) * row["p_X"] - (1 - row["p_X"]) < 0.05):
                    if (row["Home Score"] == row["Away Score"]):
                        dict["3-5%"].append(row[timing + " X"] - 1)
                    else:
                        dict["3-5%"].append(-1)
                elif ((row[timing + " X"] - 1) * row["p_X"] - (1 - row["p_X"]) < 0.10):
                    if (row["Home Score"] == row["Away Score"]):
                        dict["5-10%"].append(row[timing + " X"] - 1)
                    else:
                        dict["5-10%"].append(-1)
                elif ((row[timing + " X"] - 1) * row["p_X"] - (1 - row["p_X"]) < 0.175):
                    if (row["Home Score"] == row["Away Score"]):
                        dict["10-17.5%"].append(row[timing + " X"] - 1)
                    else:
                        dict["10-17.5%"].append(-1)
                elif ((row[timing + " X"] - 1) * row["p_X"] - (1 - row["p_X"]) < 0.25):
                    if (row["Home Score"] == row["Away Score"]):
                        dict["17.5-25%"].append(row[timing + " X"] - 1)
                    else:
                        dict["17.5-25%"].append(-1)
                elif ((row[timing + " X"] - 1) * row["p_X"] - (1 - row["p_X"]) < 0.40):
                    if (row["Home Score"] == row["Away Score"]):
                        dict["25-40%"].append(row[timing + " X"] - 1)
                    else:
                        dict["25-40%"].append(-1)
                else:
                    if (row["Home Score"] == row["Away Score"]):
                        dict["40%+"].append(row[timing + " X"] - 1)
                    else:
                        dict["40%+"].append(-1)
            if (row["p_2"] > 1 / row[timing + " 2"]):
                if ((row[timing + " 2"] - 1) * row["p_2"] - (1 - row["p_2"]) < 0.03):
                    if (row["Home Score"] < row["Away Score"]):
                        dict["<3%"].append(row[timing + " 2"] - 1)
                    else:
                        dict["<3%"].append(-1)
                elif ((row[timing + " 2"] - 1) * row["p_2"] - (1 - row["p_2"]) < 0.05):
                    if (row["Home Score"] < row["Away Score"]):
                        dict["3-5%"].append(row[timing + " 2"] - 1)
                    else:
                        dict["3-5%"].append(-1)
                elif ((row[timing + " 2"] - 1) * row["p_2"] - (1 - row["p_2"]) < 0.10):
                    if (row["Home Score"] < row["Away Score"]):
                        dict["5-10%"].append(row[timing + " 2"] - 1)
                    else:
                        dict["5-10%"].append(-1)
                elif ((row[timing + " 2"] - 1) * row["p_2"] - (1 - row["p_2"]) < 0.175):
                    if (row["Home Score"] < row["Away Score"]):
                        dict["10-17.5%"].append(row[timing + " 2"] - 1)
                    else:
                        dict["10-17.5%"].append(-1)
                elif ((row[timing + " 2"] - 1) * row["p_2"] - (1 - row["p_2"]) < 0.25):
                    if (row["Home Score"] < row["Away Score"]):
                        dict["17.5-25%"].append(row[timing + " 2"] - 1)
                    else:
                        dict["17.5-25%"].append(-1)
                elif ((row[timing + " 2"] - 1) * row["p_2"] - (1 - row["p_2"]) < 0.40):
                    if (row["Home Score"] < row["Away Score"]):
                        dict["25-40%"].append(row[timing + " 2"] - 1)
                    else:
                        dict["25-40%"].append(-1)
                else:
                    if (row["Home Score"] < row["Away Score"]):
                        dict["40%+"].append(row[timing + " 2"] - 1)
                    else:
                        dict["40%+"].append(-1)

        elif (betType == "AH"):
            if (row["p_" + timing + "_home_cover"] > 1 / row["Home " + timing + " AH Odds"]):
                if ((row["Home " + timing + " AH Odds"] - 1) * row["p_" + timing + "_home_cover"] - (1 - row["p_" + timing + "_home_cover"]) < 0.03):
                    if ("0.75" not in str(row[timing + " AH"]) and "0.25" not in str(row[timing + " AH"])):
                        if (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                            dict["<3%"].append(row["Home " + timing + " AH Odds"] - 1)
                        elif (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                            dict["<3%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                                ret += (row["Home " + timing + " AH Odds"] - 1) / 2
                            elif (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                                ret += -1/2
                        dict["<3%"].append(ret)
                elif ((row["Home " + timing + " AH Odds"] - 1) * row["p_" + timing + "_home_cover"] - (1 - row["p_" + timing + "_home_cover"]) < 0.05):
                    if ("0.75" not in str(row[timing + " AH"]) and "0.25" not in str(row[timing + " AH"])):
                        if (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                            dict["3-5%"].append(row["Home " + timing + " AH Odds"] - 1)
                        elif (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                            dict["3-5%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                                ret += (row["Home " + timing + " AH Odds"] - 1) / 2
                            elif (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                                ret += -1/2
                        dict["3-5%"].append(ret)
                elif ((row["Home " + timing + " AH Odds"] - 1) * row["p_" + timing + "_home_cover"] - (1 - row["p_" + timing + "_home_cover"]) < 0.10):
                    if ("0.75" not in str(row[timing + " AH"]) and "0.25" not in str(row[timing + " AH"])):
                        if (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                            dict["5-10%"].append(row["Home " + timing + " AH Odds"] - 1)
                        elif (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                            dict["5-10%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                                ret += (row["Home " + timing + " AH Odds"] - 1) / 2
                            elif (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                                ret += -1/2
                        dict["5-10%"].append(ret)
                elif ((row["Home " + timing + " AH Odds"] - 1) * row["p_" + timing + "_home_cover"] - (1 - row["p_" + timing + "_home_cover"]) < 0.175):
                    if ("0.75" not in str(row[timing + " AH"]) and "0.25" not in str(row[timing + " AH"])):
                        if (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                            dict["10-17.5%"].append(row["Home " + timing + " AH Odds"] - 1)
                        elif (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                            dict["10-17.5%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                                ret += (row["Home " + timing + " AH Odds"] - 1) / 2
                            elif (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                                ret += -1/2
                        dict["10-17.5%"].append(ret)
                elif ((row["Home " + timing + " AH Odds"] - 1) * row["p_" + timing + "_home_cover"] - (1 - row["p_" + timing + "_home_cover"]) < 0.25):
                    if ("0.75" not in str(row[timing + " AH"]) and "0.25" not in str(row[timing + " AH"])):
                        if (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                            dict["17.5-25%"].append(row["Home " + timing + " AH Odds"] - 1)
                        elif (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                            dict["17.5-25%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                                ret += (row["Home " + timing + " AH Odds"] - 1) / 2
                            elif (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                                ret += -1/2
                        dict["17.5-25%"].append(ret)
                elif ((row["Home " + timing + " AH Odds"] - 1) * row["p_" + timing + "_home_cover"] - (1 - row["p_" + timing + "_home_cover"]) < 0.40):
                    if ("0.75" not in str(row[timing + " AH"]) and "0.25" not in str(row[timing + " AH"])):
                        if (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                            dict["25-40%"].append(row["Home " + timing + " AH Odds"] - 1)
                        elif (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                            dict["25-40%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                                ret += (row["Home " + timing + " AH Odds"] - 1) / 2
                            elif (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                                ret += -1/2
                        dict["25-40%"].append(ret)
                else:
                    if ("0.75" not in str(row[timing + " AH"]) and "0.25" not in str(row[timing + " AH"])):
                        if (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                            dict["40%+"].append(row["Home " + timing + " AH Odds"] - 1)
                        elif (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                            dict["40%+"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                                ret += (row["Home " + timing + " AH Odds"] - 1) / 2
                            elif (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                                ret += -1/2
                        dict["40%+"].append(ret)
            elif ((1 - row["p_" + timing + "_home_cover"]) > 1 / row["Away " + timing + " AH Odds"]):
                if ((row["Away " + timing + " AH Odds"] - 1) * (1 - row["p_" + timing + "_home_cover"]) - (1 - (1 - row["p_" + timing + "_home_cover"])) < 0.03):
                    if ("0.75" not in str(row[timing + " AH"]) and "0.25" not in str(row[timing + " AH"])):
                        if (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                            dict["<3%"].append(row["Away " + timing + " AH Odds"] - 1)
                        elif (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                            dict["<3%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                                ret += (row["Away " + timing + " AH Odds"] - 1) / 2
                            elif (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                                ret += -1/2
                        dict["<3%"].append(ret)
                elif ((row["Away " + timing + " AH Odds"] - 1) * (1 - row["p_" + timing + "_home_cover"]) - (1 - (1 - row["p_" + timing + "_home_cover"])) < 0.05):
                    if ("0.75" not in str(row[timing + " AH"]) and "0.25" not in str(row[timing + " AH"])):
                        if (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                            dict["3-5%"].append(row["Away " + timing + " AH Odds"] - 1)
                        elif (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                            dict["3-5%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                                ret += (row["Away " + timing + " AH Odds"] - 1) / 2
                            elif (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                                ret += -1/2
                        dict["3-5%"].append(ret)
                elif ((row["Away " + timing + " AH Odds"] - 1) * (1 - row["p_" + timing + "_home_cover"]) - (1 - (1 - row["p_" + timing + "_home_cover"])) < 0.10):
                    if ("0.75" not in str(row[timing + " AH"]) and "0.25" not in str(row[timing + " AH"])):
                        if (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                            dict["5-10%"].append(row["Away " + timing + " AH Odds"] - 1)
                        elif (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                            dict["5-10%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                                ret += (row["Away " + timing + " AH Odds"] - 1) / 2
                            elif (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                                ret += -1/2
                        dict["5-10%"].append(ret)
                elif ((row["Away " + timing + " AH Odds"] - 1) * (1 - row["p_" + timing + "_home_cover"]) - (1 - (1 - row["p_" + timing + "_home_cover"])) < 0.175):
                    if ("0.75" not in str(row[timing + " AH"]) and "0.25" not in str(row[timing + " AH"])):
                        if (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                            dict["10-17.5%"].append(row["Away " + timing + " AH Odds"] - 1)
                        elif (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                            dict["10-17.5%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                                ret += (row["Away " + timing + " AH Odds"] - 1) / 2
                            elif (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                                ret += -1/2
                        dict["10-17.5%"].append(ret)
                elif ((row["Away " + timing + " AH Odds"] - 1) * (1 - row["p_" + timing + "_home_cover"]) - (1 - (1 - row["p_" + timing + "_home_cover"])) < 0.25):
                    if ("0.75" not in str(row[timing + " AH"]) and "0.25" not in str(row[timing + " AH"])):
                        if (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                            dict["17.5-25%"].append(row["Away " + timing + " AH Odds"] - 1)
                        elif (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                            dict["17.5-25%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                                ret += (row["Away " + timing + " AH Odds"] - 1) / 2
                            elif (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                                ret += -1/2
                        dict["17.5-25%"].append(ret)
                elif ((row["Away " + timing + " AH Odds"] - 1) * (1 - row["p_" + timing + "_home_cover"]) - (1 - (1 - row["p_" + timing + "_home_cover"])) < 0.40):
                    if ("0.75" not in str(row[timing + " AH"]) and "0.25" not in str(row[timing + " AH"])):
                        if (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                            dict["25-40%"].append(row["Away " + timing + " AH Odds"] - 1)
                        elif (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                            dict["25-40%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                                ret += (row["Away " + timing + " AH Odds"] - 1) / 2
                            elif (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                                ret += -1/2
                        dict["25-40%"].append(ret)
                else:
                    if ("0.75" not in str(row[timing + " AH"]) and "0.25" not in str(row[timing + " AH"])):
                        if (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                            dict["40%+"].append(row["Away " + timing + " AH Odds"] - 1)
                        elif (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                            dict["40%+"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] < row["Away Score"] + row[timing + " AH"]):
                                ret += (row["Away " + timing + " AH Odds"] - 1) / 2
                            elif (row["Home Score"] > row["Away Score"] + row[timing + " AH"]):
                                ret += -1/2
                        dict["40%+"].append(ret)
        elif (betType == "OU"):
            if (row["p_" + timing + "_over"] > 1 / row["Over " + timing + " OU Odds"]):
                if ((row["Over " + timing + " OU Odds"] - 1) * row["p_" + timing + "_over"] - (1 - row["p_" + timing + "_over"]) < 0.03):
                    if ("0.75" not in str(row[timing + " OU"]) and "0.25" not in str(row[timing + " OU"])):
                        if (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                            dict["<3%"].append(row["Over " + timing + " OU Odds"] - 1)
                        elif (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                            dict["<3%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                                ret += (row["Over " + timing + " OU Odds"] - 1) / 2
                            elif (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                                ret += -1/2
                        dict["<3%"].append(ret)
                elif ((row["Over " + timing + " OU Odds"] - 1) * row["p_" + timing + "_over"] - (1 - row["p_" + timing + "_over"]) < 0.05):
                    if ("0.75" not in str(row[timing + " OU"]) and "0.25" not in str(row[timing + " OU"])):
                        if (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                            dict["3-5%"].append(row["Over " + timing + " OU Odds"] - 1)
                        elif (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                            dict["3-5%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                                ret += (row["Over " + timing + " OU Odds"] - 1) / 2
                            elif (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                                ret += -1/2
                        dict["3-5%"].append(ret)
                elif ((row["Over " + timing + " OU Odds"] - 1) * row["p_" + timing + "_over"] - (1 - row["p_" + timing + "_over"]) < 0.10):
                    if ("0.75" not in str(row[timing + " OU"]) and "0.25" not in str(row[timing + " OU"])):
                        if (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                            dict["5-10%"].append(row["Over " + timing + " OU Odds"] - 1)
                        elif (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                            dict["5-10%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                                ret += (row["Over " + timing + " OU Odds"] - 1) / 2
                            elif (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                                ret += -1/2
                        dict["5-10%"].append(ret)
                elif ((row["Over " + timing + " OU Odds"] - 1) * row["p_" + timing + "_over"] - (1 - row["p_" + timing + "_over"]) < 0.175):
                    if ("0.75" not in str(row[timing + " OU"]) and "0.25" not in str(row[timing + " OU"])):
                        if (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                            dict["10-17.5%"].append(row["Over " + timing + " OU Odds"] - 1)
                        elif (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                            dict["10-17.5%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                                ret += (row["Over " + timing + " OU Odds"] - 1) / 2
                            elif (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                                ret += -1/2
                        dict["10-17.5%"].append(ret)
                elif ((row["Over " + timing + " OU Odds"] - 1) * row["p_" + timing + "_over"] - (1 - row["p_" + timing + "_over"]) < 0.25):
                    if ("0.75" not in str(row[timing + " OU"]) and "0.25" not in str(row[timing + " OU"])):
                        if (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                            dict["17.5-25%"].append(row["Over " + timing + " OU Odds"] - 1)
                        elif (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                            dict["17.5-25%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                                ret += (row["Over " + timing + " OU Odds"] - 1) / 2
                            elif (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                                ret += -1/2
                        dict["17.5-25%"].append(ret)
                elif ((row["Over " + timing + " OU Odds"] - 1) * row["p_" + timing + "_over"] - (1 - row["p_" + timing + "_over"]) < 0.40):
                    if ("0.75" not in str(row[timing + " OU"]) and "0.25" not in str(row[timing + " OU"])):
                        if (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                            dict["25-40%"].append(row["Over " + timing + " OU Odds"] - 1)
                        elif (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                            dict["25-40%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                                ret += (row["Over " + timing + " OU Odds"] - 1) / 2
                            elif (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                                ret += -1/2
                        dict["25-40%"].append(ret)
                else:
                    if ("0.75" not in str(row[timing + " OU"]) and "0.25" not in str(row[timing + " OU"])):
                        if (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                            dict["40%+"].append(row["Over " + timing + " OU Odds"] - 1)
                        elif (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                            dict["40%+"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                                ret += (row["Over " + timing + " OU Odds"] - 1) / 2
                            elif (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                                ret += -1/2
                        dict["40%+"].append(ret)
            elif ((1 - row["p_" + timing + "_over"]) > 1 / row["Under " + timing + " OU Odds"]):
                if ((row["Under " + timing + " OU Odds"] - 1) * (1 - row["p_" + timing + "_over"]) - (1 - (1 - row["p_" + timing + "_over"])) < 0.03):
                    if ("0.75" not in str(row[timing + " OU"]) and "0.25" not in str(row[timing + " OU"])):
                        if (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                            dict["<3%"].append(row["Under " + timing + " OU Odds"] - 1)
                        elif (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                            dict["<3%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                                ret += (row["Under " + timing + " OU Odds"] - 1) / 2
                            elif (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                                ret += -1/2
                        dict["<3%"].append(ret)
                elif ((row["Under " + timing + " OU Odds"] - 1) * (1 - row["p_" + timing + "_over"]) - (1 - (1 - row["p_" + timing + "_over"])) < 0.05):
                    if ("0.75" not in str(row[timing + " OU"]) and "0.25" not in str(row[timing + " OU"])):
                        if (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                            dict["3-5%"].append(row["Under " + timing + " OU Odds"] - 1)
                        elif (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                            dict["3-5%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                                ret += (row["Under " + timing + " OU Odds"] - 1) / 2
                            elif (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                                ret += -1/2
                        dict["3-5%"].append(ret)
                elif ((row["Under " + timing + " OU Odds"] - 1) * (1 - row["p_" + timing + "_over"]) - (1 - (1 - row["p_" + timing + "_over"])) < 0.10):
                    if ("0.75" not in str(row[timing + " OU"]) and "0.25" not in str(row[timing + " OU"])):
                        if (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                            dict["5-10%"].append(row["Under " + timing + " OU Odds"] - 1)
                        elif (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                            dict["5-10%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                                ret += (row["Under " + timing + " OU Odds"] - 1) / 2
                            elif (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                                ret += -1/2
                        dict["5-10%"].append(ret)
                elif ((row["Under " + timing + " OU Odds"] - 1) * (1 - row["p_" + timing + "_over"]) - (1 - (1 - row["p_" + timing + "_over"])) < 0.175):
                    if ("0.75" not in str(row[timing + " OU"]) and "0.25" not in str(row[timing + " OU"])):
                        if (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                            dict["10-17.5%"].append(row["Under " + timing + " OU Odds"] - 1)
                        elif (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                            dict["10-17.5%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                                ret += (row["Under " + timing + " OU Odds"] - 1) / 2
                            elif (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                                ret += -1/2
                        dict["10-17.5%"].append(ret)
                elif ((row["Under " + timing + " OU Odds"] - 1) * (1 - row["p_" + timing + "_over"]) - (1 - (1 - row["p_" + timing + "_over"])) < 0.25):
                    if ("0.75" not in str(row[timing + " OU"]) and "0.25" not in str(row[timing + " OU"])):
                        if (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                            dict["17.5-25%"].append(row["Under " + timing + " OU Odds"] - 1)
                        elif (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                            dict["17.5-25%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                                ret += (row["Under " + timing + " OU Odds"] - 1) / 2
                            elif (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                                ret += -1/2
                        dict["17.5-25%"].append(ret)
                elif ((row["Under " + timing + " OU Odds"] - 1) * (1 - row["p_" + timing + "_over"]) - (1 - (1 - row["p_" + timing + "_over"])) < 0.40):
                    if ("0.75" not in str(row[timing + " OU"]) and "0.25" not in str(row[timing + " OU"])):
                        if (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                            dict["25-40%"].append(row["Under " + timing + " OU Odds"] - 1)
                        elif (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                            dict["25-40%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                                ret += (row["Under " + timing + " OU Odds"] - 1) / 2
                            elif (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                                ret += -1/2
                        dict["25-40%"].append(ret)
                else:
                    if ("0.75" not in str(row[timing + " OU"]) and "0.25" not in str(row[timing + " OU"])):
                        if (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                            dict["40%+"].append(row["Under " + timing + " OU Odds"] - 1)
                        elif (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                            dict["40%+"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["Home Score"] + row["Away Score"] < row[timing + " OU"]):
                                ret += (row["Under " + timing + " OU Odds"] - 1) / 2
                            elif (row["Home Score"] + row["Away Score"] > row[timing + " OU"]):
                                ret += -1/2
                        dict["40%+"].append(ret)

    for key in dict:
        print (key + ":", np.average(dict[key]), len(dict[key]))
