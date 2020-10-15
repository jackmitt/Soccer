import pandas as pd
import numpy as np
from simultaneousDependentKelly import gradient_ascent

pred = pd.read_csv('./EPL_Csvs/3Game_newvars_no_T/bettingPredictions3Games.csv', encoding = "ISO-8859-1")
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
    print (key, len(pred.index), len(mlDict[key]), len(ahDict[key]), len(ouDict[key]))
for key in mlDict:
    print (key, len(pred.index), len(mlDict[key]), len(ahDict[key]), len(ouDict[key]))
    pred["ML " + key] = mlDict[key]
    pred["AH " + key] = ahDict[key]
    pred["OU " + key] = ouDict[key]

# betTypes = ["ML ", "AH ", "OU "]
# sizeDict = {"ML Bet Size":[], "AH Bet Size":[], "OU Bet Size":[]}
# mlBetSizes = []
#
# for i, row in pred.iterrows():
#     print (i)
#     print (len(sizeDict["ML Bet Size"]), len(sizeDict["AH Bet Size"]), len(sizeDict["OU Bet Size"]))
#     bn = []
#     pt = [[],[],[],[],[],[],[],[],[],[],[]]
#     pb = []
#     kelly = []
#     for j in range(11):
#         for k in range(11):
#             pt[j].append(pred.at[i, str(j) + " -- " + str(k)])
#     for t in betTypes:
#         if (not np.isnan(pred.at[i, t + "Book Prob"])):
#             bn.append(pred.at[i, t + "Bet"])
#             pb.append(pred.at[i, t + "Book Prob"])
#             kelly.append((pred.at[i, t + "P"] - pred.at[i, t + "Book Prob"]) / (1-(pred.at[i, t + "Book Prob"])))
#     adjWagers = gradient_ascent(bn, pt, pb, kelly)
#     wC = 0
#     for t in betTypes:
#         if (np.isnan(pred.at[i, t + "Book Prob"])):
#             sizeDict[t + "Bet Size"].append(np.nan)
#         else:
#             sizeDict[t + "Bet Size"].append(adjWagers[wC])
#             wC += 1
#
# for key in sizeDict:
#     pred[key] = sizeDict[key]

mlAdj = []
ahAdj = []
ouAdj = []
betTypes = ["ML ", "AH ", "OU "]
for index, row in pred.iterrows():
    print (index)
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
    #ML adj weight = (P(ML) + P(ML^c INTERSECT AH) + P(ML^c INTERSECT OU))/(P(ML) + P(AH) + P(OU))
    temp1 = 0
    temp2 = 0
    for score in list(set(td["ML Fail"]) & set(td["AH Success"])):
        temp1 += row[score]
    for score in list(set(td["ML Fail"]) & set(td["OU Success"])):
        temp2 += row[score]
    mlAdj.append(row["ML Kelly"] * (td["ML P"] + temp1 + temp2)/div)
    temp1 = 0
    temp2 = 0
    for score in list(set(td["AH Fail"]) & set(td["ML Success"])):
        temp1 += row[score]
    for score in list(set(td["AH Fail"]) & set(td["OU Success"])):
        temp2 += row[score]
    ahAdj.append(row["AH Kelly"] * (td["AH P"] + temp1 + temp2)/div)
    temp1 = 0
    temp2 = 0
    for score in list(set(td["OU Fail"]) & set(td["AH Success"])):
        temp1 += row[score]
    for score in list(set(td["OU Fail"]) & set(td["ML Success"])):
        temp2 += row[score]
    ouAdj.append(row["OU Kelly"] * (td["OU P"] + temp1 + temp2)/div)

pred["ML Adj Kelly"] = mlAdj
pred["AH Adj Kelly"] = ahAdj
pred["OU Adj Kelly"] = ouAdj
pred.to_csv("./EPL_Csvs/3Game_newvars_no_T/resultsByEdge3Games.csv")
