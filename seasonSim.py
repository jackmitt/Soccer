import pandas as pd
import numpy as np

ml = pd.read_csv('./EPL_Csvs/newvars_no_T/weibull_copula/mlResultsByEdge.csv', encoding = "ISO-8859-1")
ah = pd.read_csv('./EPL_Csvs/newvars_no_T/weibull_copula/ahResultsByEdge.csv', encoding = "ISO-8859-1")
ou = pd.read_csv('./EPL_Csvs/newvars_no_T/weibull_copula/ouResultsByEdge.csv', encoding = "ISO-8859-1")

ahkellyDiv = 11
oukellyDiv = 18
mlkellyDiv = 16

for k in range(1):
    #Season loop
    curIter = 0
    lowestReturn = 1000
    highestReturn = -1
    endingReturns = []
    betSizes = []
    weekWagers = []
    while (curIter < 1000):
        # if (curIter % 100 == 0):
        #     print (curIter)
        ah = ah.sample(frac=1).reset_index(drop=True)
        ml = ml.sample(frac=1).reset_index(drop=True)
        ou = ou.sample(frac=1).reset_index(drop=True)
        bankroll = 1
        for i in range(380):
            if (i % 10 == 0):
                temp = 1
                curWeekWagers = []
            if (np.isnan(ah.at[i, "P"])):
                curWeekWagers.append(0)
            elif (ah.at[i, "P"] > ah.at[i, "Book Prob"]):
                if (ah.at[i, "Result"] == 1):
                    temp += (ah.at[i, "P"] - ah.at[i, "Book Prob"]) / (1-(ah.at[i, "Book Prob"]))*((1/ah.at[i, "Book Prob"]) - 1)/ahkellyDiv
                    betSizes.append((ah.at[i, "P"] - ah.at[i, "Book Prob"]) / (1-(ah.at[i, "Book Prob"]))/ahkellyDiv)
                    curWeekWagers.append((ah.at[i, "P"] - ah.at[i, "Book Prob"]) / (1-(ah.at[i, "Book Prob"]))/ahkellyDiv)
                else:
                    temp -= (ah.at[i, "P"] - ah.at[i, "Book Prob"]) / (1-(ah.at[i, "Book Prob"]))/ahkellyDiv
                    betSizes.append((ah.at[i, "P"] - ah.at[i, "Book Prob"]) / (1-(ah.at[i, "Book Prob"]))/ahkellyDiv)
                    curWeekWagers.append((ah.at[i, "P"] - ah.at[i, "Book Prob"]) / (1-(ah.at[i, "Book Prob"]))/ahkellyDiv)
            if (np.isnan(ou.at[i, "P"])):
                curWeekWagers.append(0)
            if (ou.at[i, "P"] > ou.at[i, "Book Prob"]):
                if (ou.at[i, "Result"] == 1):
                    temp += (ou.at[i, "P"] - ou.at[i, "Book Prob"]) / (1-(ou.at[i, "Book Prob"]))*((1/ou.at[i, "Book Prob"]) - 1)/oukellyDiv
                    betSizes.append((ou.at[i, "P"] - ou.at[i, "Book Prob"]) / (1-(ou.at[i, "Book Prob"]))/oukellyDiv)
                    curWeekWagers.append((ou.at[i, "P"] - ou.at[i, "Book Prob"]) / (1-(ou.at[i, "Book Prob"]))/oukellyDiv)
                else:
                    temp -= (ou.at[i, "P"] - ou.at[i, "Book Prob"]) / (1-(ou.at[i, "Book Prob"]))/oukellyDiv
                    betSizes.append((ou.at[i, "P"] - ou.at[i, "Book Prob"]) / (1-(ou.at[i, "Book Prob"]))/oukellyDiv)
                    curWeekWagers.append((ou.at[i, "P"] - ou.at[i, "Book Prob"]) / (1-(ou.at[i, "Book Prob"]))/oukellyDiv)
            if (np.isnan(ml.at[i, "P"])):
                curWeekWagers.append(0)
            if (ml.at[i, "P"] > ml.at[i, "Book Prob"]):
                if (ml.at[i, "Result"] == 1):
                    temp += (ml.at[i, "P"] - ml.at[i, "Book Prob"]) / (1-(ml.at[i, "Book Prob"]))*((1/ml.at[i, "Book Prob"]) - 1)/mlkellyDiv
                    betSizes.append((ml.at[i, "P"] - ml.at[i, "Book Prob"]) / (1-(ml.at[i, "Book Prob"]))/mlkellyDiv)
                    curWeekWagers.append((ml.at[i, "P"] - ml.at[i, "Book Prob"]) / (1-(ml.at[i, "Book Prob"]))/mlkellyDiv)
                else:
                    temp -= (ml.at[i, "P"] - ml.at[i, "Book Prob"]) / (1-(ml.at[i, "Book Prob"]))/mlkellyDiv
                    betSizes.append((ml.at[i, "P"] - ml.at[i, "Book Prob"]) / (1-(ml.at[i, "Book Prob"]))/mlkellyDiv)
                    curWeekWagers.append((ml.at[i, "P"] - ml.at[i, "Book Prob"]) / (1-(ml.at[i, "Book Prob"]))/mlkellyDiv)
            if (i % 10 == 9):
                bankroll = bankroll * temp
                weekWagers.append(np.sum(curWeekWagers))
        curIter += 1
        if (bankroll - 1 > highestReturn):
            highestReturn = bankroll - 1
        if (bankroll - 1 < lowestReturn):
            lowestReturn = bankroll - 1
        endingReturns.append((bankroll - 1))
    print ("Level", k, "with ahDiv of", ahkellyDiv, "; ouDiv of", oukellyDiv, "; mlDiv of", mlkellyDiv)
    print ("Average Seasonal Return:", str(np.average(endingReturns)))
    print ("Standard Deviation:", np.std(endingReturns))
    print ("Lowest Observed Return:", max(lowestReturn,-1))
    print ("Highest Observed Return:", highestReturn)
    print ("Average Bet Size:", np.average(betSizes))
    print ("Average Bankroll Bets per Week:", np.average(weekWagers))
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
    # oukellyDiv *=  1.06
    # ahkellyDiv *=  1.06
    # mlkellyDiv *=  1.06
