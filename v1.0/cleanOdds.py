import pandas as pd
import numpy as np


pred = pd.read_csv('./EPL_Csvs/3Game_newvars_no_T/bettingPredictions3Games.csv', encoding = "ISO-8859-1")

for index, row in pred.iterrows():
    dict = {"ah":[],"ou":[]}
    for col in pred.columns:
        if ("AH" in col and "P(" not in col and not np.isnan(row[col]) and row[col] != 1):
            #if (row["P(" + col + ")"] - (1/row[col]) > 0):
            dict["ah"].append(row["P(" + col + ")"] - (1/row[col]))
        if (("Over" in col or "Under" in col) and "P(" not in col and not np.isnan(row[col]) and row[col] != 1):
            #if (row["P(" + col + ")"] - (1/row[col]) > 0):
            dict["ou"].append(row["P(" + col + ")"] - (1/row[col]))
    if (dict["ah"]):
        ahMean = np.average(dict["ah"])
        ahStd = np.std(dict["ah"])
    if (dict["ou"]):
        ouMean = np.average(dict["ou"])
        ouStd = np.std(dict["ou"])
    for col in pred.columns:
        if ("AH" in col and "P(" not in col and not np.isnan(row[col]) and row[col] != 1):
            if (dict["ah"] and abs((row["P(" + col + ")"] - (1/row[col]) - ahMean)/ahStd) > 3.5 and row["P(" + col + ")"] - (1/row[col]) > 0):
                row[col] = np.nan
        if (("Over" in col or "Under" in col) and "P(" not in col and not np.isnan(row[col]) and row[col] != 1):
            if (dict["ou"] and abs((row["P(" + col + ")"] - (1/row[col]) - ouMean)/ouStd) > 3.5 and row["P(" + col + ")"] - (1/row[col]) > 0):
                row[col] = np.nan
