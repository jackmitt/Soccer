import pandas as pd
import numpy as np
from simultaneousDependentKelly import gradient_ascent

pred = pd.read_csv("./EPL_Csvs/3Game_newvars_no_T/resultsByEdge3Games.csv", encoding = "ISO-8859-1")
betTypes = ["ML ", "AH ", "OU "]


for i, row in pred.iterrows():
    if (np.isnan(row["ML Bet Size"]) and np.isnan(row["AH Bet Size"]) and np.isnan(row["OU Bet Size"])):
        bn = []
        pt = [[],[],[],[],[],[],[],[],[],[],[]]
        pb = []
        kelly = []
        for j in range(11):
            for k in range(11):
                pt[j].append(pred.at[i, str(j) + " -- " + str(k)])
        for t in betTypes:
            if (not np.isnan(pred.at[i, t + "Book Prob"])):
                bn.append(pred.at[i, t + "Bet"])
                pb.append(pred.at[i, t + "Book Prob"])
                kelly.append((pred.at[i, t + "P"] - pred.at[i, t + "Book Prob"]) / (1-(pred.at[i, t + "Book Prob"])))
        print ("STARTING KELLY:::::", kelly)
        adjWagers = gradient_ascent(bn, pt, pb, kelly)

print (i)
