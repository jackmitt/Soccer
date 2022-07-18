import pandas as pd
import numpy as np
from helpers import standardizeTeamName

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

verifyTeamNamesTransfermarkt("Korea1")
