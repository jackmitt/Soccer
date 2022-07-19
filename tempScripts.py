import pandas as pd
import numpy as np
from helpers import standardizeTeamName
from fuzzywuzzy import fuzz

def verifyTeamNamesTransfermarkt(league):
    temp = pd.read_csv("./csv_data/" + league + "/transfermarkt.csv", encoding = "UTF-8")["Team"].unique()
    real = pd.read_csv("./csv_data/" + league + "/betting.csv", encoding = "ISO-8859-1")["Home"].unique()
    print (temp)
    print (real)
    for team in temp:
        fix = ""
        for i in range(len(team.split())):
            fix = fix + team.split()[i]
            if (i != len(team.split()) - 1):
                fix = fix + " "
        if (standardizeTeamName(fix,league) not in real):
            print (fix)

def team_match_algo(league):
    temp = pd.read_csv("./csv_data/" + league + "/transfermarkt.csv", encoding = "UTF-8")["Team"].unique()
    real = pd.read_csv("./csv_data/" + league + "/betting.csv", encoding = "ISO-8859-1")["Home"].unique()
    teams = {}
    for j in range(len(temp)):
        if (temp[j] not in teams):
            teams[temp[j]] = ("",0)
        for i in range(len(real)):
            if (fuzz.ratio(temp[j], real[i]) > teams[temp[j]][1] and fuzz.ratio(temp[j], real[i]) > 30):
                teams[temp[j]] = (real[i], fuzz.ratio(temp[j], real[i]))
    print (teams)
    for team in teams:
        if (teams[team][1] == 0):
            print (team)

verifyTeamNamesTransfermarkt("Belgium1")
#team_match_algo("Austria2")
#team_match_algo("Norway2")
