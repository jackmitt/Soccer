import pandas as pd
import numpy as np
import math
from WeibullPMF import weibullPmf
from frankCopula import copula

#logLikelihood function for ONE game
def logLikelihood(c1, c2, k, df):
    total = 0
    curIndex = 0
    while (curIndex < len(df.index)):
        print (curIndex)
        print (total)
        #print (copula(weibullPmf(df.at[curIndex, "Score"], l1, c1), weibullPmf(df.at[curIndex + 1, "Score"], l2, c2), k) - copula(weibullPmf(df.at[curIndex, "Score"] - 1, l1, c1), weibullPmf(df.at[curIndex + 1, "Score"], l2, c2), k) - copula(weibullPmf(df.at[curIndex, "Score"], l1, c1), weibullPmf(df.at[curIndex + 1, "Score"] - 1, l2, c2), k) + copula(weibullPmf(df.at[curIndex, "Score"] - 1, l1, c1), weibullPmf(df.at[curIndex + 1, "Score"] - 1, l2, c2), k))
        total += (np.log(copula(weibullPmf(df.at[curIndex, "Score"], df.at[curIndex, "Poisson Mean Prediction"], c1), weibullPmf(df.at[curIndex + 1, "Score"], df.at[curIndex + 1, "Poisson Mean Prediction"], c2), k) - copula(weibullPmf(df.at[curIndex, "Score"] - 1, df.at[curIndex, "Poisson Mean Prediction"], c1), weibullPmf(df.at[curIndex + 1, "Score"], df.at[curIndex + 1, "Poisson Mean Prediction"], c2), k) - copula(weibullPmf(df.at[curIndex, "Score"], df.at[curIndex, "Poisson Mean Prediction"], c1), weibullPmf(df.at[curIndex + 1, "Score"] - 1, df.at[curIndex + 1, "Poisson Mean Prediction"], c2), k) + copula(weibullPmf(df.at[curIndex, "Score"] - 1, df.at[curIndex, "Poisson Mean Prediction"], c1), weibullPmf(df.at[curIndex + 1, "Score"] - 1, df.at[curIndex + 1, "Poisson Mean Prediction"], c2), k)))
        curIndex += 2
    #return (np.log(copula(weibullPmf(y1, l1, c1), weibullPmf(y2, l2, c2), k) - copula(weibullPmf(y1 - 1, l1, c1), weibullPmf(y2, l2, c2), k) - copula(weibullPmf(y1, l1, c1), weibullPmf(y2 - 1, l2, c2), k) + copula(weibullPmf(y1 - 1, l1, c1), weibullPmf(y2 - 1, l2, c2), k)))
    return (-total)

pred = pd.read_csv('C:/Users/JackMitt/Documents/EPLBettingModel/SerieA_Csvs/poissonPredictionMeans.csv', encoding = "ISO-8859-1")
print (logLikelihood(1.05, 0.98, -0.45, pred))
