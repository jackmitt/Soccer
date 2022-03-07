import pandas as pd
import numpy as np
import datetime
from WeibullCountModelFunctions.MLE import MLE
from WeibullCountModelFunctions.WeibullPMF import weibullPmf
from WeibullCountModelFunctions.frankCopula import copula


def WeibullCountDistPredictions(league):
    train = pd.read_csv("./csv_data/England1/train.csv", encoding = "ISO-8859-1")
    train = train[train["H_proj"].notna()]
    aggLeagues = ["England2","England3","England4"]
    for l in aggLeagues:
        new = pd.read_csv("./csv_data/" + l + "/train.csv", encoding = "ISO-8859-1")
        new = new[new["H_proj"].notna()]
        train = train.append(new, ignore_index = True)
    test = pd.read_csv("./csv_data/" + league + "/test.csv", encoding = "ISO-8859-1")
    test = test[test["H_proj"].notna()]
    test = test.reset_index(drop=True)
    games = len(train.index)
    dict = {}
    testCount = 0
    #[1.03212958 0.98436033 0.01603222] #OPTIMAL YESTERDAY
    #optimal = MLE(train)
    optimal = [1.0308, 0.98436033, 0.01603222]
    alphaDictH = {}
    alphaDictA = {}
    cur = 0
    while (cur < len(test.index)):
        hCdf = []
        aCdf = []
        for j in range(11):
            if (j == 0):
                hCdf.append(weibullPmf(j, test.at[cur, "H_proj"], optimal[0], alphaDictH))
                aCdf.append(weibullPmf(j, test.at[cur, "A_proj"], optimal[1], alphaDictA))
            else:
                hCdf.append(weibullPmf(j, test.at[cur, "H_proj"], optimal[0], alphaDictH) + hCdf[j-1])
                aCdf.append(weibullPmf(j, test.at[cur, "A_proj"], optimal[1], alphaDictA) + aCdf[j-1])
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

    pred = {"p_1":[],"p_X":[],"p_2":[],"p_Open_home_cover":[],"p_Close_home_cover":[],"p_Open_over":[],"p_Close_over":[]}
    for key in pred:
        for i in range(len(test.index)):
            pred[key].append(0)
    for index in range(len(test.index)):
        p_spaces = {"Open_cover":0,"Close_cover":0,"Open_over":0,"Close_over":0}
        for j in range(11):
            for k in range(11):
                if (j > k):
                    pred["p_1"][index] += dict[j][k][index]
                elif (k > j):
                    pred["p_2"][index] += dict[j][k][index]
                else:
                    pred["p_X"][index] += dict[j][k][index]

                for x in ["Open","Close"]:
                    if ("0.5" in str(test.at[index, x + " AH"])):
                        p_spaces[x + "_cover"] += dict[j][k][index]
                        if (j > k + test.at[index, x + " AH"]):
                            pred["p_" + x + "_home_cover"][index] += dict[j][k][index]
                    elif ("0.75" not in str(test.at[index, x + " AH"]) and "0.25" not in str(test.at[index, x + " AH"])):
                        if (j != k + test.at[index, x + " AH"]):
                            p_spaces[x + "_cover"] += dict[j][k][index]
                        if (j > k + test.at[index, x + " AH"]):
                            pred["p_" + x + "_home_cover"][index] += dict[j][k][index]
                    else:
                        parts = [test.at[index, x + " AH"] - 0.25,test.at[index, x + " AH"] + 0.25]
                        for part in parts:
                            if ("0.5" in str(part)):
                                p_spaces[x + "_cover"] += dict[j][k][index]
                                if (j > k + part):
                                    pred["p_" + x + "_home_cover"][index] += dict[j][k][index]
                            else:
                                if (j != k + part):
                                    p_spaces[x + "_cover"] += dict[j][k][index]
                                if (j > k + part):
                                    pred["p_" + x + "_home_cover"][index] += dict[j][k][index]

                    if ("0.5" in str(test.at[index, x + " OU"])):
                        p_spaces[x + "_over"] += dict[j][k][index]
                        if (j + k > test.at[index, x + " OU"]):
                            pred["p_" + x + "_over"][index] += dict[j][k][index]
                    elif ("0.75" not in str(test.at[index, x + " OU"]) and "0.25" not in str(test.at[index, x + " OU"])):
                        if (j + k != test.at[index, x + " OU"]):
                            p_spaces[x + "_over"] += dict[j][k][index]
                        if (j + k > test.at[index, x + " OU"]):
                            pred["p_" + x + "_over"][index] += dict[j][k][index]
                    else:
                        parts = [test.at[index, x + " OU"] - 0.25,test.at[index, x + " OU"] + 0.25]
                        for part in parts:
                            if ("0.5" in str(part)):
                                p_spaces[x + "_over"] += dict[j][k][index]
                                if (j + k > part):
                                    pred["p_" + x + "_over"][index] += dict[j][k][index]
                            else:
                                if (j + k != part):
                                    p_spaces[x + "_over"] += dict[j][k][index]
                                if (j + k > part):
                                    pred["p_" + x + "_over"][index] += dict[j][k][index]

        for x in ["Open","Close"]:
            pred["p_" + x + "_home_cover"][index] = pred["p_" + x + "_home_cover"][index] / p_spaces[x + "_cover"]
            pred["p_" + x + "_over"][index] = pred["p_" + x + "_over"][index] / p_spaces[x + "_over"]


    for key in pred:
        test[key] = pred[key]
    test.to_csv("./csv_data/" + league + "/predictions.csv", index = False)
