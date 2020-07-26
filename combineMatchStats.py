import pandas as pd
import numpy as np

understat = pd.read_csv('./understatGameStats.csv', encoding = "ISO-8859-1")
whoscored = pd.read_csv('./whoscoredGameStats.csv', encoding = "ISO-8859-1")
homeXg = []
awayXg = []
homeDeep = []
awayDeep = []
homePpda = []
awayPpda = []
homeXpts = []
awayXpts = []

for index, row in whoscored.iterrows():
    print (index)
    for index1, row1 in understat.iterrows():
        if (row1["Date"] == row["Date"] and row1["Home"] == row["Home"] and row1["Away"] == row["Away"]):
            homeXg.append(row1["Home xG"])
            awayXg.append(row1["Away xG"])
            homeDeep.append(row1["Home deep"])
            awayDeep.append(row1["Away deep"])
            homePpda.append(row1["Home ppda"])
            awayPpda.append(row1["Away ppda"])
            homeXpts.append(row1["Home xPts"])
            awayXpts.append(row1["Away xPts"])
whoscored["Home xG"] = homeXg
whoscored["Home deep"] = homeDeep
whoscored["Home ppda"] = homePpda
whoscored["Home xPts"] = homeXpts
whoscored["Away xG"] = awayXg
whoscored["Away deep"] = awayDeep
whoscored["Away ppda"] = awayPpda
whoscored["Away xPts"] = awayXpts

whoscored.to_csv('./matchStats.csv')
