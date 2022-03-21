#import scrapers as scr
import data_manipulation as dm
#import predictions as pr
import evaluations as eval


leagues = ["Finland1"]
for league in leagues:
    print (league)
    #dm.preMatchAverages(league)
    #dm.train_test_split(league)
    #pr.WeibullCountDistPredictions(league)
    eval.analyzeWinRates(league, "AH", "Open", "")
    #pr.bayesian(league)
#r.fitWeibullParameters()
