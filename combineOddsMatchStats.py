import pandas as pd
import numpy as np
from miscFcns import standardizeTeamName

matchStats = pd.read_csv('./EPL_Csvs/matchStats.csv', encoding = "ISO-8859-1")
odds = pd.read_csv('./EPL_Csvs/HistoricOddsWithElo.csv', encoding = "ISO-8859-1")
dict = {}
for col in odds.columns:
    if (col != "Date" and col != "Home" and col != "Away"):
        dict[col] = []

bool = False
for index, row in matchStats.iterrows():
    #print (index)
    #where 2014 season begins
    curIndex = 2274
    while (curIndex < len(odds.index)):
        if (odds.at[curIndex, "Date"] == row["Date"] and standardizeTeamName(odds.at[curIndex, "Home"], "La Liga") == standardizeTeamName(row["Home"], "La Liga") and standardizeTeamName(odds.at[curIndex, "Away"], "La Liga") == standardizeTeamName(row["Away"], "La Liga")):
            bool = True
            for col in odds.columns:
                if (col != "Date" and col != "Home" and col != "Away"):
                    dict[col].append(odds.at[curIndex, col])
        curIndex += 1
    if (bool):
        bool = False
    else:
        print (row["Date"], row["Home"], row["Away"])
        for col in odds.columns:
            if (col != "Date" and col != "Home" and col != "Away"):
                dict[col].append(np.nan)

for key in dict:
    matchStats[key] = dict[key]

matchStats.to_csv("./EPL_Csvs/allRawData.csv")
