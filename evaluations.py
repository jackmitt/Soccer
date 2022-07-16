import pandas as pd
import numpy as np
import datetime

def kellyStake(p, decOdds, kellyDiv):
    if ((p - (1 - p)/(decOdds - 1)) / kellyDiv > 0.05):
        return 0.05
    return ((p - (1 - p)/(decOdds - 1)) / kellyDiv)

def analyzeWinRates(league, betType, timing, pType = ""):
    pred = pd.read_csv("./csv_data/" + league + "/bayes_predictions.csv", encoding = "ISO-8859-1")
    for i in range(len(pred.index)):
        pred.at[i, "Date"] = datetime.date(int(pred.at[i, "Date"].split("-")[0]), int(pred.at[i, "Date"].split("-")[1]), int(pred.at[i, "Date"].split("-")[2]))
    seasons = {}
    for index, row in pred.iterrows():
        if (index == 0 or abs(row["Date"] - pred.at[index - 1,"Date"]).days > 30):
            if (str(row["Date"].year) not in seasons):
                seasons[str(row["Date"].year)] = {"<3%":[],"3-5%":[],"5-10%":[],"10-17.5%":[],"17.5-25%":[],"25-40%":[],"40%+":[]}
                curSeason = str(row["Date"].year)
            else:
                seasons[str(row["Date"].year) + "_2"] = {"<3%":[],"3-5%":[],"5-10%":[],"10-17.5%":[],"17.5-25%":[],"25-40%":[],"40%+":[]}
                curSeason = str(row["Date"].year) + "_2"
        if (row["Date"].year < 2017):
            continue
        if (betType == "1X2"):
            if (row[pType + "p_1"] > 1 / row[timing + " 1"]):
                if ((row[timing + " 1"] - 1) * row[pType + "p_1"] - (1 - row[pType + "p_1"]) < 0.03):
                    if (row["home_team_reg_score"] > row["away_team_reg_score"]):
                        seasons[curSeason]["<3%"].append(row[timing + " 1"] - 1)
                    else:
                        seasons[curSeason]["<3%"].append(-1)
                elif ((row[timing + " 1"] - 1) * row[pType + "p_1"] - (1 - row[pType + "p_1"]) < 0.05):
                    if (row["home_team_reg_score"] > row["away_team_reg_score"]):
                        seasons[curSeason]["3-5%"].append(row[timing + " 1"] - 1)
                    else:
                        seasons[curSeason]["3-5%"].append(-1)
                elif ((row[timing + " 1"] - 1) * row[pType + "p_1"] - (1 - row[pType + "p_1"]) < 0.10):
                    if (row["home_team_reg_score"] > row["away_team_reg_score"]):
                        seasons[curSeason]["5-10%"].append(row[timing + " 1"] - 1)
                    else:
                        seasons[curSeason]["5-10%"].append(-1)
                elif ((row[timing + " 1"] - 1) * row[pType + "p_1"] - (1 - row[pType + "p_1"]) < 0.175):
                    if (row["home_team_reg_score"] > row["away_team_reg_score"]):
                        seasons[curSeason]["10-17.5%"].append(row[timing + " 1"] - 1)
                    else:
                        seasons[curSeason]["10-17.5%"].append(-1)
                elif ((row[timing + " 1"] - 1) * row[pType + "p_1"] - (1 - row[pType + "p_1"]) < 0.25):
                    if (row["home_team_reg_score"] > row["away_team_reg_score"]):
                        seasons[curSeason]["17.5-25%"].append(row[timing + " 1"] - 1)
                    else:
                        seasons[curSeason]["17.5-25%"].append(-1)
                elif ((row[timing + " 1"] - 1) * row[pType + "p_1"] - (1 - row[pType + "p_1"]) < 0.40):
                    if (row["home_team_reg_score"] > row["away_team_reg_score"]):
                        seasons[curSeason]["25-40%"].append(row[timing + " 1"] - 1)
                    else:
                        seasons[curSeason]["25-40%"].append(-1)
                else:
                    if (row["home_team_reg_score"] > row["away_team_reg_score"]):
                        seasons[curSeason]["40%+"].append(row[timing + " 1"] - 1)
                    else:
                        seasons[curSeason]["40%+"].append(-1)
            if (row[pType + "p_X"] > 1 / row[timing + " X"]):
                if ((row[timing + " X"] - 1) * row[pType + "p_X"] - (1 - row[pType + "p_X"]) < 0.03):
                    if (row["home_team_reg_score"] == row["away_team_reg_score"]):
                        seasons[curSeason]["<3%"].append(row[timing + " X"] - 1)
                    else:
                        seasons[curSeason]["<3%"].append(-1)
                elif ((row[timing + " X"] - 1) * row[pType + "p_X"] - (1 - row[pType + "p_X"]) < 0.05):
                    if (row["home_team_reg_score"] == row["away_team_reg_score"]):
                        seasons[curSeason]["3-5%"].append(row[timing + " X"] - 1)
                    else:
                        seasons[curSeason]["3-5%"].append(-1)
                elif ((row[timing + " X"] - 1) * row[pType + "p_X"] - (1 - row[pType + "p_X"]) < 0.10):
                    if (row["home_team_reg_score"] == row["away_team_reg_score"]):
                        seasons[curSeason]["5-10%"].append(row[timing + " X"] - 1)
                    else:
                        seasons[curSeason]["5-10%"].append(-1)
                elif ((row[timing + " X"] - 1) * row[pType + "p_X"] - (1 - row[pType + "p_X"]) < 0.175):
                    if (row["home_team_reg_score"] == row["away_team_reg_score"]):
                        seasons[curSeason]["10-17.5%"].append(row[timing + " X"] - 1)
                    else:
                        seasons[curSeason]["10-17.5%"].append(-1)
                elif ((row[timing + " X"] - 1) * row[pType + "p_X"] - (1 - row[pType + "p_X"]) < 0.25):
                    if (row["home_team_reg_score"] == row["away_team_reg_score"]):
                        seasons[curSeason]["17.5-25%"].append(row[timing + " X"] - 1)
                    else:
                        seasons[curSeason]["17.5-25%"].append(-1)
                elif ((row[timing + " X"] - 1) * row[pType + "p_X"] - (1 - row[pType + "p_X"]) < 0.40):
                    if (row["home_team_reg_score"] == row["away_team_reg_score"]):
                        seasons[curSeason]["25-40%"].append(row[timing + " X"] - 1)
                    else:
                        seasons[curSeason]["25-40%"].append(-1)
                else:
                    if (row["home_team_reg_score"] == row["away_team_reg_score"]):
                        seasons[curSeason]["40%+"].append(row[timing + " X"] - 1)
                    else:
                        seasons[curSeason]["40%+"].append(-1)
            if (row[pType + "p_2"] > 1 / row[timing + " 2"]):
                if ((row[timing + " 2"] - 1) * row[pType + "p_2"] - (1 - row[pType + "p_2"]) < 0.03):
                    if (row["home_team_reg_score"] < row["away_team_reg_score"]):
                        seasons[curSeason]["<3%"].append(row[timing + " 2"] - 1)
                    else:
                        seasons[curSeason]["<3%"].append(-1)
                elif ((row[timing + " 2"] - 1) * row[pType + "p_2"] - (1 - row[pType + "p_2"]) < 0.05):
                    if (row["home_team_reg_score"] < row["away_team_reg_score"]):
                        seasons[curSeason]["3-5%"].append(row[timing + " 2"] - 1)
                    else:
                        seasons[curSeason]["3-5%"].append(-1)
                elif ((row[timing + " 2"] - 1) * row[pType + "p_2"] - (1 - row[pType + "p_2"]) < 0.10):
                    if (row["home_team_reg_score"] < row["away_team_reg_score"]):
                        seasons[curSeason]["5-10%"].append(row[timing + " 2"] - 1)
                    else:
                        seasons[curSeason]["5-10%"].append(-1)
                elif ((row[timing + " 2"] - 1) * row[pType + "p_2"] - (1 - row[pType + "p_2"]) < 0.175):
                    if (row["home_team_reg_score"] < row["away_team_reg_score"]):
                        seasons[curSeason]["10-17.5%"].append(row[timing + " 2"] - 1)
                    else:
                        seasons[curSeason]["10-17.5%"].append(-1)
                elif ((row[timing + " 2"] - 1) * row[pType + "p_2"] - (1 - row[pType + "p_2"]) < 0.25):
                    if (row["home_team_reg_score"] < row["away_team_reg_score"]):
                        seasons[curSeason]["17.5-25%"].append(row[timing + " 2"] - 1)
                    else:
                        seasons[curSeason]["17.5-25%"].append(-1)
                elif ((row[timing + " 2"] - 1) * row[pType + "p_2"] - (1 - row[pType + "p_2"]) < 0.40):
                    if (row["home_team_reg_score"] < row["away_team_reg_score"]):
                        seasons[curSeason]["25-40%"].append(row[timing + " 2"] - 1)
                    else:
                        seasons[curSeason]["25-40%"].append(-1)
                else:
                    if (row["home_team_reg_score"] < row["away_team_reg_score"]):
                        seasons[curSeason]["40%+"].append(row[timing + " 2"] - 1)
                    else:
                        seasons[curSeason]["40%+"].append(-1)

        elif (betType == "AH"):
            if (row[pType + "p_" + timing + "_home_cover"] > 1 / row["Home " + timing + " AH Odds"]):
                if ((row["Home " + timing + " AH Odds"] - 1) * row[pType + "p_" + timing + "_home_cover"] - (1 - row[pType + "p_" + timing + "_home_cover"]) < 0.03):
                    if (".75" not in str(row[timing + " AH"]) and ".25" not in str(row[timing + " AH"])):
                        if (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["<3%"].append(row["Home " + timing + " AH Odds"] - 1)
                        elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["<3%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += (row["Home " + timing + " AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += -1/2
                        seasons[curSeason]["<3%"].append(ret)
                elif ((row["Home " + timing + " AH Odds"] - 1) * row[pType + "p_" + timing + "_home_cover"] - (1 - row[pType + "p_" + timing + "_home_cover"]) < 0.05):
                    if (".75" not in str(row[timing + " AH"]) and ".25" not in str(row[timing + " AH"])):
                        if (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["3-5%"].append(row["Home " + timing + " AH Odds"] - 1)
                        elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["3-5%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += (row["Home " + timing + " AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += -1/2
                        seasons[curSeason]["3-5%"].append(ret)
                elif ((row["Home " + timing + " AH Odds"] - 1) * row[pType + "p_" + timing + "_home_cover"] - (1 - row[pType + "p_" + timing + "_home_cover"]) < 0.10):
                    if (".75" not in str(row[timing + " AH"]) and ".25" not in str(row[timing + " AH"])):
                        if (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["5-10%"].append(row["Home " + timing + " AH Odds"] - 1)
                        elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["5-10%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += (row["Home " + timing + " AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += -1/2
                        seasons[curSeason]["5-10%"].append(ret)
                elif ((row["Home " + timing + " AH Odds"] - 1) * row[pType + "p_" + timing + "_home_cover"] - (1 - row[pType + "p_" + timing + "_home_cover"]) < 0.175):
                    if (".75" not in str(row[timing + " AH"]) and ".25" not in str(row[timing + " AH"])):
                        if (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["10-17.5%"].append(row["Home " + timing + " AH Odds"] - 1)
                        elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["10-17.5%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += (row["Home " + timing + " AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += -1/2
                        seasons[curSeason]["10-17.5%"].append(ret)
                elif ((row["Home " + timing + " AH Odds"] - 1) * row[pType + "p_" + timing + "_home_cover"] - (1 - row[pType + "p_" + timing + "_home_cover"]) < 0.25):
                    if (".75" not in str(row[timing + " AH"]) and ".25" not in str(row[timing + " AH"])):
                        if (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["17.5-25%"].append(row["Home " + timing + " AH Odds"] - 1)
                        elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["17.5-25%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += (row["Home " + timing + " AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += -1/2
                        seasons[curSeason]["17.5-25%"].append(ret)
                elif ((row["Home " + timing + " AH Odds"] - 1) * row[pType + "p_" + timing + "_home_cover"] - (1 - row[pType + "p_" + timing + "_home_cover"]) < 0.40):
                    if (".75" not in str(row[timing + " AH"]) and ".25" not in str(row[timing + " AH"])):
                        if (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["25-40%"].append(row["Home " + timing + " AH Odds"] - 1)
                        elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["25-40%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += (row["Home " + timing + " AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += -1/2
                        seasons[curSeason]["25-40%"].append(ret)
                else:
                    if (".75" not in str(row[timing + " AH"]) and ".25" not in str(row[timing + " AH"])):
                        if (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["40%+"].append(row["Home " + timing + " AH Odds"] - 1)
                        elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["40%+"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += (row["Home " + timing + " AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += -1/2
                        seasons[curSeason]["40%+"].append(ret)
            elif ((1 - row[pType + "p_" + timing + "_home_cover"]) > 1 / row["Away " + timing + " AH Odds"]):
                if ((row["Away " + timing + " AH Odds"] - 1) * (1 - row[pType + "p_" + timing + "_home_cover"]) - (1 - (1 - row[pType + "p_" + timing + "_home_cover"])) < 0.03):
                    if (".75" not in str(row[timing + " AH"]) and ".25" not in str(row[timing + " AH"])):
                        if (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["<3%"].append(row["Away " + timing + " AH Odds"] - 1)
                        elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["<3%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += (row["Away " + timing + " AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += -1/2
                        seasons[curSeason]["<3%"].append(ret)
                elif ((row["Away " + timing + " AH Odds"] - 1) * (1 - row[pType + "p_" + timing + "_home_cover"]) - (1 - (1 - row[pType + "p_" + timing + "_home_cover"])) < 0.05):
                    if (".75" not in str(row[timing + " AH"]) and ".25" not in str(row[timing + " AH"])):
                        if (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["3-5%"].append(row["Away " + timing + " AH Odds"] - 1)
                        elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["3-5%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += (row["Away " + timing + " AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += -1/2
                        seasons[curSeason]["3-5%"].append(ret)
                elif ((row["Away " + timing + " AH Odds"] - 1) * (1 - row[pType + "p_" + timing + "_home_cover"]) - (1 - (1 - row[pType + "p_" + timing + "_home_cover"])) < 0.10):
                    if (".75" not in str(row[timing + " AH"]) and ".25" not in str(row[timing + " AH"])):
                        if (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["5-10%"].append(row["Away " + timing + " AH Odds"] - 1)
                        elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["5-10%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += (row["Away " + timing + " AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += -1/2
                        seasons[curSeason]["5-10%"].append(ret)
                elif ((row["Away " + timing + " AH Odds"] - 1) * (1 - row[pType + "p_" + timing + "_home_cover"]) - (1 - (1 - row[pType + "p_" + timing + "_home_cover"])) < 0.175):
                    if (".75" not in str(row[timing + " AH"]) and ".25" not in str(row[timing + " AH"])):
                        if (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["10-17.5%"].append(row["Away " + timing + " AH Odds"] - 1)
                        elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["10-17.5%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += (row["Away " + timing + " AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += -1/2
                        seasons[curSeason]["10-17.5%"].append(ret)
                elif ((row["Away " + timing + " AH Odds"] - 1) * (1 - row[pType + "p_" + timing + "_home_cover"]) - (1 - (1 - row[pType + "p_" + timing + "_home_cover"])) < 0.25):
                    if (".75" not in str(row[timing + " AH"]) and ".25" not in str(row[timing + " AH"])):
                        if (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["17.5-25%"].append(row["Away " + timing + " AH Odds"] - 1)
                        elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["17.5-25%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += (row["Away " + timing + " AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += -1/2
                        seasons[curSeason]["17.5-25%"].append(ret)
                elif ((row["Away " + timing + " AH Odds"] - 1) * (1 - row[pType + "p_" + timing + "_home_cover"]) - (1 - (1 - row[pType + "p_" + timing + "_home_cover"])) < 0.40):
                    if (".75" not in str(row[timing + " AH"]) and ".25" not in str(row[timing + " AH"])):
                        if (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["25-40%"].append(row["Away " + timing + " AH Odds"] - 1)
                        elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["25-40%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += (row["Away " + timing + " AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += -1/2
                        seasons[curSeason]["25-40%"].append(ret)
                else:
                    if (".75" not in str(row[timing + " AH"]) and ".25" not in str(row[timing + " AH"])):
                        if (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["40%+"].append(row["Away " + timing + " AH Odds"] - 1)
                        elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                            seasons[curSeason]["40%+"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += (row["Away " + timing + " AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                                ret += -1/2
                        seasons[curSeason]["40%+"].append(ret)
        elif (betType == "OU"):
            if (row[pType + "p_" + timing + "_over"] > 1 / row["Over " + timing + " OU Odds"]):
                if ((row["Over " + timing + " OU Odds"] - 1) * row[pType + "p_" + timing + "_over"] - (1 - row[pType + "p_" + timing + "_over"]) < 0.03):
                    if (".75" not in str(row[timing + " OU"]) and ".25" not in str(row[timing + " OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                            seasons[curSeason]["<3%"].append(row["Over " + timing + " OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                            seasons[curSeason]["<3%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                                ret += (row["Over " + timing + " OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                                ret += -1/2
                        seasons[curSeason]["<3%"].append(ret)
                elif ((row["Over " + timing + " OU Odds"] - 1) * row[pType + "p_" + timing + "_over"] - (1 - row[pType + "p_" + timing + "_over"]) < 0.05):
                    if (".75" not in str(row[timing + " OU"]) and ".25" not in str(row[timing + " OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                            seasons[curSeason]["3-5%"].append(row["Over " + timing + " OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                            seasons[curSeason]["3-5%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                                ret += (row["Over " + timing + " OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                                ret += -1/2
                        seasons[curSeason]["3-5%"].append(ret)
                elif ((row["Over " + timing + " OU Odds"] - 1) * row[pType + "p_" + timing + "_over"] - (1 - row[pType + "p_" + timing + "_over"]) < 0.10):
                    if (".75" not in str(row[timing + " OU"]) and ".25" not in str(row[timing + " OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                            seasons[curSeason]["5-10%"].append(row["Over " + timing + " OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                            seasons[curSeason]["5-10%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                                ret += (row["Over " + timing + " OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                                ret += -1/2
                        seasons[curSeason]["5-10%"].append(ret)
                elif ((row["Over " + timing + " OU Odds"] - 1) * row[pType + "p_" + timing + "_over"] - (1 - row[pType + "p_" + timing + "_over"]) < 0.175):
                    if (".75" not in str(row[timing + " OU"]) and ".25" not in str(row[timing + " OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                            seasons[curSeason]["10-17.5%"].append(row["Over " + timing + " OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                            seasons[curSeason]["10-17.5%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                                ret += (row["Over " + timing + " OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                                ret += -1/2
                        seasons[curSeason]["10-17.5%"].append(ret)
                elif ((row["Over " + timing + " OU Odds"] - 1) * row[pType + "p_" + timing + "_over"] - (1 - row[pType + "p_" + timing + "_over"]) < 0.25):
                    if (".75" not in str(row[timing + " OU"]) and ".25" not in str(row[timing + " OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                            seasons[curSeason]["17.5-25%"].append(row["Over " + timing + " OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                            seasons[curSeason]["17.5-25%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                                ret += (row["Over " + timing + " OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                                ret += -1/2
                        seasons[curSeason]["17.5-25%"].append(ret)
                elif ((row["Over " + timing + " OU Odds"] - 1) * row[pType + "p_" + timing + "_over"] - (1 - row[pType + "p_" + timing + "_over"]) < 0.40):
                    if (".75" not in str(row[timing + " OU"]) and ".25" not in str(row[timing + " OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                            seasons[curSeason]["25-40%"].append(row["Over " + timing + " OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                            seasons[curSeason]["25-40%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                                ret += (row["Over " + timing + " OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                                ret += -1/2
                        seasons[curSeason]["25-40%"].append(ret)
                else:
                    if (".75" not in str(row[timing + " OU"]) and ".25" not in str(row[timing + " OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                            seasons[curSeason]["40%+"].append(row["Over " + timing + " OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                            seasons[curSeason]["40%+"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                                ret += (row["Over " + timing + " OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                                ret += -1/2
                        seasons[curSeason]["40%+"].append(ret)
            elif ((1 - row[pType + "p_" + timing + "_over"]) > 1 / row["Under " + timing + " OU Odds"]):
                if ((row["Under " + timing + " OU Odds"] - 1) * (1 - row[pType + "p_" + timing + "_over"]) - (1 - (1 - row[pType + "p_" + timing + "_over"])) < 0.03):
                    if (".75" not in str(row[timing + " OU"]) and ".25" not in str(row[timing + " OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                            seasons[curSeason]["<3%"].append(row["Under " + timing + " OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                            seasons[curSeason]["<3%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                                ret += (row["Under " + timing + " OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                                ret += -1/2
                        seasons[curSeason]["<3%"].append(ret)
                elif ((row["Under " + timing + " OU Odds"] - 1) * (1 - row[pType + "p_" + timing + "_over"]) - (1 - (1 - row[pType + "p_" + timing + "_over"])) < 0.05):
                    if (".75" not in str(row[timing + " OU"]) and ".25" not in str(row[timing + " OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                            seasons[curSeason]["3-5%"].append(row["Under " + timing + " OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                            seasons[curSeason]["3-5%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                                ret += (row["Under " + timing + " OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                                ret += -1/2
                        seasons[curSeason]["3-5%"].append(ret)
                elif ((row["Under " + timing + " OU Odds"] - 1) * (1 - row[pType + "p_" + timing + "_over"]) - (1 - (1 - row[pType + "p_" + timing + "_over"])) < 0.10):
                    if (".75" not in str(row[timing + " OU"]) and ".25" not in str(row[timing + " OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                            seasons[curSeason]["5-10%"].append(row["Under " + timing + " OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                            seasons[curSeason]["5-10%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                                ret += (row["Under " + timing + " OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                                ret += -1/2
                        seasons[curSeason]["5-10%"].append(ret)
                elif ((row["Under " + timing + " OU Odds"] - 1) * (1 - row[pType + "p_" + timing + "_over"]) - (1 - (1 - row[pType + "p_" + timing + "_over"])) < 0.175):
                    if (".75" not in str(row[timing + " OU"]) and ".25" not in str(row[timing + " OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                            seasons[curSeason]["10-17.5%"].append(row["Under " + timing + " OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                            seasons[curSeason]["10-17.5%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                                ret += (row["Under " + timing + " OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                                ret += -1/2
                        seasons[curSeason]["10-17.5%"].append(ret)
                elif ((row["Under " + timing + " OU Odds"] - 1) * (1 - row[pType + "p_" + timing + "_over"]) - (1 - (1 - row[pType + "p_" + timing + "_over"])) < 0.25):
                    if (".75" not in str(row[timing + " OU"]) and ".25" not in str(row[timing + " OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                            seasons[curSeason]["17.5-25%"].append(row["Under " + timing + " OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                            seasons[curSeason]["17.5-25%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                                ret += (row["Under " + timing + " OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                                ret += -1/2
                        seasons[curSeason]["17.5-25%"].append(ret)
                elif ((row["Under " + timing + " OU Odds"] - 1) * (1 - row[pType + "p_" + timing + "_over"]) - (1 - (1 - row[pType + "p_" + timing + "_over"])) < 0.40):
                    if (".75" not in str(row[timing + " OU"]) and ".25" not in str(row[timing + " OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                            seasons[curSeason]["25-40%"].append(row["Under " + timing + " OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                            seasons[curSeason]["25-40%"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                                ret += (row["Under " + timing + " OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                                ret += -1/2
                        seasons[curSeason]["25-40%"].append(ret)
                else:
                    if (".75" not in str(row[timing + " OU"]) and ".25" not in str(row[timing + " OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                            seasons[curSeason]["40%+"].append(row["Under " + timing + " OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                            seasons[curSeason]["40%+"].append(-1)
                    else:
                        ret = 0
                        parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                                ret += (row["Under " + timing + " OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                                ret += -1/2
                        seasons[curSeason]["40%+"].append(ret)
    all = {"<3%":[],"3-5%":[],"5-10%":[],"10-17.5%":[],"17.5-25%":[],"25-40%":[],"40%+":[]}
    for season in seasons:
        print (season + "---------------------------------------------------------")
        for key in seasons[season]:
            print (key + ":", np.average(seasons[season][key]), len(seasons[season][key]))
            for x in seasons[season][key]:
                all[key].append(x)
    print ("All----------------------------------------------------")
    for key in all:
        print (key + ":", np.average(all[key]), len(all[key]))

def kellybet(league, betType, timing, bankroll, kellyDiv, betThresh, pType = ""):
    pred = pd.read_csv("./csv_data/" + league + "/bayes_predictions_transfer_val.csv", encoding = "ISO-8859-1")
    for i in range(len(pred.index)):
        pred.at[i, "Date"] = datetime.date(int(pred.at[i, "Date"].split("-")[0]), int(pred.at[i, "Date"].split("-")[1]), int(pred.at[i, "Date"].split("-")[2]))
    seasons = {}
    preBR = bankroll
    for index, row in pred.iterrows():
        if (index == 0 or abs(row["Date"] - pred.at[index - 1,"Date"]).days > 30):
            if (str(row["Date"].year) not in seasons):
                seasons[str(row["Date"].year)] = {"netwin":0}
                curSeason = str(row["Date"].year)
            else:
                seasons[str(row["Date"].year) + "_2"] = {"netwin":0}
                curSeason = str(row["Date"].year) + "_2"
        if (betType == "AH"):
            if ((row["Home " + timing + " AH Odds"] - 1) * row[pType + "p_" + timing + "_home_cover"] - (1 - row[pType + "p_" + timing + "_home_cover"]) > betThresh):
                if (".75" not in str(row[timing + " AH"]) and ".25" not in str(row[timing + " AH"])):
                    if (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                        bankroll += bankroll * kellyStake(row[pType + "p_" + timing + "_home_cover"], row["Home " + timing + " AH Odds"], kellyDiv) * (row["Home " + timing + " AH Odds"] - 1)
                        seasons[curSeason]["netwin"] += preBR * kellyStake(row[pType + "p_" + timing + "_home_cover"], row["Home " + timing + " AH Odds"], kellyDiv) * (row["Home " + timing + " AH Odds"] - 1)
                    elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                        bankroll -= bankroll * kellyStake(row[pType + "p_" + timing + "_home_cover"], row["Home " + timing + " AH Odds"], kellyDiv)
                        seasons[curSeason]["netwin"] -= preBR * kellyStake(row[pType + "p_" + timing + "_home_cover"], row["Home " + timing + " AH Odds"], kellyDiv)
                else:
                    parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                    for part in parts:
                        if (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                            bankroll += bankroll * kellyStake(row[pType + "p_" + timing + "_home_cover"], row["Home " + timing + " AH Odds"], kellyDiv) * (row["Home " + timing + " AH Odds"] - 1) / 2
                            seasons[curSeason]["netwin"] += preBR * kellyStake(row[pType + "p_" + timing + "_home_cover"], row["Home " + timing + " AH Odds"], kellyDiv) * (row["Home " + timing + " AH Odds"] - 1) / 2
                        elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                            bankroll -= bankroll * kellyStake(row[pType + "p_" + timing + "_home_cover"], row["Home " + timing + " AH Odds"], kellyDiv) / 2
                            seasons[curSeason]["netwin"] -= preBR * kellyStake(row[pType + "p_" + timing + "_home_cover"], row["Home " + timing + " AH Odds"], kellyDiv) / 2
            elif ((row["Away " + timing + " AH Odds"] - 1) * (1 - row[pType + "p_" + timing + "_home_cover"]) - (1 - (1 - row[pType + "p_" + timing + "_home_cover"])) > betThresh):
                if (".75" not in str(row[timing + " AH"]) and ".25" not in str(row[timing + " AH"])):
                    if (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                        bankroll += bankroll * kellyStake((1 - row[pType + "p_" + timing + "_home_cover"]), row["Away " + timing + " AH Odds"], kellyDiv) * (row["Away " + timing + " AH Odds"] - 1)
                        seasons[curSeason]["netwin"] += preBR * kellyStake((1 - row[pType + "p_" + timing + "_home_cover"]), row["Away " + timing + " AH Odds"], kellyDiv) * (row["Away " + timing + " AH Odds"] - 1)
                    elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                        bankroll -= bankroll * kellyStake((1 - row[pType + "p_" + timing + "_home_cover"]), row["Away " + timing + " AH Odds"], kellyDiv)
                        seasons[curSeason]["netwin"] -= preBR * kellyStake((1 - row[pType + "p_" + timing + "_home_cover"]), row["Away " + timing + " AH Odds"], kellyDiv)
                else:
                    parts = [row[timing + " AH"] - 0.25,row[timing + " AH"] + 0.25]
                    for part in parts:
                        if (row["home_team_reg_score"] < row["away_team_reg_score"] + row[timing + " AH"]):
                            bankroll += bankroll * kellyStake((1 - row[pType + "p_" + timing + "_home_cover"]), row["Away " + timing + " AH Odds"], kellyDiv) * (row["Away " + timing + " AH Odds"] - 1) / 2
                            seasons[curSeason]["netwin"] += preBR * kellyStake((1 - row[pType + "p_" + timing + "_home_cover"]), row["Away " + timing + " AH Odds"], kellyDiv) * (row["Away " + timing + " AH Odds"] - 1) / 2
                        elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row[timing + " AH"]):
                            bankroll -= bankroll * kellyStake((1 - row[pType + "p_" + timing + "_home_cover"]), row["Away " + timing + " AH Odds"], kellyDiv) / 2
                            seasons[curSeason]["netwin"] -= preBR * kellyStake((1 - row[pType + "p_" + timing + "_home_cover"]), row["Away " + timing + " AH Odds"], kellyDiv) / 2
        elif (betType == "OU"):
            if ((row["Over " + timing + " OU Odds"] - 1) * row[pType + "p_" + timing + "_over"] - (1 - row[pType + "p_" + timing + "_over"]) > betThresh):
                if (".75" not in str(row[timing + " OU"]) and ".25" not in str(row[timing + " OU"])):
                    if (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                        bankroll += bankroll * kellyStake(row[pType + "p_" + timing + "_over"], row["Over " + timing + " OU Odds"], kellyDiv) * (row["Over " + timing + " OU Odds"] - 1)
                        seasons[curSeason]["netwin"] += preBR * kellyStake(row[pType + "p_" + timing + "_over"], row["Over " + timing + " OU Odds"], kellyDiv) * (row["Over " + timing + " OU Odds"] - 1)
                    elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                        bankroll -= bankroll * kellyStake(row[pType + "p_" + timing + "_over"], row["Over " + timing + " OU Odds"], kellyDiv)
                        seasons[curSeason]["netwin"] -= preBR * kellyStake(row[pType + "p_" + timing + "_over"], row["Over " + timing + " OU Odds"], kellyDiv)
                else:
                    parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                    for part in parts:
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                            bankroll += bankroll * kellyStake(row[pType + "p_" + timing + "_over"], row["Over " + timing + " OU Odds"], kellyDiv) * (row["Over " + timing + " OU Odds"] - 1) / 2
                            seasons[curSeason]["netwin"] += preBR * kellyStake(row[pType + "p_" + timing + "_over"], row["Over " + timing + " OU Odds"], kellyDiv) * (row["Over " + timing + " OU Odds"] - 1) / 2
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                            bankroll -= bankroll * kellyStake(row[pType + "p_" + timing + "_over"], row["Over " + timing + " OU Odds"], kellyDiv) / 2
                            seasons[curSeason]["netwin"] -= preBR * kellyStake(row[pType + "p_" + timing + "_over"], row["Over " + timing + " OU Odds"], kellyDiv) / 2
            elif ((row["Under " + timing + " OU Odds"] - 1) * (1 - row[pType + "p_" + timing + "_over"]) - (1 - (1 - row[pType + "p_" + timing + "_over"])) > betThresh):
                if (".75" not in str(row[timing + " OU"]) and ".25" not in str(row[timing + " OU"])):
                    if (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                        bankroll += bankroll * kellyStake((1 - row[pType + "p_" + timing + "_over"]), row["Under " + timing + " OU Odds"], kellyDiv) * (row["Under " + timing + " OU Odds"] - 1)
                        seasons[curSeason]["netwin"] += preBR * kellyStake((1 - row[pType + "p_" + timing + "_over"]), row["Under " + timing + " OU Odds"], kellyDiv) * (row["Under " + timing + " OU Odds"] - 1)
                    elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                        bankroll -= bankroll * kellyStake((1 - row[pType + "p_" + timing + "_over"]), row["Under " + timing + " OU Odds"], kellyDiv)
                        seasons[curSeason]["netwin"] -= preBR * kellyStake((1 - row[pType + "p_" + timing + "_over"]), row["Under " + timing + " OU Odds"], kellyDiv)
                else:

                    parts = [row[timing + " OU"] - 0.25,row[timing + " OU"] + 0.25]
                    for part in parts:
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] < row[timing + " OU"]):
                            bankroll += bankroll * kellyStake((1 - row[pType + "p_" + timing + "_over"]), row["Under " + timing + " OU Odds"], kellyDiv) * (row["Under " + timing + " OU Odds"] - 1) / 2
                            seasons[curSeason]["netwin"] += preBR * kellyStake((1 - row[pType + "p_" + timing + "_over"]), row["Under " + timing + " OU Odds"], kellyDiv) * (row["Under " + timing + " OU Odds"] - 1) / 2
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row[timing + " OU"]):
                            bankroll -= bankroll * kellyStake((1 - row[pType + "p_" + timing + "_over"]), row["Under " + timing + " OU Odds"], kellyDiv) / 2
                            seasons[curSeason]["netwin"] -= preBR * kellyStake((1 - row[pType + "p_" + timing + "_over"]), row["Under " + timing + " OU Odds"], kellyDiv) / 2
    for key in seasons:
        print (key, seasons[key]["netwin"])
    print ("Ending BR:", bankroll)

def analyzeLineMovement(league, betType, moveDirection = "With", pType = ""):
    pred = pd.read_csv("./csv_data/" + league + "/bayes_predictions.csv", encoding = "ISO-8859-1")
    for i in range(len(pred.index)):
        pred.at[i, "Date"] = datetime.date(int(pred.at[i, "Date"].split("-")[0]), int(pred.at[i, "Date"].split("-")[1]), int(pred.at[i, "Date"].split("-")[2]))
    seasons = {}
    for index, row in pred.iterrows():
        if (index == 0 or abs(row["Date"] - pred.at[index - 1,"Date"]).days > 30):
            if (str(row["Date"].year) not in seasons):
                seasons[str(row["Date"].year)] = {"<3%":[],"3-5%":[],"5-10%":[],"10-17.5%":[],"17.5-25%":[],"25-40%":[],"40%+":[]}
                curSeason = str(row["Date"].year)
            else:
                seasons[str(row["Date"].year) + "_2"] = {"<3%":[],"3-5%":[],"5-10%":[],"10-17.5%":[],"17.5-25%":[],"25-40%":[],"40%+":[]}
                curSeason = str(row["Date"].year) + "_2"
        if (betType == "AH"):
            if (row[pType + "p_Close_home_cover"] > 1 / row["Home Close AH Odds"]):
                if (moveDirection == "With"):
                    if (row[pType + "p_Close_home_cover"] > row[pType + "p_Open_home_cover"]):
                        continue
                    elif (row[pType + "p_Close_home_cover"] == row[pType + "p_Open_home_cover"]):
                        continue
                elif (moveDirection == "Against"):
                    if (row[pType + "p_Close_home_cover"] < row[pType + "p_Open_home_cover"]):
                        continue
                    elif (row[pType + "p_Close_home_cover"] == row[pType + "p_Open_home_cover"]):
                        continue
                else:
                    if (row[pType + "p_Close_home_cover"] != row[pType + "p_Open_home_cover"]):
                        continue
                    elif (row[pType + "p_Close_home_cover"] == row[pType + "p_Open_home_cover"]):
                        continue
                if ((row["Home Close AH Odds"] - 1) * row[pType + "p_Close_home_cover"] - (1 - row[pType + "p_Close_home_cover"]) < 0.03):
                    if (".75" not in str(row["Close AH"]) and ".25" not in str(row["Close AH"])):
                        if (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["<3%"].append(row["Home Close AH Odds"] - 1)
                        elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["<3%"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close AH"] - 0.25,row["Close AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                                ret += (row["Home Close AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                                ret += -1/2
                        seasons[curSeason]["<3%"].append(ret)
                elif ((row["Home Close AH Odds"] - 1) * row[pType + "p_Close_home_cover"] - (1 - row[pType + "p_Close_home_cover"]) < 0.05):
                    if (".75" not in str(row["Close AH"]) and ".25" not in str(row["Close AH"])):
                        if (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["3-5%"].append(row["Home Close AH Odds"] - 1)
                        elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["3-5%"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close AH"] - 0.25,row["Close AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                                ret += (row["Home Close AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                                ret += -1/2
                        seasons[curSeason]["3-5%"].append(ret)
                elif ((row["Home Close AH Odds"] - 1) * row[pType + "p_Close_home_cover"] - (1 - row[pType + "p_Close_home_cover"]) < 0.10):
                    if (".75" not in str(row["Close AH"]) and ".25" not in str(row["Close AH"])):
                        if (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["5-10%"].append(row["Home Close AH Odds"] - 1)
                        elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["5-10%"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close AH"] - 0.25,row["Close AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                                ret += (row["Home Close AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                                ret += -1/2
                        seasons[curSeason]["5-10%"].append(ret)
                elif ((row["Home Close AH Odds"] - 1) * row[pType + "p_Close_home_cover"] - (1 - row[pType + "p_Close_home_cover"]) < 0.175):
                    if (".75" not in str(row["Close AH"]) and ".25" not in str(row["Close AH"])):
                        if (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["10-17.5%"].append(row["Home Close AH Odds"] - 1)
                        elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["10-17.5%"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close AH"] - 0.25,row["Close AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                                ret += (row["Home Close AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                                ret += -1/2
                        seasons[curSeason]["10-17.5%"].append(ret)
                elif ((row["Home Close AH Odds"] - 1) * row[pType + "p_Close_home_cover"] - (1 - row[pType + "p_Close_home_cover"]) < 0.25):
                    if (".75" not in str(row["Close AH"]) and ".25" not in str(row["Close AH"])):
                        if (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["17.5-25%"].append(row["Home Close AH Odds"] - 1)
                        elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["17.5-25%"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close AH"] - 0.25,row["Close AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                                ret += (row["Home Close AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                                ret += -1/2
                        seasons[curSeason]["17.5-25%"].append(ret)
                elif ((row["Home Close AH Odds"] - 1) * row[pType + "p_Close_home_cover"] - (1 - row[pType + "p_Close_home_cover"]) < 0.40):
                    if (".75" not in str(row["Close AH"]) and ".25" not in str(row["Close AH"])):
                        if (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["25-40%"].append(row["Home Close AH Odds"] - 1)
                        elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["25-40%"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close AH"] - 0.25,row["Close AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                                ret += (row["Home Close AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                                ret += -1/2
                        seasons[curSeason]["25-40%"].append(ret)
                else:
                    if (".75" not in str(row["Close AH"]) and ".25" not in str(row["Close AH"])):
                        if (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["40%+"].append(row["Home Close AH Odds"] - 1)
                        elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["40%+"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close AH"] - 0.25,row["Close AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                                ret += (row["Home Close AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                                ret += -1/2
                        seasons[curSeason]["40%+"].append(ret)
            elif ((1 - row[pType + "p_Close_home_cover"]) > 1 / row["Away Close AH Odds"]):
                if (moveDirection == "With"):
                    if (row[pType + "p_Close_home_cover"] < row[pType + "p_Open_home_cover"]):
                        continue
                    elif (row[pType + "p_Close_home_cover"] == row[pType + "p_Open_home_cover"] and row["Away Close AH Odds"] >= row["Away Open AH Odds"]):
                        continue
                elif (moveDirection == "Against"):
                    if (row[pType + "p_Close_home_cover"] > row[pType + "p_Open_home_cover"]):
                        continue
                    elif (row[pType + "p_Close_home_cover"] == row[pType + "p_Open_home_cover"] and row["Away Close AH Odds"] <= row["Away Open AH Odds"]):
                        continue
                else:
                    if (row[pType + "p_Close_home_cover"] != row[pType + "p_Open_home_cover"]):
                        continue
                    elif (row[pType + "p_Close_home_cover"] == row[pType + "p_Open_home_cover"] and row["Away Close AH Odds"] != row["Away Open AH Odds"]):
                        continue
                if ((row["Away Close AH Odds"] - 1) * (1 - row[pType + "p_Close_home_cover"]) - (1 - (1 - row[pType + "p_Close_home_cover"])) < 0.03):
                    if (".75" not in str(row["Close AH"]) and ".25" not in str(row["Close AH"])):
                        if (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["<3%"].append(row["Away Close AH Odds"] - 1)
                        elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["<3%"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close AH"] - 0.25,row["Close AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                                ret += (row["Away Close AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                                ret += -1/2
                        seasons[curSeason]["<3%"].append(ret)
                elif ((row["Away Close AH Odds"] - 1) * (1 - row[pType + "p_Close_home_cover"]) - (1 - (1 - row[pType + "p_Close_home_cover"])) < 0.05):
                    if (".75" not in str(row["Close AH"]) and ".25" not in str(row["Close AH"])):
                        if (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["3-5%"].append(row["Away Close AH Odds"] - 1)
                        elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["3-5%"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close AH"] - 0.25,row["Close AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                                ret += (row["Away Close AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                                ret += -1/2
                        seasons[curSeason]["3-5%"].append(ret)
                elif ((row["Away Close AH Odds"] - 1) * (1 - row[pType + "p_Close_home_cover"]) - (1 - (1 - row[pType + "p_Close_home_cover"])) < 0.10):
                    if (".75" not in str(row["Close AH"]) and ".25" not in str(row["Close AH"])):
                        if (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["5-10%"].append(row["Away Close AH Odds"] - 1)
                        elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["5-10%"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close AH"] - 0.25,row["Close AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                                ret += (row["Away Close AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                                ret += -1/2
                        seasons[curSeason]["5-10%"].append(ret)
                elif ((row["Away Close AH Odds"] - 1) * (1 - row[pType + "p_Close_home_cover"]) - (1 - (1 - row[pType + "p_Close_home_cover"])) < 0.175):
                    if (".75" not in str(row["Close AH"]) and ".25" not in str(row["Close AH"])):
                        if (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["10-17.5%"].append(row["Away Close AH Odds"] - 1)
                        elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["10-17.5%"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close AH"] - 0.25,row["Close AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                                ret += (row["Away Close AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                                ret += -1/2
                        seasons[curSeason]["10-17.5%"].append(ret)
                elif ((row["Away Close AH Odds"] - 1) * (1 - row[pType + "p_Close_home_cover"]) - (1 - (1 - row[pType + "p_Close_home_cover"])) < 0.25):
                    if (".75" not in str(row["Close AH"]) and ".25" not in str(row["Close AH"])):
                        if (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["17.5-25%"].append(row["Away Close AH Odds"] - 1)
                        elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["17.5-25%"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close AH"] - 0.25,row["Close AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                                ret += (row["Away Close AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                                ret += -1/2
                        seasons[curSeason]["17.5-25%"].append(ret)
                elif ((row["Away Close AH Odds"] - 1) * (1 - row[pType + "p_Close_home_cover"]) - (1 - (1 - row[pType + "p_Close_home_cover"])) < 0.40):
                    if (".75" not in str(row["Close AH"]) and ".25" not in str(row["Close AH"])):
                        if (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["25-40%"].append(row["Away Close AH Odds"] - 1)
                        elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["25-40%"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close AH"] - 0.25,row["Close AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                                ret += (row["Away Close AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                                ret += -1/2
                        seasons[curSeason]["25-40%"].append(ret)
                else:
                    if (".75" not in str(row["Close AH"]) and ".25" not in str(row["Close AH"])):
                        if (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["40%+"].append(row["Away Close AH Odds"] - 1)
                        elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                            seasons[curSeason]["40%+"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close AH"] - 0.25,row["Close AH"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] < row["away_team_reg_score"] + row["Close AH"]):
                                ret += (row["Away Close AH Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] > row["away_team_reg_score"] + row["Close AH"]):
                                ret += -1/2
                        seasons[curSeason]["40%+"].append(ret)
        elif (betType == "OU"):
            if (row[pType + "p_Close_over"] > 1 / row["Over Close OU Odds"]):
                if ((row["Over Close OU Odds"] - 1) * row[pType + "p_Close_over"] - (1 - row[pType + "p_Close_over"]) < 0.03):
                    if (".75" not in str(row["Close OU"]) and ".25" not in str(row["Close OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                            seasons[curSeason]["<3%"].append(row["Over Close OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                            seasons[curSeason]["<3%"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close OU"] - 0.25,row["Close OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                                ret += (row["Over Close OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                                ret += -1/2
                        seasons[curSeason]["<3%"].append(ret)
                elif ((row["Over Close OU Odds"] - 1) * row[pType + "p_Close_over"] - (1 - row[pType + "p_Close_over"]) < 0.05):
                    if (".75" not in str(row["Close OU"]) and ".25" not in str(row["Close OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                            seasons[curSeason]["3-5%"].append(row["Over Close OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                            seasons[curSeason]["3-5%"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close OU"] - 0.25,row["Close OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                                ret += (row["Over Close OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                                ret += -1/2
                        seasons[curSeason]["3-5%"].append(ret)
                elif ((row["Over Close OU Odds"] - 1) * row[pType + "p_Close_over"] - (1 - row[pType + "p_Close_over"]) < 0.10):
                    if (".75" not in str(row["Close OU"]) and ".25" not in str(row["Close OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                            seasons[curSeason]["5-10%"].append(row["Over Close OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                            seasons[curSeason]["5-10%"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close OU"] - 0.25,row["Close OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                                ret += (row["Over Close OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                                ret += -1/2
                        seasons[curSeason]["5-10%"].append(ret)
                elif ((row["Over Close OU Odds"] - 1) * row[pType + "p_Close_over"] - (1 - row[pType + "p_Close_over"]) < 0.175):
                    if (".75" not in str(row["Close OU"]) and ".25" not in str(row["Close OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                            seasons[curSeason]["10-17.5%"].append(row["Over Close OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                            seasons[curSeason]["10-17.5%"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close OU"] - 0.25,row["Close OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                                ret += (row["Over Close OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                                ret += -1/2
                        seasons[curSeason]["10-17.5%"].append(ret)
                elif ((row["Over Close OU Odds"] - 1) * row[pType + "p_Close_over"] - (1 - row[pType + "p_Close_over"]) < 0.25):
                    if (".75" not in str(row["Close OU"]) and ".25" not in str(row["Close OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                            seasons[curSeason]["17.5-25%"].append(row["Over Close OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                            seasons[curSeason]["17.5-25%"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close OU"] - 0.25,row["Close OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                                ret += (row["Over Close OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                                ret += -1/2
                        seasons[curSeason]["17.5-25%"].append(ret)
                elif ((row["Over Close OU Odds"] - 1) * row[pType + "p_Close_over"] - (1 - row[pType + "p_Close_over"]) < 0.40):
                    if (".75" not in str(row["Close OU"]) and ".25" not in str(row["Close OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                            seasons[curSeason]["25-40%"].append(row["Over Close OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                            seasons[curSeason]["25-40%"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close OU"] - 0.25,row["Close OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                                ret += (row["Over Close OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                                ret += -1/2
                        seasons[curSeason]["25-40%"].append(ret)
                else:
                    if (".75" not in str(row["Close OU"]) and ".25" not in str(row["Close OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                            seasons[curSeason]["40%+"].append(row["Over Close OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                            seasons[curSeason]["40%+"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close OU"] - 0.25,row["Close OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                                ret += (row["Over Close OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                                ret += -1/2
                        seasons[curSeason]["40%+"].append(ret)
            elif ((1 - row[pType + "p_Close_over"]) > 1 / row["Under Close OU Odds"]):
                if ((row["Under Close OU Odds"] - 1) * (1 - row[pType + "p_Close_over"]) - (1 - (1 - row[pType + "p_Close_over"])) < 0.03):
                    if (".75" not in str(row["Close OU"]) and ".25" not in str(row["Close OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                            seasons[curSeason]["<3%"].append(row["Under Close OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                            seasons[curSeason]["<3%"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close OU"] - 0.25,row["Close OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                                ret += (row["Under Close OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                                ret += -1/2
                        seasons[curSeason]["<3%"].append(ret)
                elif ((row["Under Close OU Odds"] - 1) * (1 - row[pType + "p_Close_over"]) - (1 - (1 - row[pType + "p_Close_over"])) < 0.05):
                    if (".75" not in str(row["Close OU"]) and ".25" not in str(row["Close OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                            seasons[curSeason]["3-5%"].append(row["Under Close OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                            seasons[curSeason]["3-5%"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close OU"] - 0.25,row["Close OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                                ret += (row["Under Close OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                                ret += -1/2
                        seasons[curSeason]["3-5%"].append(ret)
                elif ((row["Under Close OU Odds"] - 1) * (1 - row[pType + "p_Close_over"]) - (1 - (1 - row[pType + "p_Close_over"])) < 0.10):
                    if (".75" not in str(row["Close OU"]) and ".25" not in str(row["Close OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                            seasons[curSeason]["5-10%"].append(row["Under Close OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                            seasons[curSeason]["5-10%"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close OU"] - 0.25,row["Close OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                                ret += (row["Under Close OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                                ret += -1/2
                        seasons[curSeason]["5-10%"].append(ret)
                elif ((row["Under Close OU Odds"] - 1) * (1 - row[pType + "p_Close_over"]) - (1 - (1 - row[pType + "p_Close_over"])) < 0.175):
                    if (".75" not in str(row["Close OU"]) and ".25" not in str(row["Close OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                            seasons[curSeason]["10-17.5%"].append(row["Under Close OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                            seasons[curSeason]["10-17.5%"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close OU"] - 0.25,row["Close OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                                ret += (row["Under Close OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                                ret += -1/2
                        seasons[curSeason]["10-17.5%"].append(ret)
                elif ((row["Under Close OU Odds"] - 1) * (1 - row[pType + "p_Close_over"]) - (1 - (1 - row[pType + "p_Close_over"])) < 0.25):
                    if (".75" not in str(row["Close OU"]) and ".25" not in str(row["Close OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                            seasons[curSeason]["17.5-25%"].append(row["Under Close OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                            seasons[curSeason]["17.5-25%"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close OU"] - 0.25,row["Close OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                                ret += (row["Under Close OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                                ret += -1/2
                        seasons[curSeason]["17.5-25%"].append(ret)
                elif ((row["Under Close OU Odds"] - 1) * (1 - row[pType + "p_Close_over"]) - (1 - (1 - row[pType + "p_Close_over"])) < 0.40):
                    if (".75" not in str(row["Close OU"]) and ".25" not in str(row["Close OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                            seasons[curSeason]["25-40%"].append(row["Under Close OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                            seasons[curSeason]["25-40%"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close OU"] - 0.25,row["Close OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                                ret += (row["Under Close OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                                ret += -1/2
                        seasons[curSeason]["25-40%"].append(ret)
                else:
                    if (".75" not in str(row["Close OU"]) and ".25" not in str(row["Close OU"])):
                        if (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                            seasons[curSeason]["40%+"].append(row["Under Close OU Odds"] - 1)
                        elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                            seasons[curSeason]["40%+"].append(-1)
                    else:
                        ret = 0
                        parts = [row["Close OU"] - 0.25,row["Close OU"] + 0.25]
                        for part in parts:
                            if (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Close OU"]):
                                ret += (row["Under Close OU Odds"] - 1) / 2
                            elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Close OU"]):
                                ret += -1/2
                        seasons[curSeason]["40%+"].append(ret)
    all = {"<3%":[],"3-5%":[],"5-10%":[],"10-17.5%":[],"17.5-25%":[],"25-40%":[],"40%+":[]}
    for season in seasons:
        print (season + "---------------------------------------------------------")
        for key in seasons[season]:
            print (key + ":", np.average(seasons[season][key]), len(seasons[season][key]))
            for x in seasons[season][key]:
                all[key].append(x)
    print ("All----------------------------------------------------")
    for key in all:
        print (key + ":", np.average(all[key]), len(all[key]))
