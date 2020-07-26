import pandas as pd
import numpy as np

pred = pd.read_csv('./bettingPredictions.csv', encoding = "ISO-8859-1")

#pred = pred.sample(frac=1).reset_index(drop=True)
bankroll = 30000
mloddsTaken = []
mlresults = []
ahoddsTaken = []
ahresults = []
ouoddsTaken = []
ouresults = []
ml = {"edge":0,"colName":"","netWin":0}
ah = {"edge":0,"colName":"","netWin":0}
ou = {"edge":0,"colName":"","netWin":0}
for index, row in pred.iterrows():
    print (index, ou["netWin"])
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
                mlresults.append(1)
            else:
                bankroll -= ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*preBR
                ml["netWin"] -= ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*30000
                mlresults.append(0)
        elif (ml["colName"] == "2"):
            if (row["Away Score"] > row["Home Score"]):
                bankroll += ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*preBR*(row[ml["colName"]] - 1)
                ml["netWin"] += ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*30000*(row[ml["colName"]] - 1)
                mlresults.append(1)
            else:
                bankroll -= ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*preBR
                ml["netWin"] -= ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*30000
                mlresults.append(0)
        else:
            if (row["Away Score"] == row["Home Score"]):
                bankroll += ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*preBR*(row[ml["colName"]] - 1)
                ml["netWin"] += ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*30000*(row[ml["colName"]] - 1)
                mlresults.append(1)
            else:
                bankroll -= ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*preBR
                ml["netWin"] -= ((row["P(" + ml["colName"] + ")"] - (1/row[ml["colName"]])) / (1-(1/row[ml["colName"]])))*30000
                mlresults.append(0)
    if (ah["edge"] > 0):
        ahoddsTaken.append(row[ah["colName"]])
        if (ah["colName"].split()[1].split(".")[1] != "25" and ah["colName"].split()[1].split(".")[1] != "75"):
            if ("(1)" in ah["colName"]):
                if (row["Away Score"] - row["Home Score"] < float(ah["colName"].split()[1])):
                    bankroll += ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR*(row[ah["colName"]] - 1)
                    ah["netWin"] += ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000*(row[ah["colName"]] - 1)
                    ahresults.append(1)
                elif (row["Away Score"] - row["Home Score"] > float(ah["colName"].split()[1])):
                    bankroll -= ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR
                    ah["netWin"] -= ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000
                    ahresults.append(0)
            else:
                if (row["Home Score"] - row["Away Score"] < 0-float(ah["colName"].split()[1])):
                    bankroll += ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR*(row[ah["colName"]] - 1)
                    ah["netWin"] += ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000*(row[ah["colName"]] - 1)
                    ahresults.append(1)
                elif (row["Home Score"] - row["Away Score"] > 0-float(ah["colName"].split()[1])):
                    bankroll -= ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR
                    ah["netWin"] -= ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000
                    ahresults.append(0)
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
                    ahresults.append(1)
                elif (row["Away Score"] - row["Home Score"] > float(ah["colName"].split()[1]) + toAdd):
                    bankroll -= ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR
                    ah["netWin"] -= ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000
                    ahresults.append(0)
                else:
                    if ((ah["colName"].split()[1][0] == "-" and ah["colName"].split()[1].split(".")[1] == "75") or (ah["colName"].split()[1][0] != "-" and ah["colName"].split()[1].split(".")[1] == "25")):
                        bankroll += (((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR*(row[ah["colName"]] - 1))/2
                        ah["netWin"] += (((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000*(row[ah["colName"]] - 1))/2
                    else:
                        bankroll -= (((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR)/2
                        ah["netWin"] -= (((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000)/2
            else:
                if (row["Home Score"] - row["Away Score"] < 0-float(ah["colName"].split()[1]) - toAdd):
                    bankroll += ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR*(row[ah["colName"]] - 1)
                    ah["netWin"] += ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000*(row[ah["colName"]] - 1)
                    ahresults.append(1)
                elif (row["Home Score"] - row["Away Score"] > 0-float(ah["colName"].split()[1]) - toAdd):
                    bankroll -= ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR
                    ah["netWin"] -= ((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000
                    ahresults.append(0)
                else:
                    if ((ah["colName"].split()[1][0] == "-" and ah["colName"].split()[1].split(".")[1] == "25") or (ah["colName"].split()[1][0] != "-" and ah["colName"].split()[1].split(".")[1] == "75")):
                        bankroll += (((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR*(row[ah["colName"]] - 1))/2
                        ah["netWin"] += (((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000*(row[ah["colName"]] - 1))/2
                    else:
                        bankroll -= (((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*preBR)/2
                        ah["netWin"] -= (((row["P(" + ah["colName"] + ")"] - (1/row[ah["colName"]])) / (1-(1/row[ah["colName"]])))*30000)/2
    if (ou["edge"] > 0):
        print (ou["colName"], row["Home Score"], row["Away Score"], ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]]))))
        ouoddsTaken.append(row[ou["colName"]])
        if (ou["colName"].split()[1].split(".")[1] != "25" and ou["colName"].split()[1].split(".")[1] != "75"):
            if ("Over" in ou["colName"]):
                if (row["Home Score"] + row["Away Score"] > float(ou["colName"].split()[1])):
                    bankroll += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR*(row[ou["colName"]] - 1)
                    ou["netWin"] += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000*(row[ou["colName"]] - 1)
                    ouresults.append(1)
                elif (row["Home Score"] + row["Away Score"] < float(ou["colName"].split()[1])):
                    bankroll -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR
                    ou["netWin"] -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000
                    ouresults.append(0)
            else:
                if (row["Home Score"] + row["Away Score"] < float(ou["colName"].split()[1])):
                    bankroll += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR*(row[ou["colName"]] - 1)
                    ou["netWin"] += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000*(row[ou["colName"]] - 1)
                    ouresults.append(1)
                elif (row["Home Score"] + row["Away Score"] > float(ou["colName"].split()[1])):
                    bankroll -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR
                    ou["netWin"] -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000
                    ouresults.append(0)
        elif (ou["colName"].split()[1].split(".")[1] == "25"):
            if ("Over" in ou["colName"]):
                if (row["Home Score"] + row["Away Score"] == float(ou["colName"].split()[1]) - 0.25):
                    bankroll -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR/2
                    ou["netWin"] -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000/2
                elif (row["Home Score"] + row["Away Score"] > float(ou["colName"].split()[1])):
                    bankroll += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR*(row[ou["colName"]] - 1)
                    ou["netWin"] += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000*(row[ou["colName"]] - 1)
                    ouresults.append(1)
                else:
                    bankroll -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR
                    ou["netWin"] -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000
                    ouresults.append(0)
            else:
                if (row["Home Score"] + row["Away Score"] == float(ou["colName"].split()[1]) - 0.25):
                    bankroll += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR*(row[ou["colName"]] - 1)/2
                    ou["netWin"] += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000*(row[ou["colName"]] - 1)/2
                elif (row["Home Score"] + row["Away Score"] < float(ou["colName"].split()[1])):
                    bankroll += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR*(row[ou["colName"]] - 1)
                    ou["netWin"] += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000*(row[ou["colName"]] - 1)
                    ouresults.append(1)
                else:
                    bankroll -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR
                    ou["netWin"] -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000
                    ouresults.append(0)
        else:
            if ("Over" in ou["colName"]):
                if (row["Home Score"] + row["Away Score"] == float(ou["colName"].split()[1]) + 0.25):
                    bankroll += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR*(row[ou["colName"]] - 1)/2
                    ou["netWin"] += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000*(row[ou["colName"]] - 1)/2
                elif (row["Home Score"] + row["Away Score"] > float(ou["colName"].split()[1])):
                    bankroll += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR*(row[ou["colName"]] - 1)
                    ou["netWin"] += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000*(row[ou["colName"]] - 1)
                    ouresults.append(1)
                else:
                    bankroll -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR
                    ou["netWin"] -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000
                    ouresults.append(0)
            else:
                if (row["Home Score"] + row["Away Score"] == float(ou["colName"].split()[1]) + 0.25):
                    bankroll -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR/2
                    ou["netWin"] -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000/2
                elif (row["Home Score"] + row["Away Score"] < float(ou["colName"].split()[1])):
                    bankroll += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR*(row[ou["colName"]] - 1)
                    ou["netWin"] += ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000*(row[ou["colName"]] - 1)
                    ouresults.append(1)
                else:
                    bankroll -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*preBR
                    ou["netWin"] -= ((row["P(" + ou["colName"] + ")"] - (1/row[ou["colName"]])) / (1-(1/row[ou["colName"]])))*30000
                    ouresults.append(0)
    #print (bankroll, ml["netWin"])
print ("------------------------")
print ("Final Bankroll:", bankroll)
print ("ML Odds Taken:", 1/np.average(mloddsTaken))
print ("ML Results:", np.average(mlresults))
print ("ML Net Win:", ml["netWin"])
print ("AH Odds Taken:", 1/np.average(ahoddsTaken))
print ("AH Results:", np.average(ahresults))
print ("AH Net Win:", ah["netWin"])
print ("OU Odds Taken:", 1/np.average(ouoddsTaken))
print ("OU Results:",np.average(ouresults))
print ("OU Net Win:", ou["netWin"])
