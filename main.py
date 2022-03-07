import scrapers as scr
import data_manipulation as dm
import predictions as pr
import evaluations as eval


leagues = ["England1","England2","England3","England4"]
for league in leagues:
    print (league)
    #dm.preMatchAverages(league)
    #dm.train_test_split(league)
    #pr.WeibullCountDistPredictions(league)
    eval.analyzeWinRates(league, "OU", "Open")
