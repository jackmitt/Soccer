import pandas as pd
import numpy as np

matchStats = pd.read_csv('./matchStats.csv', encoding = "ISO-8859-1")
odds = pd.read_csv('./EPLHistoricOddsWithElo.csv', encoding = "ISO-8859-1")
dict = {}
for col in odds.columns:
    if (col != "Date" and col != "Home" and col != "Away"):
        dict[col] = []

bool = False
for index, row in matchStats.iterrows():
    print (index)
    curIndex = 2274
    while (curIndex < len(odds.index)):
        if (odds.at[curIndex, "Date"] == row["Date"] and odds.at[curIndex, "Home"] == row["Home"] and odds.at[curIndex, "Away"] == row["Away"]):
            bool = True
            for col in odds.columns:
                if (col != "Date" and col != "Home" and col != "Away"):
                    dict[col].append(odds.at[curIndex, col])
        curIndex += 1
    if (bool):
        bool = False
    else:
        for col in odds.columns:
            if (col != "Date" and col != "Home" and col != "Away"):
                dict[col].append(np.nan)

for key in dict:
    matchStats[key] = dict[key]

matchStats.to_csv("allRawData.csv")
