import pandas as pd
import numpy as np

ah = pd.read_csv('./LaLiga_Csvs/no_T_Vars/ahTruePredictedProbabilities.csv', encoding = "ISO-8859-1")
ou = pd.read_csv('./LaLiga_Csvs/no_T_Vars/ouTruePredictedProbabilities.csv', encoding = "ISO-8859-1")
best = 0
bn = 0
kellyDiv = 1
while (1):
    print (kellyDiv)
    bankroll = 30000
    netwin = 0
    for index, row in ou.iterrows():
        # if (index > len(pred.index)/5):
        #     break
        if (row["True Prediction"] > row["Book.Prob"]):
            if (row["Result"] == 1):
                bankroll += (row["True Prediction"] - row["Book.Prob"]) / (1-(row["Book.Prob"]))*bankroll*((1/row["Book.Prob"]) - 1)/kellyDiv
                netwin += (row["True Prediction"] - row["Book.Prob"]) / (1-(row["Book.Prob"]))*30000*((1/row["Book.Prob"]) - 1)/kellyDiv
            else:
                bankroll -= (row["True Prediction"] - row["Book.Prob"]) / (1-(row["Book.Prob"]))*bankroll/kellyDiv
                netwin -= (row["True Prediction"] - row["Book.Prob"]) / (1-(row["Book.Prob"]))*30000/kellyDiv
    if (bankroll > best):
        best = bankroll
        bn = netwin
    else:
        break
    kellyDiv = kellyDiv*1.05
print (best)
print (bn)
