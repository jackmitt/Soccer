import pandas as pd
import numpy as np

curElo = {}
curTeams = []
df = pd.read_csv('./EPLHistoricOdds.csv', encoding = "ISO-8859-1")
for index, row in df.iterrows():
    if (row["Date"].split('-')[1] == "Aug" and row["Date"].split('-')[2] == "09"):
        break
    if (row["Home"] not in curElo):
        curElo[row["Home"]] = {"Elo":1500,"G":0}
        curTeams.append(row["Home"])

incEloHome = []
incEloAway = []
resEloHome = []
resEloAway = []
newSeason = False
newTeams = []


for index, row in df.iterrows():
    if (row["Date"].split('-')[1] == "Aug" and newSeason):
        elos = []
        for key in curElo:
            curElo[key]["G"] = 0
            elos.append(curElo[key]["Elo"])
        for key in curElo:
            curElo[key]["Elo"] = ((curElo[key]["Elo"] - np.average(elos)) / np.std(elos)) * (np.std(elos)/2) + 1500
        newSeason = False
    if (row["Date"].split('-')[1] == "Sep"):
        newSeason = True
    incEloHome.append(curElo[row["Home"]]["Elo"])
    incEloAway.append(curElo[row["Away"]]["Elo"])
    # 0.05 to compensate for home field advantage
    eH = min(1, 1/(1+10**((curElo[row["Away"]]["Elo"] - curElo[row["Home"]]["Elo"])/400)) + 0.05)
    eA = 1 - eH
    kH = 100/np.log((curElo[row["Home"]]["G"] / 50) + 3)
    kA = 100/np.log((curElo[row["Away"]]["G"] / 50) + 3)
    if (int(row["Home Score"]) > int(row["Away Score"])):
        curElo[row["Home"]]["Elo"] += kH*(1-eH)
        curElo[row["Away"]]["Elo"] += kA*(0-eA)
    elif (int(row["Home Score"]) < int(row["Away Score"])):
        curElo[row["Home"]]["Elo"] += kH*(0-eH)
        curElo[row["Away"]]["Elo"] += kA*(1-eA)
    else:
        curElo[row["Home"]]["Elo"] += kH*(0.5-eH)
        curElo[row["Away"]]["Elo"] += kA*(0.5-eA)
    curElo[row["Away"]]["G"] += 1
    curElo[row["Home"]]["G"] += 1
    resEloHome.append(curElo[row["Home"]]["Elo"])
    resEloAway.append(curElo[row["Away"]]["Elo"])
    #for promoted/relegated teams
    if (index < len(df.index) - 1 and row["Date"].split("-")[1] != "Aug" and df.iat[index+1, 0].split("-")[1] == "Aug"):
        for index1, row1, in df.iterrows():
            if (index1 > index):
                if (len(newTeams) == 20):
                    break
                if (row1["Home"] not in newTeams):
                    newTeams.append(row1["Home"])
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
df["Home Pre Elo"] = incEloHome
df["Away Pre Elo"] = incEloAway
df["Home Post Elo"] = resEloHome
df["Away Post Elo"] = resEloAway
df.to_csv('./EPLHistoricOddsWithElo.csv')
