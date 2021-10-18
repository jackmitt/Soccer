import pandas as pd
import numpy as np

ah = pd.read_csv('./LaLiga_Csvs/ah.csv', encoding = "ISO-8859-1")
ou = pd.read_csv('./LaLiga_Csvs/ou.csv', encoding = "ISO-8859-1")
ml = pd.read_csv('./LaLiga_Csvs/1x2.csv', encoding = "ISO-8859-1")
dict = ml.to_dict("list")

ahmatch = False
oumatch = False
for index, row in ml.iterrows():
    print (index)
    #index where 2014 season begins
    if (index >= 2280):
        for key in dict:
            print (key, len(dict[key]))
        for index1, row1 in ah.iterrows():
            if (row1["Date"] == row["Date"] and row1["Home"] == row["Home"] and row1["Away"] == row["Away"]):
                ahmatch = True
                for col in ah.columns:
                    if (col != "Date" and col != "Home" and col != "Away" and col != "Home Score" and col != "Away Score"):
                        if (col not in dict):
                            dict[col] = []
                        dict[col].append(row1[col])
        if (not ahmatch):
            for col in ah.columns:
                if (col != "Date" and col != "Home" and col != "Away" and col != "Home Score" and col != "Away Score"):
                    dict[col].append(np.nan)
        else:
            ahmatch = False
        for index1, row1 in ou.iterrows():
            if (row1["Date"] == row["Date"] and row1["Home"] == row["Home"] and row1["Away"] == row["Away"]):
                oumatch = True
                for col in ou.columns:
                    if (col != "Date" and col != "Home" and col != "Away" and col != "Home Score" and col != "Away Score"):
                        if (col not in dict):
                            dict[col] = []
                        dict[col].append(row1[col])
        if (not oumatch):
            for col in ou.columns:
                if (col != "Date" and col != "Home" and col != "Away" and col != "Home Score" and col != "Away Score"):
                    dict[col].append(np.nan)
        else:
            oumatch = False
    else:
        for col in ah.columns:
            if (col != "Date" and col != "Home" and col != "Away" and col != "Home Score" and col != "Away Score"):
                if (col not in dict):
                    dict[col] = []
                dict[col].append(np.nan)
        for col in ou.columns:
            if (col != "Date" and col != "Home" and col != "Away" and col != "Home Score" and col != "Away Score"):
                if (col not in dict):
                    dict[col] = []
                dict[col].append(np.nan)
dfFinal = pd.DataFrame.from_dict(dict)
dfFinal.to_csv("./LaLiga_Csvs/combinedOdds.csv")
