import pandas as pd
import numpy as np
from miscFcns import standardizeTeamName

df1 = pd.read_csv('./LaLiga_Csvs/ou.csv', encoding = "ISO-8859-1")
df2 = pd.read_csv('./LaLiga_Csvs/whoscoredGameStats.csv', encoding = "ISO-8859-1")
df3 = pd.read_csv('./LaLiga_Csvs/understatGameStats.csv', encoding = "ISO-8859-1")

for index, row in df1.iterrows():
    if (standardizeTeamName(row["Home"], "La Liga").islower()):
        print (standardizeTeamName(row["Home"], "La Liga"))
