import pandas as pd
import numpy as np
import datetime

def preMatchAverages(league):
    stats = pd.read_csv("./csv_data/" + league + "/betting.csv", encoding = "ISO-8859-1")
    for i in range(len(stats.index)):
        stats.at[i, "Date"] = datetime.date(int(stats.at[i, "Date"].split("-")[0]), int(stats.at[i, "Date"].split("-")[1]), int(stats.at[i, "Date"].split("-")[2]))
    stats = stats.sort_values(by=["Date"], ignore_index = True)

    dict = {"H_proj":[],"A_proj":[],"H_GP":[],"A_GP":[]}
    for index, row in stats.iterrows():
        if (index == 0 or abs(row["Date"] - stats.at[index-1,"Date"]).days > 30):
            seasonDict = {}
        if (row["Home"] not in seasonDict):
            seasonDict[row["Home"]] = {"G":[],"GA":[],"GP":0}
        if (row["Away"] not in seasonDict):
            seasonDict[row["Away"]] = {"G":[],"GA":[],"GP":0}

        dict["H_GP"].append(seasonDict[row["Home"]]["GP"])
        dict["A_GP"].append(seasonDict[row["Away"]]["GP"])
        if (seasonDict[row["Away"]]["GP"] > 5 and seasonDict[row["Home"]]["GP"] > 5):
            dict["H_proj"].append((np.average(seasonDict[row["Home"]]["G"]) + np.average(seasonDict[row["Away"]]["GA"])) / 2)
            dict["A_proj"].append((np.average(seasonDict[row["Away"]]["G"]) + np.average(seasonDict[row["Home"]]["GA"])) / 2)
        else:
            dict["H_proj"].append(np.nan)
            dict["A_proj"].append(np.nan)

        seasonDict[row["Home"]]["G"].append(row["Home Score"])
        seasonDict[row["Away"]]["GA"].append(row["Home Score"])
        seasonDict[row["Away"]]["G"].append(row["Away Score"])
        seasonDict[row["Home"]]["GA"].append(row["Away Score"])
        seasonDict[row["Away"]]["GP"] += 1
        seasonDict[row["Home"]]["GP"] += 1

    for key in dict:
        stats[key] = dict[key]
    stats.to_csv("./csv_data/" + league + "/preMatchAverages.csv", index = False)

def train_test_split(league):
    data = pd.read_csv("./csv_data/" + league + "/preMatchAverages.csv", encoding = "ISO-8859-1")
    test = False
    trainRows = []
    testRows = []
    for index, row in data.iterrows():
        #used to be 2017
        if (row["Date"].split("-")[0] == "2017" and abs(datetime.date(int(row["Date"].split("-")[0]), int(row["Date"].split("-")[1]), int(row["Date"].split("-")[2])) - datetime.date(int(data.at[index-1,"Date"].split("-")[0]), int(data.at[index-1,"Date"].split("-")[1]), int(data.at[index-1,"Date"].split("-")[2]))).days > 30):
            test = True
        if (test):
            testRows.append(index)
        else:
            trainRows.append(index)
    data.iloc[trainRows].to_csv("./csv_data/" + league + "/train.csv", index = False)
    data.iloc[testRows].to_csv("./csv_data/" + league + "/test.csv", index = False)
