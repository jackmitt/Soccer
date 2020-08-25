import pandas as pd
import numpy as np
from miscFcns import standardizeTeamName

df1 = pd.read_csv('./SerieA_Csvs/HistoricOddsWithElo.csv', encoding = "ISO-8859-1")
df2 = pd.read_csv('./SerieA_Csvs/whoscoredGameStats.csv', encoding = "ISO-8859-1")
df3 = pd.read_csv('./SerieA_Csvs/understatGameStats.csv', encoding = "ISO-8859-1")

for index, row in df3.iterrows():
    if (standardizeTeamName(row["Home"], "Serie A").islower()):
        print (standardizeTeamName(row["Home"], "Serie A"))
