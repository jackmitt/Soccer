import pandas as pd
import numpy as np

pred = pd.read_csv('./EPL_Csvs/no_T_Vars/weibull_copula/bettingPredictionsTest.csv', encoding = "ISO-8859-1")
mlDict = {"Book Prob":[],"Edge":[],"Result":[],"P":[]}
ahDict = {"Book Prob":[],"Edge":[],"Result":[],"P":[]}
ouDict = {"Book Prob":[],"Edge":[],"Result":[],"P":[]}
print(pred)
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
    preBR = bankroll
    if (ml["edge"] > 0):
        mloddsTaken.append(row[ml["colName"]])
        if (ml["colName"] == "1"):
            if (row["Home Score"] > row["Away Score"]):
                bankroll += ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*preBR*(row[ml["colName"]] - 1)
                ml["netWin"] += ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*30000*(row[ml["colName"]] - 1)
                ml["netWinFixed"] += 300*(row[ml["colName"]] - 1)
                mlresults.append(1)
                mlDict["Result"].append(1)
                mlDict["Book Prob"].append(1/row[ml["colName"]])
                mlDict["Edge"].append(ml["edge"])
                mlDict["P"].append(1/row[ml["colName"]] + ml["edge"])
            else:
                bankroll -= ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*preBR
                ml["netWin"] -= ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*30000
                ml["netWinFixed"] -= 300
                mlresults.append(0)
                mlDict["Result"].append(0)
                mlDict["Book Prob"].append(1/row[ml["colName"]])
                mlDict["Edge"].append(ml["edge"])
                mlDict["P"].append(1/row[ml["colName"]] + ml["edge"])
        elif (ml["colName"] == "2"):
            if (row["Away Score"] > row["Home Score"]):
                bankroll += ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*preBR*(row[ml["colName"]] - 1)
                ml["netWin"] += ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*30000*(row[ml["colName"]] - 1)
                ml["netWinFixed"] += 300*(row[ml["colName"]] - 1)
                mlresults.append(1)
                mlDict["Result"].append(1)
                mlDict["Book Prob"].append(1/row[ml["colName"]])
                mlDict["Edge"].append(ml["edge"])
                mlDict["P"].append(1/row[ml["colName"]] + ml["edge"])
            else:
                bankroll -= ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*preBR
                ml["netWin"] -= ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*30000
                ml["netWinFixed"] -= 300
                mlresults.append(0)
                mlDict["Result"].append(0)
                mlDict["Book Prob"].append(1/row[ml["colName"]])
                mlDict["Edge"].append(ml["edge"])
                mlDict["P"].append(1/row[ml["colName"]] + ml["edge"])
        else:
            if (row["Away Score"] == row["Home Score"]):
                bankroll += ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*preBR*(row[ml["colName"]] - 1)
                ml["netWin"] += ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*30000*(row[ml["colName"]] - 1)
                ml["netWinFixed"] += 300*(row[ml["colName"]] - 1)
                mlresults.append(1)
                mlDict["Result"].append(1)
                mlDict["Book Prob"].append(1/row[ml["colName"]])
                mlDict["Edge"].append(ml["edge"])
                mlDict["P"].append(1/row[ml["colName"]] + ml["edge"])
            else:
                bankroll -= ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*preBR
                ml["netWin"] -= ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*30000
                ml["netWinFixed"] -= 300
                mlresults.append(0)
                mlDict["Result"].append(0)
                mlDict["Book Prob"].append(1/row[ml["colName"]])
                mlDict["Edge"].append(ml["edge"])
                mlDict["P"].append(1/row[ml["colName"]] + ml["edge"])
    if (ah["edge"] > 0 and ah["edge"]):
        ahoddsTaken.append(row[ah["colName"]])
        if (ah["colName"].split()[1].split(".")[1] != "25" and ah["colName"].split()[1].split(".")[1] != "75"):
            if ("(1)" in ah["colName"]):
                if (row["Away Score"] - row["Home Score"] < float(ah["colName"].split()[1])):
                    bankroll += ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR*(row[ah["colName"]] - 1)
                    ah["netWin"] += ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000*(row[ah["colName"]] - 1)
                    ah["netWinFixed"] += 300*(row[ah["colName"]] - 1)
                    ahresults.append(1)
                    ahDict["Result"].append(1)
                    ahDict["Book Prob"].append(1/row[ah["colName"]])
                    ahDict["Edge"].append(ah["edge"])
                    ahDict["P"].append(1/row[ah["colName"]] + ah["edge"])
                    resultsByEdge[int(ah["edge"]*100/5)].append(1)
                    try:
                        resultsByKK[int(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*50)].append(1)
                    except:
                        resultsByKK[19].append(1)
                elif (row["Away Score"] - row["Home Score"] > float(ah["colName"].split()[1])):
                    bankroll -= ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR
                    ah["netWin"] -= ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000
                    ah["netWinFixed"] -= 300
                    ahresults.append(0)
                    ahDict["Result"].append(0)
                    ahDict["Book Prob"].append(1/row[ah["colName"]])
                    ahDict["Edge"].append(ah["edge"])
                    ahDict["P"].append(1/row[ah["colName"]] + ah["edge"])
                    resultsByEdge[int(ah["edge"]*100/5)].append(0)
                    try:
                        resultsByKK[int(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*50)].append(0)
                    except:
                        resultsByKK[19].append(0)
            else:
                if (row["Home Score"] - row["Away Score"] < 0-float(ah["colName"].split()[1])):
                    bankroll += ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR*(row[ah["colName"]] - 1)
                    ah["netWin"] += ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000*(row[ah["colName"]] - 1)
                    ah["netWinFixed"] += 300*(row[ah["colName"]] - 1)
                    ahresults.append(1)
                    ahDict["Result"].append(1)
                    ahDict["Book Prob"].append(1/row[ah["colName"]])
                    ahDict["Edge"].append(ah["edge"])
                    ahDict["P"].append(1/row[ah["colName"]] + ah["edge"])
                    resultsByEdge[int(ah["edge"]*100/5)].append(1)
                    try:
                        resultsByKK[int(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*50)].append(1)
                    except:
                        resultsByKK[19].append(1)
                elif (row["Home Score"] - row["Away Score"] > 0-float(ah["colName"].split()[1])):
                    bankroll -= ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR
                    ah["netWin"] -= ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000
                    ah["netWinFixed"] -= 300
                    ahresults.append(0)
                    ahDict["Result"].append(0)
                    ahDict["Book Prob"].append(1/row[ah["colName"]])
                    ahDict["Edge"].append(ah["edge"])
                    ahDict["P"].append(1/row[ah["colName"]] + ah["edge"])
                    resultsByEdge[int(ah["edge"]*100/5)].append(0)
                    try:
                        resultsByKK[int(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*50)].append(0)
                    except:
                        resultsByKK[19].append(0)
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
                    ahDict["Edge"].append(ah["edge"])
                    ahDict["P"].append(1/row[ah["colName"]] + ah["edge"])
                    resultsByEdge[int(ah["edge"]*100/5)].append(1)
                    try:
                        resultsByKK[int(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*50)].append(1)
                    except:
                        resultsByKK[19].append(1)
                elif (row["Away Score"] - row["Home Score"] > float(ah["colName"].split()[1]) + toAdd):
                    bankroll -= ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR
                    ah["netWin"] -= ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000
                    ah["netWinFixed"] -= 300
                    ahresults.append(0)
                    ahDict["Result"].append(0)
                    ahDict["Book Prob"].append(1/row[ah["colName"]])
                    ahDict["Edge"].append(ah["edge"])
                    ahDict["P"].append(1/row[ah["colName"]] + ah["edge"])
                    resultsByEdge[int(ah["edge"]*100/5)].append(0)
                    try:
                        resultsByKK[int(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*50)].append(0)
                    except:
                        resultsByKK[19].append(0)
                else:
                    if ((ah["colName"].split()[1][0] == "-" and ah["colName"].split()[1].split(".")[1] == "75") or (ah["colName"].split()[1][0] != "-" and ah["colName"].split()[1].split(".")[1] == "25")):
                        bankroll += (((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR*(row[ah["colName"]] - 1))/2
                        ah["netWin"] += (((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000*(row[ah["colName"]] - 1))/2
                        ah["netWinFixed"] += 300*(row[ah["colName"]] - 1)/2
                        ahresults.append(1)
                        ahDict["Result"].append(1)
                        ahDict["Book Prob"].append(1/row[ah["colName"]])
                        ahDict["Edge"].append(ah["edge"])
                        ahDict["P"].append(1/row[ah["colName"]] + ah["edge"])
                        resultsByEdge[int(ah["edge"]*100/5)].append(1)
                        try:
                            resultsByKK[int(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*50)].append(1)
                        except:
                            resultsByKK[19].append(1)
                    else:
                        bankroll -= (((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR)/2
                        ah["netWin"] -= (((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000)/2
                        ah["netWinFixed"] -= 300/2
                        ahresults.append(0)
                        ahDict["Result"].append(0)
                        ahDict["Book Prob"].append(1/row[ah["colName"]])
                        ahDict["Edge"].append(ah["edge"])
                        ahDict["P"].append(1/row[ah["colName"]] + ah["edge"])
                        resultsByEdge[int(ah["edge"]*100/5)].append(0)
                        try:
                            resultsByKK[int(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*50)].append(0)
                        except:
                            resultsByKK[19].append(0)
            else:
                if (row["Home Score"] - row["Away Score"] < 0-float(ah["colName"].split()[1]) - toAdd):
                    bankroll += ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR*(row[ah["colName"]] - 1)
                    ah["netWin"] += ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000*(row[ah["colName"]] - 1)
                    ah["netWinFixed"] += 300*(row[ah["colName"]] - 1)
                    ahresults.append(1)
                    ahDict["Result"].append(1)
                    ahDict["Book Prob"].append(1/row[ah["colName"]])
                    ahDict["Edge"].append(ah["edge"])
                    ahDict["P"].append(1/row[ah["colName"]] + ah["edge"])
                    resultsByEdge[int(ah["edge"]*100/5)].append(1)
                    try:
                        resultsByKK[int(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*50)].append(1)
                    except:
                        resultsByKK[19].append(1)
                elif (row["Home Score"] - row["Away Score"] > 0-float(ah["colName"].split()[1]) - toAdd):
                    bankroll -= ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR
                    ah["netWin"] -= ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000
                    ah["netWinFixed"] -= 300
                    ahresults.append(0)
                    ahDict["Result"].append(0)
                    ahDict["Book Prob"].append(1/row[ah["colName"]])
                    ahDict["Edge"].append(ah["edge"])
                    ahDict["P"].append(1/row[ah["colName"]] + ah["edge"])
                    resultsByEdge[int(ah["edge"]*100/5)].append(0)
                    try:
                        resultsByKK[int(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*50)].append(0)
                    except:
                        resultsByKK[19].append(0)
                else:
                    if ((ah["colName"].split()[1][0] == "-" and ah["colName"].split()[1].split(".")[1] == "25") or (ah["colName"].split()[1][0] != "-" and ah["colName"].split()[1].split(".")[1] == "75")):
                        bankroll += (((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR*(row[ah["colName"]] - 1))/2
                        ah["netWin"] += (((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000*(row[ah["colName"]] - 1))/2
                        ah["netWinFixed"] += 300*(row[ah["colName"]] - 1)/2
                        ahresults.append(1)
                        ahDict["Result"].append(1)
                        ahDict["Book Prob"].append(1/row[ah["colName"]])
                        ahDict["Edge"].append(ah["edge"])
                        ahDict["P"].append(1/row[ah["colName"]] + ah["edge"])
                        resultsByEdge[int(ah["edge"]*100/5)].append(1)
                        try:
                            resultsByKK[int(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*50)].append(1)
                        except:
                            resultsByKK[19].append(1)
                    else:
                        bankroll -= (((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR)/2
                        ah["netWin"] -= (((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000)/2
                        ah["netWinFixed"] -= 300/2
                        ahresults.append(0)
                        ahDict["Result"].append(0)
                        ahDict["Book Prob"].append(1/row[ah["colName"]])
                        ahDict["Edge"].append(ah["edge"])
                        ahDict["P"].append(1/row[ah["colName"]] + ah["edge"])
                        resultsByEdge[int(ah["edge"]*100/5)].append(0)
                        try:
                            resultsByKK[int(((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*50)].append(0)
                        except:
                            resultsByKK[19].append(0)
    if (ou["edge"] > 0 and ou["edge"]):
        ouoddsTaken.append(row[ou["colName"]])
        if (ou["colName"].split()[1].split(".")[1] != "25" and ou["colName"].split()[1].split(".")[1] != "75"):
            if ("Over" in ou["colName"]):
                if (row["Home Score"] + row["Away Score"] > float(ou["colName"].split()[1])):
                    bankroll += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR*(row[ou["colName"]] - 1)
                    ou["netWin"] += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000*(row[ou["colName"]] - 1)
                    ou["netWinFixed"] += 300*(row[ou["colName"]] - 1)
                    ouresults.append(1)
                    ouDict["Result"].append(1)
                    ouDict["Book Prob"].append(1/row[ou["colName"]])
                    ouDict["Edge"].append(ou["edge"])
                    ouDict["P"].append(1/row[ou["colName"]] + ou["edge"])
                    try:
                        ouresultsByKK[int(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*50)].append(1)
                    except:
                        ouresultsByKK[19].append(1)
                elif (row["Home Score"] + row["Away Score"] < float(ou["colName"].split()[1])):
                    bankroll -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR
                    ou["netWin"] -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000
                    ou["netWinFixed"] -= 300
                    ouresults.append(0)
                    ouDict["Result"].append(0)
                    ouDict["Book Prob"].append(1/row[ou["colName"]])
                    ouDict["Edge"].append(ou["edge"])
                    ouDict["P"].append(1/row[ou["colName"]] + ou["edge"])
            else:
                if (row["Home Score"] + row["Away Score"] < float(ou["colName"].split()[1])):
                    bankroll += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR*(row[ou["colName"]] - 1)
                    ou["netWin"] += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000*(row[ou["colName"]] - 1)
                    ou["netWinFixed"] += 300*(row[ou["colName"]] - 1)
                    ouresults.append(1)
                    ouDict["Result"].append(1)
                    ouDict["Book Prob"].append(1/row[ou["colName"]])
                    ouDict["Edge"].append(ou["edge"])
                    ouDict["P"].append(1/row[ou["colName"]] + ou["edge"])
                    try:
                        ouresultsByKK[int(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*50)].append(1)
                    except:
                        ouresultsByKK[19].append(1)
                elif (row["Home Score"] + row["Away Score"] > float(ou["colName"].split()[1])):
                    bankroll -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR
                    ou["netWin"] -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000
                    ou["netWinFixed"] -= 300
                    ouresults.append(0)
                    ouDict["Result"].append(0)
                    ouDict["Book Prob"].append(1/row[ou["colName"]])
                    ouDict["Edge"].append(ou["edge"])
                    ouDict["P"].append(1/row[ou["colName"]] + ou["edge"])
        elif (ou["colName"].split()[1].split(".")[1] == "25"):
            if ("Over" in ou["colName"]):
                if (row["Home Score"] + row["Away Score"] == float(ou["colName"].split()[1]) - 0.25):
                    bankroll -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR/2
                    ou["netWin"] -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000/2
                    ou["netWinFixed"] -= 300/2
                    ouresults.append(0)
                    ouDict["Result"].append(0)
                    ouDict["Book Prob"].append(1/row[ou["colName"]])
                    ouDict["Edge"].append(ou["edge"])
                    ouDict["P"].append(1/row[ou["colName"]] + ou["edge"])
                    try:
                        ouresultsByKK[int(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*50)].append(0)
                    except:
                        ouresultsByKK[19].append(0)
                elif (row["Home Score"] + row["Away Score"] > float(ou["colName"].split()[1])):
                    bankroll += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR*(row[ou["colName"]] - 1)
                    ou["netWin"] += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000*(row[ou["colName"]] - 1)
                    ou["netWinFixed"] += 300*(row[ou["colName"]] - 1)
                    ouresults.append(1)
                    ouDict["Result"].append(1)
                    ouDict["Book Prob"].append(1/row[ou["colName"]])
                    ouDict["Edge"].append(ou["edge"])
                    ouDict["P"].append(1/row[ou["colName"]] + ou["edge"])
                    try:
                        ouresultsByKK[int(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*50)].append(1)
                    except:
                        ouresultsByKK[19].append(1)
                else:
                    bankroll -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR
                    ou["netWin"] -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000
                    ou["netWinFixed"] -= 300
                    ouresults.append(0)
                    ouDict["Result"].append(0)
                    ouDict["Book Prob"].append(1/row[ou["colName"]])
                    ouDict["Edge"].append(ou["edge"])
                    ouDict["P"].append(1/row[ou["colName"]] + ou["edge"])
                    try:
                        ouresultsByKK[int(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*50)].append(0)
                    except:
                        ouresultsByKK[19].append(0)
            else:
                if (row["Home Score"] + row["Away Score"] == float(ou["colName"].split()[1]) - 0.25):
                    bankroll += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR*(row[ou["colName"]] - 1)/2
                    ou["netWin"] += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000*(row[ou["colName"]] - 1)/2
                    ou["netWinFixed"] += 300*(row[ou["colName"]] - 1)/2
                    ouresults.append(1)
                    ouDict["Result"].append(1)
                    ouDict["Book Prob"].append(1/row[ou["colName"]])
                    ouDict["Edge"].append(ou["edge"])
                    ouDict["P"].append(1/row[ou["colName"]] + ou["edge"])
                    try:
                        ouresultsByKK[int(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*50)].append(1)
                    except:
                        ouresultsByKK[19].append(1)
                elif (row["Home Score"] + row["Away Score"] < float(ou["colName"].split()[1])):
                    bankroll += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR*(row[ou["colName"]] - 1)
                    ou["netWin"] += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000*(row[ou["colName"]] - 1)
                    ou["netWinFixed"] += 300*(row[ou["colName"]] - 1)
                    ouresults.append(1)
                    ouDict["Result"].append(1)
                    ouDict["Book Prob"].append(1/row[ou["colName"]])
                    ouDict["Edge"].append(ou["edge"])
                    ouDict["P"].append(1/row[ou["colName"]] + ou["edge"])
                    try:
                        ouresultsByKK[int(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*50)].append(1)
                    except:
                        ouresultsByKK[19].append(1)
                else:
                    bankroll -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR
                    ou["netWin"] -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000
                    ou["netWinFixed"] -= 300
                    ouresults.append(0)
                    ouDict["Result"].append(0)
                    ouDict["Book Prob"].append(1/row[ou["colName"]])
                    ouDict["Edge"].append(ou["edge"])
                    ouDict["P"].append(1/row[ou["colName"]] + ou["edge"])
                    try:
                        ouresultsByKK[int(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*50)].append(0)
                    except:
                        ouresultsByKK[19].append(0)
        else:
            if ("Over" in ou["colName"]):
                if (row["Home Score"] + row["Away Score"] == float(ou["colName"].split()[1]) + 0.25):
                    bankroll += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR*(row[ou["colName"]] - 1)/2
                    ou["netWin"] += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000*(row[ou["colName"]] - 1)/2
                    ou["netWinFixed"] += 300*(row[ou["colName"]] - 1)/2
                    ouresults.append(1)
                    ouDict["Result"].append(1)
                    ouDict["Book Prob"].append(1/row[ou["colName"]])
                    ouDict["Edge"].append(ou["edge"])
                    ouDict["P"].append(1/row[ou["colName"]] + ou["edge"])
                    try:
                        ouresultsByKK[int(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*50)].append(1)
                    except:
                        ouresultsByKK[19].append(1)
                elif (row["Home Score"] + row["Away Score"] > float(ou["colName"].split()[1])):
                    bankroll += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR*(row[ou["colName"]] - 1)
                    ou["netWin"] += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000*(row[ou["colName"]] - 1)
                    ou["netWinFixed"] += 300*(row[ou["colName"]] - 1)
                    ouresults.append(1)
                    ouDict["Result"].append(1)
                    ouDict["Book Prob"].append(1/row[ou["colName"]])
                    ouDict["Edge"].append(ou["edge"])
                    ouDict["P"].append(1/row[ou["colName"]] + ou["edge"])
                    try:
                        ouresultsByKK[int(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*50)].append(1)
                    except:
                        ouresultsByKK[19].append(1)
                else:
                    bankroll -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR
                    ou["netWin"] -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000
                    ou["netWinFixed"] -= 300
                    ouresults.append(0)
                    ouDict["Result"].append(0)
                    ouDict["Book Prob"].append(1/row[ou["colName"]])
                    ouDict["Edge"].append(ou["edge"])
                    ouDict["P"].append(1/row[ou["colName"]] + ou["edge"])
                    try:
                        ouresultsByKK[int(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*50)].append(0)
                    except:
                        ouresultsByKK[19].append(0)
            else:
                if (row["Home Score"] + row["Away Score"] == float(ou["colName"].split()[1]) + 0.25):
                    bankroll -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR/2
                    ou["netWin"] -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000/2
                    ou["netWinFixed"] -= 300/2
                    ouresults.append(0)
                    ouDict["Result"].append(0)
                    ouDict["Book Prob"].append(1/row[ou["colName"]])
                    ouDict["Edge"].append(ou["edge"])
                    ouDict["P"].append(1/row[ou["colName"]] + ou["edge"])
                    try:
                        ouresultsByKK[int(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*50)].append(0)
                    except:
                        ouresultsByKK[19].append(0)
                elif (row["Home Score"] + row["Away Score"] < float(ou["colName"].split()[1])):
                    bankroll += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR*(row[ou["colName"]] - 1)
                    ou["netWin"] += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000*(row[ou["colName"]] - 1)
                    ou["netWinFixed"] += 300*(row[ou["colName"]] - 1)
                    ouresults.append(1)
                    ouDict["Result"].append(1)
                    ouDict["Book Prob"].append(1/row[ou["colName"]])
                    ouDict["Edge"].append(ou["edge"])
                    ouDict["P"].append(1/row[ou["colName"]] + ou["edge"])
                    try:
                        ouresultsByKK[int(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*50)].append(1)
                    except:
                        ouresultsByKK[19].append(1)
                else:
                    bankroll -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR
                    ou["netWin"] -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000
                    ou["netWinFixed"] -= 300
                    ouresults.append(0)
                    ouDict["Result"].append(0)
                    ouDict["Book Prob"].append(1/row[ou["colName"]])
                    ouDict["Edge"].append(ou["edge"])
                    ouDict["P"].append(1/row[ou["colName"]] + ou["edge"])
                    try:
                        ouresultsByKK[int(((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*50)].append(0)
                    except:
                        ouresultsByKK[19].append(0)
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
# for i in range(20):
#     print (i, np.average(resultsByEdge[i]), len(resultsByEdge[i]))
# for i in range(20):
#     print (i, np.average(resultsByKK[i]), len(resultsByKK[i]))
# for i in range(20):
#     print (i, np.average(resultsByKK[i]), len(resultsByKK[i]))
# dfFinal = pd.DataFrame.from_dict(mlDict)
# dfFinal.to_csv("./SerieA_Csvs/newvars_only_T_E_Vars/weibull_copula/mlResultsByEdge.csv")
# dfFinal = pd.DataFrame.from_dict(ahDict)
# dfFinal.to_csv("./SerieA_Csvs/newvars_only_T_E_Vars/weibull_copula/ahResultsByEdge.csv")
# dfFinal = pd.DataFrame.from_dict(ouDict)
# dfFinal.to_csv("./SerieA_Csvs/newvars_only_T_E_Vars/weibull_copula/ouResultsByEdge.csv")
