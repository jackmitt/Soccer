import pandas as pd
import numpy as np
from WeibullCountModelFunctions.MLE import MLE
from WeibullCountModelFunctions.WeibullPMF import weibullPmf
from WeibullCountModelFunctions.frankCopula import copula
from sklearn.utils import shuffle

pred = pd.read_csv('./EPL_Csvs/newvars_no_T/weibull_copula/WeibullFormat.csv', encoding = "ISO-8859-1")
pred = shuffle(pred, random_state = 43).reset_index(drop = True)

z = 10
games = len(pred.index)
dict = {}
testCount = 0
for i in range(z):
    inIndex = []
    for j in range(len(pred.index)):
        if (j not in range(int(i/z*games), int((i+1)/z*games))):
            inIndex.append(j)
    outS = pred[int(i/z*games):int((i+1)/z*games)].reset_index(drop=True)
    inS = pred.iloc[inIndex, :].reset_index(drop=True)
    optimal = MLE(inS)
    print(optimal)
    #optimal = [1.0308, 1.1188, 0.6489]
    alphaDictH = {}
    alphaDictA = {}
    cur = 0
    while (cur < len(outS.index)):
        hCdf = []
        aCdf = []
        for j in range(11):
            if (j == 0):
                hCdf.append(weibullPmf(j, outS.at[cur, "H_Poisson Mean Prediction"], optimal[0], alphaDictH))
                aCdf.append(weibullPmf(j, outS.at[cur, "A_Poisson Mean Prediction"], optimal[1], alphaDictA))
            else:
                hCdf.append(weibullPmf(j, outS.at[cur, "H_Poisson Mean Prediction"], optimal[0], alphaDictH) + hCdf[j-1])
                aCdf.append(weibullPmf(j, outS.at[cur, "A_Poisson Mean Prediction"], optimal[1], alphaDictA) + aCdf[j-1])
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

for j in range(11):
    for k in range(11):
        pred[str(j) + " -- " + str(k)] = dict[j][k]

pred.to_csv("./EPL_Csvs/newvars_No_T/weibull_copula/WeibullPredictions.csv")
