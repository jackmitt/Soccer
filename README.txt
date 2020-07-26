Order for recreating model from scratch:
1) get data either through scrapers or from the google drive backup
2) delete any duplicate games
3) combineMatchStats.py to merge whoscored and understat
4) combineOddsMatchStats.py to merge matchStats with EPLHistoricOddsWithElo
5) preMatchAverages.py
6) poissonFormat.py
7) poissonRegression.R
8) bettingProbabilities.py
