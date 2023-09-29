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
        fix = ""
        for i in range(len(temp[j].split())):
            fix = fix + temp[j].split()[i]
            if (i != len(temp[j].split()) - 1):
                fix = fix + " "
        if (fix not in teams):
            teams[fix] = ("",0)
        for i in range(len(real)):
            if (fuzz.ratio(fix, real[i]) > teams[fix][1] and fuzz.ratio(fix, real[i]) > 30):
                teams[fix] = (real[i], fuzz.ratio(fix, real[i]))
    print (teams)
    for team in teams:
        if (teams[team][1] == 0):
            print (team)

def algo_fix_transfermarkt(league):
    exclude = ["Akhisar Belediyespor","Gaziantep Büyüksehir Belediyespor","TKI Tavsanli Linyitspor","Büyüksehir Belediye Erzurumspor","Istanbul Güngörenspor","Sanliurfaspor","Osmanlispor FK","Büyüksehir Belediye Erzurumspor","Fatih Karagümrük","Akhisarspor","Eyüpspor","Manisa FK","Kocaelispor"]
    temp = pd.read_csv("./csv_data/" + league + "/transfermarkt.csv", encoding = "UTF-8")["Team"].unique()
    real = pd.read_csv("./csv_data/" + league + "/betting.csv", encoding = "ISO-8859-1")["Home"].unique()
    teams = {}
    for j in range(len(temp)):
        fix = ""
        for i in range(len(temp[j].split())):
            fix = fix + temp[j].split()[i]
            if (i != len(temp[j].split()) - 1):
                fix = fix + " "
        if (fix not in teams):
            teams[fix] = ("",0)
        for i in range(len(real)):
            if (fuzz.ratio(fix, real[i]) > teams[fix][1] and fuzz.ratio(fix, real[i]) > 30):
                teams[fix] = (real[i], fuzz.ratio(fix, real[i]))
    print (teams)
    for team in teams:
        if (teams[team][1] == 0):
            print (team)

    transfermarkt = pd.read_csv("./csv_data/" + league + "/transfermarkt.csv", encoding = "UTF-8")
    for i in range(len(transfermarkt.index)):
        fix = ""
        for j in range(len(transfermarkt.at[i, "Team"].split())):
            fix = fix + transfermarkt.at[i, "Team"].split()[j]
            if (j != len(transfermarkt.at[i, "Team"].split()) - 1):
                fix = fix + " "
        if (fix not in exclude):
            transfermarkt.at[i, "Team"] = teams[fix][0]

    transfermarkt.to_csv("./csv_data/" + league + "/transfermarkt.csv", index = False)

# league = "Turkey2"
#
# #team_match_algo(league)
# algo_fix_transfermarkt(league)
# verifyTeamNamesTransfermarkt(league)
