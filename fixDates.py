import pandas as pd
import numpy as np

df = pd.read_csv('./SerieA_Csvs/understatGameStats.csv', encoding = "ISO-8859-1")
for index, row in df.iterrows():
    df.at[index, "Date"] = row["Date"].split()[0] + " " + row["Date"].split()[1] + ", " + row["Date"].split()[2]
df.to_csv('./SerieA_Csvs/understatGameStats.csv')
