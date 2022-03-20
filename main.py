#import scrapers as scr
import data_manipulation as dm
import predictions as pr
import evaluations as eval


leagues = ["NorthernIreland1","Norway1","Norway2","Sweden1","Sweden2","Finland1","Finland2"]
for league in leagues:
    #print (league)
    #dm.preMatchAverages(league)
    #dm.train_test_split(league)
    #pr.WeibullCountDistPredictions(league)
    #eval.analyzeWinRates(league, "AH", "Open")
    pr.bayesian(league)
#r.fitWeibullParameters()
