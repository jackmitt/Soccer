import pandas as pd
import numpy as np


pred = pd.read_csv('./EPL_Csvs/currentModelTrain/tempNaiveEval.csv', encoding = "ISO-8859-1")
ou = []
for index, row in pred.iterrows():
    if ("Over" in row["OU Bet"]):
        ou.append(1)
    else:
        ou.append(0)
print (np.average(ou))
