import pandas as pd
import numpy as np
import math
from WeibullCountModelFunctions.WeibullPMF import weibullPmf
from WeibullCountModelFunctions.frankCopula import copula
import time

#logLikelihood function for ONE game
def logLikelihood(array, df):
    total = 0
    curIndex = 0
    alphaDict = {}
    while (curIndex < len(df.index)):
        #print (curIndex)
        #CDF from Weibull PMF
        F11 = 0
        for i in range(df.at[curIndex, "H_Score"] + 1):
            if (i == df.at[curIndex, "H_Score"]):
                if (i == 0):
                    F12 = 0
                else:
                    F12 = F11
            F11 += weibullPmf(i, df.at[curIndex, "H_Poisson Mean Prediction"], array[0], alphaDict)
        F21 = 0
        for i in range(df.at[curIndex, "A_Score"] + 1):
            if (i == df.at[curIndex, "A_Score"]):
                if (i == 0):
                    F22 = 0
                else:
                    F22 = F21
            F21 += weibullPmf(i, df.at[curIndex, "A_Poisson Mean Prediction"], array[1], alphaDict)
        total += (np.log(copula(F11, F21, array[2]) - copula(F12, F21, array[2]) - copula(F11, F22, array[2]) + copula(F12, F22, array[2])))
        curIndex += 1
    #return (np.log(copula(weibullPmf(y1, l1, c1), weibullPmf(y2, l2, c2), k) - copula(weibullPmf(y1 - 1, l1, c1), weibullPmf(y2, l2, c2), k) - copula(weibullPmf(y1, l1, c1), weibullPmf(y2 - 1, l2, c2), k) + copula(weibullPmf(y1 - 1, l1, c1), weibullPmf(y2 - 1, l2, c2), k)))
    return (-total)
