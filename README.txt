Order for recreating model from scratch:
1) get data either through scrapers or from the google drive backup
2) delete any duplicate games
2.5) Sort files by date
3) combineMatchStats.py to merge whoscored and understat; combineOdds.py to merge 1x2, ah, ou
3.5) eloGen.py
4) combineOddsMatchStats.py to merge matchStats with EPLHistoricOddsWithElo
5) preMatchAverages.py
6) poissonFormat.py
6.5) Delete the T variables since those don't help the model/keeping this step so that first 5 games are already removed from the set
7) poissonRegression.R
8) bettingProbabilities.py
9) naiveEvaluation.py
10) regressionOnModelledEdge.R
11) bettingSims.py
