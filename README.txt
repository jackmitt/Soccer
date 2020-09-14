Order for recreating model from scratch:
1) get data either through scrapers or from the google drive backup
1.5) fix understat dates, sort files by date, delete the dataframe index rows
2) delete any duplicate games
3) combineMatchStats.py to merge whoscored and understat; combineOdds.py to merge 1x2, ah, ou
3.5) eloGen.py
4) combineOddsMatchStats.py to merge matcStats with EPLHistoricOddsWithElo
4.5) delete columns containing old indices
5) preMatchAverages.py
6) poissonFormat.py
6.5) trainTestSplit.py if applicable
7) poissonRegression.R
***) PoissonMeansForWeibull.py then WeibullCountDist.py then fix dates if necessary in WeibullPredictions.csv
8) bettingProbabilities.py/weibullBettingProbabilities.py
9) naiveEvaluation.py
10) regressionOnModelledEdge.R
11) bettingSims.py
12) seasonSim.py
