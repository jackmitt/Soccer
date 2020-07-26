import pandas as pd
import numpy as np
from miscFcns import standardizeTeamName

df = pd.read_csv('./understatGameStats.csv', encoding = "ISO-8859-1")
df2 = pd.read_csv('./EPLHistoricOdds.csv', encoding = "ISO-8859-1")
bool = False
home = []
away = []
print (df)
for index, row in df.iterrows():
    home.append(standardizeTeamName(row["Home"]))
    away.append(standardizeTeamName(row["Away"]))
df["Home"] = home
df["Away"] = away
print (df)
df.to_csv("./understatGameStats.csv")
