#import scrapers as scr
import data_manipulation as dm
import predictions as pr
import evaluations as eval
import pandas as pd
import numpy as np


leagues = ["France1", "France2", "France3", "Germany1", "Germany2", "Germany3"]
for league in leagues:
    print ("-----------------------------------------------",league)
    #dm.preMatchAverages(league)
    #dm.train_test_split(league)
    #pr.WeibullCountDistPredictions(league)
    #eval.analyzeWinRates(league, "AH", "Close")
    #eval.kellybet(league, "AH", "Close", 20000, 12, 0.1)
    pr.bayesian(league)
    #eval.analyzeLineMovement(league, "AH", moveDirection = "renst")
#r.fitWeibullParameters()


# leagues = ["England1"]
# for league in leagues:
#     pred = pd.read_csv("./csv_data/" + league + "/bayes_predictions.csv", encoding = "ISO-8859-1")
#     cover = []
#     over = []
#     for index, row in pred.iterrows():
#         if (".75" in str(row["Open AH"]) or "0.25" in str(row["Open AH"])):
#             cover.append(np.nan)
#         elif (row["home_team_reg_score"] - row["Open AH"] > row["away_team_reg_score"]):
#             cover.append(1)
#         elif (row["home_team_reg_score"] - row["Open AH"] < row["away_team_reg_score"]):
#             cover.append(0)
#         else:
#             cover.append(np.nan)
#
#         if (".75" in str(row["Open OU"]) or "0.25" in str(row["Open OU"])):
#             over.append(np.nan)
#         elif (row["home_team_reg_score"] + row["away_team_reg_score"] > row["Open OU"]):
#             over.append(1)
#         elif (row["home_team_reg_score"] + row["away_team_reg_score"] < row["Open OU"]):
#             over.append(0)
#         else:
#             over.append(np.nan)
#     pred["cover"] = cover
#     pred["over"] = over
#     pred.to_csv("./csv_data/" + league + "/bayes_predictions.csv", index = False)
