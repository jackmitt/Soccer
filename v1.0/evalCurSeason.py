import pandas as pd
import numpy as np
import os
from miscFcns import standardizeTeamName

bankroll = 30000*0.86
betSizes = []
mwThru = 12

for i in range(6,mwThru+1):
    filename = "MW" + str(i) + ".csv"
    print ("----------------------FILENAME----------------------:", filename)
    preBR = bankroll
    pred = pd.read_csv('./EPL_Csvs/2020-21_Season/testPredictions/' + filename, encoding = "ISO-8859-1")
    stats = pd.read_csv('./EPL_Csvs/2020-21_Season/match_stats/' + filename, encoding = "ISO-8859-1")
    for index, row in pred.iterrows():
        if (row["Edge"] > 1):
            continue
        for i, r in stats.iterrows():
            if (standardizeTeamName(r["Home"]) == standardizeTeamName(row["Home"]) and standardizeTeamName(r["Away"]) == standardizeTeamName(row["Away"])):
                # if (row["Bet"] == "1"):
                #     if (r["Home Score"] > r["Away Score"]):
                #         bankroll += row["Bet Size"] * (row["Book Odds"] - 1) * preBR
                #     else:
                #         bankroll -= row["Bet Size"] * preBR
                # elif (row["Bet"] == "2"):
                #     if (r["Away Score"] > r["Home Score"]):
                #         bankroll += row["Bet Size"] * (row["Book Odds"] - 1) * preBR
                #     else:
                #         bankroll -= row["Bet Size"] * preBR
                # else:
                #     if (r["Away Score"] == r["Home Score"]):
                #         bankroll += row["Bet Size"] * (row["Book Odds"] - 1) * preBR
                #     else:
                #         bankroll -= row["Bet Size"] * preBR
                if ("AH" in row["Bet"]):
                    betSizes.append(row["Bet Size"])
                    if (row["Bet"].split()[1].split(".")[1] != "25" and row["Bet"].split()[1].split(".")[1] != "75"):
                        if ("(1)" in row["Bet"]):
                            if (r["Away Score"] - r["Home Score"] < float(row["Bet"].split()[1])):
                                bankroll += row["Bet Size"]*preBR*(row["Book Odds"] - 1)
                            elif (r["Away Score"] - r["Home Score"] > float(row["Bet"].split()[1])):
                                bankroll -= row["Bet Size"]*preBR
                        else:
                            if (r["Home Score"] - r["Away Score"] < 0-float(row["Bet"].split()[1])):
                                bankroll += row["Bet Size"]*preBR*(row["Book Odds"] - 1)
                            elif (r["Home Score"] - r["Away Score"] > 0-float(row["Bet"].split()[1])):
                                bankroll -= row["Bet Size"]*preBR
                    else:
                        if (row["Bet"].split()[1][0] == "-" and row["Bet"].split()[1].split(".")[1] == "75"):
                            toAdd = -0.25
                        elif (row["Bet"].split()[1][0] != "-" and row["Bet"].split()[1].split(".")[1] == "25"):
                            toAdd = -0.25
                        else:
                            toAdd = 0.25
                        if ("(1)" in row["Bet"]):
                            if (r["Away Score"] - r["Home Score"] < float(row["Bet"].split()[1]) + toAdd):
                                bankroll += row["Bet Size"]*preBR*(row["Book Odds"] - 1)
                            elif (r["Away Score"] - r["Home Score"] > float(row["Bet"].split()[1]) + toAdd):
                                bankroll -= row["Bet Size"]*preBR
                            else:
                                if ((row["Bet"].split()[1][0] == "-" and row["Bet"].split()[1].split(".")[1] == "75") or (row["Bet"].split()[1][0] != "-" and row["Bet"].split()[1].split(".")[1] == "25")):
                                    bankroll += (row["Bet Size"]*preBR*(row["Book Odds"] - 1))/2
                                else:
                                    bankroll -= (row["Bet Size"]*preBR)/2
                        else:
                            if (r["Home Score"] - r["Away Score"] < 0-float(row["Bet"].split()[1]) - toAdd):
                                bankroll += row["Bet Size"]*preBR*(row["Book Odds"] - 1)
                            elif (r["Home Score"] - r["Away Score"] > 0-float(row["Bet"].split()[1]) - toAdd):
                                bankroll -= row["Bet Size"]*preBR
                            else:
                                if ((row["Bet"].split()[1][0] == "-" and row["Bet"].split()[1].split(".")[1] == "25") or (row["Bet"].split()[1][0] != "-" and row["Bet"].split()[1].split(".")[1] == "75")):
                                    bankroll += (row["Bet Size"]*preBR*(row["Book Odds"] - 1))/2
                                else:
                                    bankroll -= (row["Bet Size"]*preBR)/2
                if ("Over" in row["Bet"] or "Under" in row["Bet"]):
                    betSizes.append(row["Bet Size"])
                    if (row["Bet"].split()[1].split(".")[1] != "25" and row["Bet"].split()[1].split(".")[1] != "75"):
                        if ("Over" in row["Bet"]):
                            if (r["Home Score"] + r["Away Score"] > float(row["Bet"].split()[1])):
                                bankroll += row["Bet Size"]*preBR*(row["Book Odds"] - 1)
                            elif (r["Home Score"] + r["Away Score"] < float(row["Bet"].split()[1])):
                                bankroll -= row["Bet Size"]*preBR
                        else:
                            if (r["Home Score"] + r["Away Score"] < float(row["Bet"].split()[1])):
                                bankroll += row["Bet Size"]*preBR*(row["Book Odds"] - 1)
                            elif (r["Home Score"] + r["Away Score"] > float(row["Bet"].split()[1])):
                                bankroll -= row["Bet Size"]*preBR
                    elif (row["Bet"].split()[1].split(".")[1] == "25"):
                        if ("Over" in row["Bet"]):
                            if (r["Home Score"] + r["Away Score"] == float(row["Bet"].split()[1]) - 0.25):
                                bankroll -= row["Bet Size"]*preBR/2
                            elif (r["Home Score"] + r["Away Score"] > float(row["Bet"].split()[1])):
                                bankroll += row["Bet Size"]*preBR*(row["Book Odds"] - 1)
                            else:
                                bankroll -= row["Bet Size"]*preBR
                        else:
                            if (r["Home Score"] + r["Away Score"] == float(row["Bet"].split()[1]) - 0.25):
                                bankroll += row["Bet Size"]*preBR*(row["Book Odds"] - 1)/2
                            elif (r["Home Score"] + r["Away Score"] < float(row["Bet"].split()[1])):
                                bankroll += row["Bet Size"]*preBR*(row["Book Odds"] - 1)
                            else:
                                bankroll -= row["Bet Size"]*preBR
                    else:
                        if ("Over" in row["Bet"]):
                            if (r["Home Score"] + r["Away Score"] == float(row["Bet"].split()[1]) + 0.25):
                                bankroll += row["Bet Size"]*preBR*(row["Book Odds"] - 1)/2
                            elif (r["Home Score"] + r["Away Score"] > float(row["Bet"].split()[1])):
                                bankroll += row["Bet Size"]*preBR*(row["Book Odds"] - 1)
                            else:
                                bankroll -= row["Bet Size"]*preBR
                            if (r["Home Score"] + r["Away Score"] == float(row["Bet"].split()[1]) + 0.25):
                                bankroll -= row["Bet Size"]*preBR/2
                            elif (r["Home Score"] + r["Away Score"] < float(row["Bet"].split()[1])):
                                bankroll += row["Bet Size"]*preBR*(row["Book Odds"] - 1)
                            else:
                                bankroll -= row["Bet Size"]*preBR

print ("RETURN:", (bankroll/(30000*.86)) - 1)
print ("AVG BET SIZE:", np.average(betSizes))
