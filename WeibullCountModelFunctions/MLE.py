import pandas as pd
import numpy as np
import math
from logLikelihood import logLikelihood
from scipy.optimize import minimize
import time

#pass in the poissonPredictionMeans.csv dataframe
def MLE(df):
    start = time.perf_counter()
    init = [1.0308, 1.1188, 0.6489]
    results = minimize(logLikelihood, init, args=(df), method = "Nelder-Mead", options = {"disp":True})
    print (results)
    end = time.perf_counter()
    print ("TIME:", end - start)

pred = pd.read_csv('C:/Users/JackMitt/Documents/EPLBettingModel/SerieA_Csvs/poissonPredictionMeans.csv', encoding = "ISO-8859-1")
MLE(pred)
