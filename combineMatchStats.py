import pandas as pd
import numpy as np
from miscFcns import standardizeTeamName
from miscFcns import monthToInt
import datetime

league = input("1 for EPL, 2 for Serie A: ")
if (int(league) == 1):
    understat = pd.read_csv('./EPL_Csvs/understatGameStats.csv', encoding = "ISO-8859-1")
    whoscored = pd.read_csv('./EPL_Csvs/whoscoredGameStats.csv', encoding = "ISO-8859-1")
    para = "EPL"
elif (int(league) == 2):
    understat = pd.read_csv('./SerieA_Csvs/understatGameStats.csv', encoding = "ISO-8859-1")
    whoscored = pd.read_csv('./SerieA_Csvs/whoscoredGameStats.csv', encoding = "ISO-8859-1")
    para = "Serie A"
homeXg = []
awayXg = []
homeDeep = []
awayDeep = []
homePpda = []
awayPpda = []
homeXpts = []
awayXpts = []

found = False
for index, row in whoscored.iterrows():
    #print (index)
    date = datetime.datetime(2000+int(row["Date"].split("-")[2]), monthToInt(row["Date"].split("-")[1]), int(row["Date"].split("-")[0]))
    for index1, row1 in understat.iterrows():
        date1 = datetime.datetime(2000+int(row1["Date"].split("-")[2]), monthToInt(row1["Date"].split("-")[1]), int(row1["Date"].split("-")[0]))
        if ((date == date1 or date + datetime.timedelta(days=1) == date1 or date == date1 + datetime.timedelta(days=1)) and standardizeTeamName(row1["Home"], para) == standardizeTeamName(row["Home"], para) and standardizeTeamName(row1["Away"], para) == standardizeTeamName(row["Away"], para)):
            found = True
            homeXg.append(row1["Home xG"])
            awayXg.append(row1["Away xG"])
            homeDeep.append(row1["Home deep"])
            awayDeep.append(row1["Away deep"])
            homePpda.append(row1["Home ppda"])
            awayPpda.append(row1["Away ppda"])
            homeXpts.append(row1["Home xPts"])
            awayXpts.append(row1["Away xPts"])
            break
    if (not found):
        print (row["Date"], row["Home"], row["Away"])
        homeXg.append(np.nan)
        awayXg.append(np.nan)
        homeDeep.append(np.nan)
        awayDeep.append(np.nan)
        homePpda.append(np.nan)
        awayPpda.append(np.nan)
        homeXpts.append(np.nan)
        awayXpts.append(np.nan)
    else:
        found = False
whoscored["Home xG"] = homeXg
whoscored["Home deep"] = homeDeep
whoscored["Home ppda"] = homePpda
whoscored["Home xPts"] = homeXpts
whoscored["Away xG"] = awayXg
whoscored["Away deep"] = awayDeep
whoscored["Away ppda"] = awayPpda
whoscored["Away xPts"] = awayXpts

if (int(league) == 1):
    whoscored.to_csv('./EPL_Csvs/matchStats.csv')
elif (int(league) == 2):
    whoscored.to_csv('./SerieA_Csvs/matchStats.csv')
