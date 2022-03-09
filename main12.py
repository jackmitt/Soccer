import scrapers as scr
import data_manipulation as dm
import predictions as pr
import evaluations as eval

leagues = ["Algeria1","Australia1","Australia2","Brazil1","Brazil2","Czech1","Czech2","Denmark1","Denmark2","England1","England2","England3","England4","Finland1","Finland2","France1","France2","France3","Germany1","Germany2","Germany3","Iran1","Italy1","Italy2","Japan1","Japan2","Korea1","Morocco1","Netherlands1","Netherlands2","Norway1","Norway2","Qatar1","Singapore1","SouthAfrica1","Spain1","Spain2","Sweden1","Sweden2","UAE1","USA1"]
for league in leagues:
    print (league)
    #dm.preMatchAverages(league)
    #dm.train_test_split(league)
    #pr.WeibullCountDistPredictions(league)
    eval.analyzeWinRates(league, "AH", "Open")
