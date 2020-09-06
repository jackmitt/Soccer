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
6.5) Delete the T variables since those don't help the model/keeping this step so that first 5 games are already removed from the set
7) poissonRegression.R
8) bettingProbabilities.py
9) naiveEvaluation.py
10) regressionOnModelledEdge.R
11) bettingSims.py
12) seasonSim.py
