import pandas as pd
import numpy as np
from WeibullCountModelFunctions.MLE import MLE
from WeibullCountModelFunctions.WeibullPMF import weibullPmf
from WeibullCountModelFunctions.frankCopula import copula
from sklearn.utils import shuffle

pred = pd.read_csv('C:/Users/JackMitt/Documents/EPLBettingModel/EPL_Csvs/no_T_Vars/poissonPredictionMeansTestSplit.csv', encoding = "ISO-8859-1")
print (pred)

newDict = {}
sides = ["H_", "A_"]
for col in pred.columns:
    for side in sides:
        newDict[side + col] = []
cur = 0
while (cur < len(pred.index)):
    for col in pred.columns:
        newDict["H_" + col].append(pred.at[cur, col])
        newDict["A_" + col].append(pred.at[cur+1,col])
    cur += 2


dfFinal = pd.DataFrame.from_dict(newDict)
print (dfFinal)
#Added for train test split - eliminate extrapolated shit
droprows = []
for index, row in dfFinal.iterrows():
    if (row["H_Poisson Mean Prediction"] > 5 or row["A_Poisson Mean Prediction"] > 5):
        droprows.append(index)
dfFinal = dfFinal.drop(droprows)
dfFinal.to_csv("./EPL_Csvs/no_T_Vars/weibull_copula/WeibullFormatTestSplit.csv")
