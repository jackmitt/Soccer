import pandas as pd
import numpy as np

ah = pd.read_csv('./EPL_Csvs/no_T_Vars/ahTruePredictedProbabilities.csv', encoding = "ISO-8859-1")
ou = pd.read_csv('./EPL_Csvs/no_T_Vars/ouTruePredictedProbabilities.csv', encoding = "ISO-8859-1")

ahkellyDiv = 3
oukellyDiv = 1

for k in range(25):
    #Season loop
    curIter = 0
    lowestReturn = 1000
    highestReturn = -1
    endingReturns = []
    betSizes = []
    while (curIter < 1000):
        # if (curIter % 100 == 0):
        #     print (curIter)
        ah = ah.sample(frac=1).reset_index(drop=True)
        ou = ou.sample(frac=1).reset_index(drop=True)
        bankroll = 1
        for i in range(380):
            if (i % 10 == 0):
                temp = 1
            if (ah.at[i, "True Prediction"] > ah.at[i, "Book.Prob"]):
                if (ah.at[i, "Result"] == 1):
                    temp += (ah.at[i, "True Prediction"] - ah.at[i, "Book.Prob"]) / (1-(ah.at[i, "Book.Prob"]))*((1/ah.at[i, "Book.Prob"]) - 1)/ahkellyDiv
                    betSizes.append((ah.at[i, "True Prediction"] - ah.at[i, "Book.Prob"]) / (1-(ah.at[i, "Book.Prob"]))/ahkellyDiv)
                else:
                    temp -= (ah.at[i, "True Prediction"] - ah.at[i, "Book.Prob"]) / (1-(ah.at[i, "Book.Prob"]))/ahkellyDiv
                    betSizes.append((ah.at[i, "True Prediction"] - ah.at[i, "Book.Prob"]) / (1-(ah.at[i, "Book.Prob"]))/ahkellyDiv)
            if (ou.at[i, "True Prediction"] > ou.at[i, "Book.Prob"]):
                if (ou.at[i, "Result"] == 1):
                    temp += (ou.at[i, "True Prediction"] - ou.at[i, "Book.Prob"]) / (1-(ou.at[i, "Book.Prob"]))*((1/ou.at[i, "Book.Prob"]) - 1)/oukellyDiv
                    betSizes.append((ou.at[i, "True Prediction"] - ou.at[i, "Book.Prob"]) / (1-(ou.at[i, "Book.Prob"]))/oukellyDiv)
                else:
                    temp -= (ou.at[i, "True Prediction"] - ou.at[i, "Book.Prob"]) / (1-(ou.at[i, "Book.Prob"]))/oukellyDiv
                    betSizes.append((ou.at[i, "True Prediction"] - ou.at[i, "Book.Prob"]) / (1-(ou.at[i, "Book.Prob"]))/oukellyDiv)
            if (i % 10 == 9):
                bankroll = bankroll * temp
        curIter += 1
        if (bankroll - 1 > highestReturn):
            highestReturn = bankroll - 1
        if (bankroll - 1 < lowestReturn):
            lowestReturn = bankroll - 1
        endingReturns.append((bankroll - 1))
    print ("Level", k, "with ahDiv of", ahkellyDiv, "and ouDiv of", oukellyDiv)
    print ("Average Seasonal Return:", str(np.average(endingReturns)))
    print ("Standard Deviation:", np.std(endingReturns))
    print ("Lowest Observed Return:", max(lowestReturn,-1))
    print ("Highest Observed Return:", highestReturn)
    print ("Average Bet Size:", np.average(betSizes))
    temp = []
    for r in endingReturns:
        if (r <= 0):
            temp.append(1)
        else:
            temp.append(0)
    print ("Percent of Seasons Ending with less than 100% of bankroll:", np.average(temp))
    temp = []
    for r in endingReturns:
        if (r <= -0.25):
            temp.append(1)
        else:
            temp.append(0)
    print ("Percent of Seasons Ending with less than 75% of bankroll:", np.average(temp))
    temp = []
    for r in endingReturns:
        if (r <= -0.5):
            temp.append(1)
        else:
            temp.append(0)
    print ("Percent of Seasons Ending with less than 50% of bankroll:", np.average(temp))
    temp = []
    for r in endingReturns:
        if (r <= -0.75):
            temp.append(1)
        else:
            temp.append(0)
    print ("Percent of Seasons Ending with less than 25% of bankroll:", np.average(temp))
    print ("------------------------------------------------------------------------------------------------")
    oukellyDiv += 0.5
    ahkellyDiv += 0.5
