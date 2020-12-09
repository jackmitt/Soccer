import pandas as pd
import numpy as np
from simultaneousDependentKelly import gradient_ascent

pred = pd.read_csv("./EPL_Csvs/3Game_newvars_no_T/resultsByEdge3Games.csv", encoding = "ISO-8859-1")

div = 10
betTypes = ["ML ", "AH ", "OU "]

for k in range(10):
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
        pred = pred.sample(frac=1).reset_index(drop=True)
        bankroll = 1
        for i in range(380):
            if (i % 10 == 0):
                temp = 1
                curWeekWagers = []
            for t in betTypes:
                if (not np.isnan(pred.at[i, t + "Kelly"])):
                    if (pred.at[i, t + "Kelly"]/div > 0.03):
                        continue
                    if (np.isnan(pred.at[i, t + "Result"])):
                        betSizes.append(pred.at[i, t + "Kelly"]/div)
                        curWeekWagers.append(pred.at[i, t + "Kelly"]/div)
                    elif (pred.at[i, t + "Result"] == 1):
                        temp += (pred.at[i, t + "Kelly"]*((1/pred.at[i, t + "Book Prob"]) - 1)/div)
                        betSizes.append(pred.at[i, t + "Kelly"]/div)
                        curWeekWagers.append(pred.at[i, t + "Kelly"]/div)
                    else:
                        temp -= (pred.at[i, t + "Kelly"]/div)
                        betSizes.append(pred.at[i, t + "Kelly"]/div)
                        curWeekWagers.append(pred.at[i, t + "Kelly"]/div)
            if (i % 10 == 9):
                bankroll = bankroll * temp
                weekWagers.append(np.sum(curWeekWagers))
        curIter += 1
        if (bankroll - 1 > highestReturn):
            highestReturn = bankroll - 1
        if (bankroll - 1 < lowestReturn):
            lowestReturn = bankroll - 1
        endingReturns.append((bankroll - 1))
    print ("Level", k, "with div of", div)
    print ("Average Seasonal Return:", str(np.average(endingReturns)))
    print ("Median Seasonal Return:", str(np.median(endingReturns)))
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
    div += 4
