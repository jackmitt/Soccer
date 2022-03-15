#import scrapers as scr
import data_manipulation as dm
#import predictions as pr
import evaluations as eval


leagues = ["England2","England3","England4","France1","France2","France3","Germany1","Germany2","Germany3","Italy1","Italy2","Spain1","Spain2"]
leagues = ["England1"]
for league in leagues:
    #print (league)
    #dm.preMatchAverages(league)
    #dm.train_test_split(league)
    #pr.WeibullCountDistPredictions(league)
    eval.analyzeWinRates(league, "AH", "Open")
    #pr.bayesian(league)
#r.fitWeibullParameters()
