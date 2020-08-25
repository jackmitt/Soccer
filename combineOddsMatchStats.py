import pandas as pd
import numpy as np
from miscFcns import standardizeTeamName

matchStats = pd.read_csv('./SerieA_Csvs/matchStats.csv', encoding = "ISO-8859-1")
odds = pd.read_csv('./SerieA_Csvs/HistoricOddsWithElo.csv', encoding = "ISO-8859-1")
dict = {}
for col in odds.columns:
    if (col != "Date" and col != "Home" and col != "Away"):
        dict[col] = []

bool = False
for index, row in matchStats.iterrows():
    #print (index)
    #where 2014 season begins
    curIndex = 2278
    while (curIndex < len(odds.index)):
        if (odds.at[curIndex, "Date"] == row["Date"] and standardizeTeamName(odds.at[curIndex, "Home"], "Serie A") == standardizeTeamName(row["Home"], "Serie A") and standardizeTeamName(odds.at[curIndex, "Away"], "Serie A") == standardizeTeamName(row["Away"], "Serie A")):
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

matchStats.to_csv("./SerieA_Csvs/allRawData.csv")
