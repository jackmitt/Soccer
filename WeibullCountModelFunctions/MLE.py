import pandas as pd
import numpy as np
import math
from logLikelihood import logLikelihood
from scipy.optimize import minimize

#pass in the poissonPredictionMeans.csv dataframe
def MLE(df):
    print (minimize(logLikelihood, [1.05, 0.98, -0.45], args=(df), method = "Nelder-Mead", options = {"disp":True}))
