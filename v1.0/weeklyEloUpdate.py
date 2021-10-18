import pandas as pd
import numpy as np
from miscFcns import standardizeTeamName

mwThru = 17
curElo = {}
curTeams = []
df = pd.read_csv('./EPL_Csvs/EPLHistoricOdds.csv', encoding = "ISO-8859-1")
df = df.drop_duplicates(ignore_index = True)
for index, row in df.iterrows():
    if (row["Date"].split('-')[1] == "Aug" and row["Date"].split('-')[2] == "09"):
        break
    if (standardizeTeamName(row["Home"]) not in curElo):
        curElo[standardizeTeamName(row["Home"])] = {"Elo":1500,"G":0}
        curTeams.append(standardizeTeamName(row["Home"]))
newTeams = []


for index, row in df.iterrows():
    if (index != 0 and row["Date"].split('-')[1] != "May" and df.at[index-1,"Date"].split("-")[1] == "May"):
        elos = []
        for key in curElo:
            curElo[key]["G"] = 0
            elos.append(curElo[key]["Elo"])
        for key in curElo:
            curElo[key]["Elo"] = ((curElo[key]["Elo"] - np.average(elos)) / np.std(elos)) * (np.std(elos)/2) + 1500
    # 0.05 to compensate for home field advantage
    eH = min(1, 1/(1+10**((curElo[standardizeTeamName(row["Away"])]["Elo"] - curElo[standardizeTeamName(row["Home"])]["Elo"])/400)) + 0.05)
    eA = 1 - eH
    kH = 100/np.log((curElo[standardizeTeamName(row["Home"])]["G"] / 50) + 3)
    kA = 100/np.log((curElo[standardizeTeamName(row["Away"])]["G"] / 50) + 3)
    if (int(row["Home Score"]) > int(row["Away Score"])):
        curElo[standardizeTeamName(row["Home"])]["Elo"] += kH*(1-eH)
        curElo[standardizeTeamName(row["Away"])]["Elo"] += kA*(0-eA)
    elif (int(row["Home Score"]) < int(row["Away Score"])):
        curElo[standardizeTeamName(row["Home"])]["Elo"] += kH*(0-eH)
        curElo[standardizeTeamName(row["Away"])]["Elo"] += kA*(1-eA)
    else:
        curElo[standardizeTeamName(row["Home"])]["Elo"] += kH*(0.5-eH)
        curElo[standardizeTeamName(row["Away"])]["Elo"] += kA*(0.5-eA)
    curElo[standardizeTeamName(row["Away"])]["G"] += 1
    curElo[standardizeTeamName(row["Home"])]["G"] += 1
    #for promoted/relegated teams
    if (index < len(df.index) - 1 and row["Date"].split("-")[1] == "May" and df.at[index+1, "Date"].split("-")[1] != "May"):
        for index1, row1, in df.iterrows():
            if (index1 > index):
                if (len(newTeams) == 20):
                    break
                if (standardizeTeamName(row1["Home"]) not in newTeams):
                    newTeams.append(standardizeTeamName(row1["Home"]))
        tSwitch = list((set(newTeams) | set(curTeams)) - (set(newTeams) & set(curTeams)))
        curRelElo = []
        for team in tSwitch:
            if (team in curTeams):
                curRelElo.append(curElo[team]["Elo"])
                del curElo[team]
        for team in tSwitch:
            if (team in newTeams):
                curElo[team] = {"Elo":np.average(curRelElo),"G":0}
        curTeams = newTeams.copy()
        newTeams = []
print (curElo)
for i in range(1, mwThru+1):
    incEloHome = []
    incEloAway = []
    resEloHome = []
    resEloAway = []
    games = pd.read_csv('./EPL_Csvs/2020-21_Season/match_stats/MW' + str(i) + '.csv', encoding = "ISO-8859-1")
    if (i == 1):
        allTeamsHere = pd.read_csv('./EPL_Csvs/2020-21_Season/match_stats/MW2.csv', encoding = "ISO-8859-1")
        newTeams = []
        for index1, row1, in allTeamsHere.iterrows():
            if (standardizeTeamName(row1["Home"]) not in newTeams):
                newTeams.append(standardizeTeamName(row1["Home"]))
            if (standardizeTeamName(row1["Away"]) not in newTeams):
                newTeams.append(standardizeTeamName(row1["Away"]))
        tSwitch = list((set(newTeams) | set(curTeams)) - (set(newTeams) & set(curTeams)))
        curRelElo = []
        for team in tSwitch:
            if (team in curTeams):
                curRelElo.append(curElo[team]["Elo"])
                del curElo[team]
        for team in tSwitch:
            if (team in newTeams):
                curElo[team] = {"Elo":np.average(curRelElo),"G":0}
        curTeams = newTeams.copy()
        elos = []
        for key in curElo:
            curElo[key]["G"] = 0
            elos.append(curElo[key]["Elo"])
        for key in curElo:
            curElo[key]["Elo"] = ((curElo[key]["Elo"] - np.average(elos)) / np.std(elos)) * (np.std(elos)/2) + 1500
        print (curElo)
    for index, row in games.iterrows():
        incEloHome.append(curElo[standardizeTeamName(row["Home"])]["Elo"])
        incEloAway.append(curElo[standardizeTeamName(row["Away"])]["Elo"])
        # 0.05 to compensate for home field advantage
        eH = min(1, 1/(1+10**((curElo[standardizeTeamName(row["Away"])]["Elo"] - curElo[standardizeTeamName(row["Home"])]["Elo"])/400)) + 0.05)
        eA = 1 - eH
        kH = 100/np.log((curElo[standardizeTeamName(row["Home"])]["G"] / 50) + 3)
        kA = 100/np.log((curElo[standardizeTeamName(row["Away"])]["G"] / 50) + 3)
        if (int(row["Home Score"]) > int(row["Away Score"])):
            curElo[standardizeTeamName(row["Home"])]["Elo"] += kH*(1-eH)
            curElo[standardizeTeamName(row["Away"])]["Elo"] += kA*(0-eA)
        elif (int(row["Home Score"]) < int(row["Away Score"])):
            curElo[standardizeTeamName(row["Home"])]["Elo"] += kH*(0-eH)
            curElo[standardizeTeamName(row["Away"])]["Elo"] += kA*(1-eA)
        else:
            curElo[standardizeTeamName(row["Home"])]["Elo"] += kH*(0.5-eH)
            curElo[standardizeTeamName(row["Away"])]["Elo"] += kA*(0.5-eA)
        curElo[standardizeTeamName(row["Away"])]["G"] += 1
        curElo[standardizeTeamName(row["Home"])]["G"] += 1
        resEloHome.append(curElo[standardizeTeamName(row["Home"])]["Elo"])
        resEloAway.append(curElo[standardizeTeamName(row["Away"])]["Elo"])
    games["Home Pre Elo"] = incEloHome
    games["Away Pre Elo"] = incEloAway
    games["Home Post Elo"] = resEloHome
    games["Away Post Elo"] = resEloAway
    if (i == mwThru):
        games.to_csv('./EPL_Csvs/2020-21_Season/match_stats/MW' + str(i) + '.csv')
