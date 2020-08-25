import pandas as pd
import numpy as np

bb = pd.read_csv('./SerieA_Csvs/bigboy.csv', encoding = "ISO-8859-1")

dict = {"Date":[], "Team":[], "Score":[], "Home Field":[]}
sides = ["expected", "opponent_expected"]
for col in bb.columns:
    if ("home_expected" in col):
        for side in sides:
            dict[col.split("home_expected")[0] + side + col.split("home_expected")[1]] = []

for index, row in bb.iterrows():
    print (index)
    dict["Date"].append(row["Date"])
    dict["Team"].append(row["Home"])
    dict["Score"].append(row["Home Score"])
    dict["Home Field"].append(1)
    for col in bb.columns:
        if ("home_expected" in col):
            dict[col.split("home_expected")[0] + "expected" + col.split("home_expected")[1]].append(row[col])
        elif ("away_expected" in col):
            dict[col.split("away_expected")[0] + "opponent_expected" + col.split("away_expected")[1]].append(row[col])
    dict["Date"].append(row["Date"])
    dict["Team"].append(row["Away"])
    dict["Score"].append(row["Away Score"])
    dict["Home Field"].append(0)
    for col in bb.columns:
        if ("away_expected" in col):
            dict[col.split("away_expected")[0] + "expected" + col.split("away_expected")[1]].append(row[col])
        elif ("home_expected" in col):
            dict[col.split("home_expected")[0] + "opponent_expected" + col.split("home_expected")[1]].append(row[col])
for key in dict:
    print (key, len(dict[key]))

dfFinal = pd.DataFrame.from_dict(dict)
dfFinal = dfFinal.dropna()
dfFinal.to_csv("./SerieA_Csvs/poissonFormattedData.csv")
