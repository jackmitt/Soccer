#import scrapers as scr
import data_manipulation as dm
#import predictions as pr
import evaluations as eval


leagues = ["England1"]
for league in leagues:
    print (league)
    #dm.preMatchAverages(league)
    #dm.train_test_split(league)
    #pr.WeibullCountDistPredictions(league)
    eval.analyzeWinRates(league, "OU", "Close", "w_")
    #pr.bayesian(league)
#r.fitWeibullParameters()
