import pandas as pd
import numpy as np
import math
from WeibullCountModelFunctions.logLikelihood import logLikelihood
from scipy.optimize import minimize
import time

#pass in the poissonPredictionMeans.csv dataframe
def MLE(df):
    init = [1.13, 0.90, 0.14]
    results = minimize(logLikelihood, init, args=(df), method = "Nelder-Mead", options = {"disp":True})
    return (results.x)
