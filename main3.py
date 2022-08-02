#import scrapers as scr
import data_manipulation as dm
#import predictions as pr
import evaluations as eval
import pandas as pd
import numpy as np
import pickle


leagues = ["Croatia1","Denmark1","Denmark2","England2","Germany1","Germany2","Netherlands1","Netherlands2","Poland1","Portugal1","Portugal2","Romania1","Scotland1","Slovakia1","Slovenia1","Spain1","Switzerland1","Turkey1"]
leagues = ["England1"]
for league in leagues:
    print ("-----------------------------------------------",league)
    with open("./csv_data/" + league + "/current/start_prior.pkl","rb") as inputFile:
        priors = pickle.load(inputFile)
    #    print (priors["offense"][0])
    #with open("./csv_data/" + league + "/last_prior_newSeason2.pkl","rb") as inputFile:
    #     priors = pickle.load(inputFile)
    #     print (priors["offense"][0])
    with open("./csv_data/" + league + "/current/teams_to_int.pkl","rb") as inputFile:
        teams_to_int = pickle.load(inputFile)
        print (teams_to_int)
    # train = pd.read_csv("./csv_data/" + league + "/betting_new.csv", encoding = "ISO-8859-1")
    # teams = train.Home.unique()
    # teams = np.sort(teams)
    # teams = pd.DataFrame(teams, columns=["team"])
    # teams["i"] = teams.index
    # #
    # teams_to_int = {}
    # for index, row in teams.iterrows():
    #     teams_to_int[row["team"]] = row["i"]
    for team in teams_to_int:
        print (team, priors["offense"][0][teams_to_int[team]], priors["defense"][0][teams_to_int[team]])
    print (priors["home"][0], priors["intercept"][0])
    #dm.preMatchAverages(league)
    #dm.train_test_split(league)
    #pr.WeibullCountDistPredictions(league)
    #eval.analyzeWinRates(league, "AH", "Open")
    #eval.analyzeWinRates(league, "AH", "Open", file = "/bayes_predictions_new.csv")
    #eval.analyzeWinRates(league, "OU", "Open", file = "/bayes_predictions_JAX.csv")
    #eval.kellybet(league, "AH", "Open", 20000, 12, 0.1, file = "/bayes_predictions_new.csv")
    #eval.kellybet(league, "AH", "Open", 20000, 12, 0.1, file = "/bayes_predictions_new.csv")
    #pr.bayesian(league)
    #eval.analyzeLineMovement(league, "AH", moveDirection = "renst")
    # train = pd.read_csv("./csv_data/" + league + "/betting.csv", encoding = "ISO-8859-1")
    # train = train.sort_values(by=["Date"], ignore_index = True)
    # train = train.rename(columns={"Home Score": "home_team_reg_score"})
    # train = train.rename(columns={"Away Score": "away_team_reg_score"})
    # teams = train.Home.unique()
    # teams = np.sort(teams)
    # teams = pd.DataFrame(teams, columns=["team"])
    # teams["i"] = teams.index
    # #
    # teams_to_int = {}
    # for index, row in teams.iterrows():
    #     teams_to_int[row["team"]] = row["i"]
    # #
    # priors["offense"][0] = list(priors["offense"][0])
    # priors["offense"][1] = list(priors["offense"][1])
    # priors["defense"][0] = list(priors["defense"][0])
    # priors["defense"][1] = list(priors["defense"][1])
    # priors["offense"][0][teams_to_int["Bournemouth AFC"]] = -0.2
    # priors["offense"][1][teams_to_int["Bournemouth AFC"]] = 0.075
    # priors["defense"][0][teams_to_int["Bournemouth AFC"]] = -0.2
    # priors["defense"][1][teams_to_int["Bournemouth AFC"]] = 0.075
    # # teams_to_int["Nottingham Forest"] = len(teams_to_int)
    # # with open("./csv_data/" + league + "/current/teams_to_int.pkl", "wb") as f:
    # #     pickle.dump(teams_to_int, f)
    # with open("./csv_data/" + league + "/current/start_prior.pkl", "wb") as f:
    #     pickle.dump(priors, f)
