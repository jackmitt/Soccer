import pandas as pd
import numpy as np
import math
from WeibullCountModelFunctions.logLikelihood import logLikelihood
from scipy.optimize import minimize
import time

#pass in the poissonPredictionMeans.csv dataframe
def MLE(df):
    init = [1.000001, 1.000001, 0.001]
    results = minimize(logLikelihood, init, args=(df), method = "CG", options = {"disp":True,"maxiter":100})
    return (results.x)
