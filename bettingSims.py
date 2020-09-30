import pandas as pd
import numpy as np

ml = pd.read_csv('./EPL_Csvs/mlResultsByEdge3Games.csv', encoding = "ISO-8859-1")
ah = pd.read_csv('./EPL_Csvs/ahResultsByEdge3Games.csv', encoding = "ISO-8859-1")
ou = pd.read_csv('./EPL_Csvs/ouResultsByEdge3Games.csv', encoding = "ISO-8859-1")
for df in [ml,ah,ou]:
    best = 0
    bn = 0
    kellyDiv = 1
    while (1):
        #print (kellyDiv)
        bankroll = 30000
        netwin = 0
        for index, row in df.iterrows():
            # if (index > len(pred.index)/5):
            #     break
            if (row["P"] > row["Book Prob"]):
                if (row["Result"] == 1):
                    bankroll += (row["P"] - row["Book Prob"]) / (1-(row["Book Prob"]))*bankroll*((1/row["Book Prob"]) - 1)/kellyDiv
                    netwin += (row["P"] - row["Book Prob"]) / (1-(row["Book Prob"]))*30000*((1/row["Book Prob"]) - 1)/kellyDiv
                else:
                    bankroll -= (row["P"] - row["Book Prob"]) / (1-(row["Book Prob"]))*bankroll/kellyDiv
                    netwin -= (row["P"] - row["Book Prob"]) / (1-(row["Book Prob"]))*30000/kellyDiv
        if (bankroll > best):
            best = bankroll
            bn = netwin
        else:
            break
        if (kellyDiv > 1000):
            break
        kellyDiv *= 1.05
    print (kellyDiv)
    print (best)
    print (bn)
