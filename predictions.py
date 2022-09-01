import pandas as pd
import numpy as np
import datetime
import pymc as pm
import pymc.sampling_jax
import aesara.tensor as tt
import aesara
import arviz as az
import gc
from WeibullCountModelFunctions.MLE import MLE
from WeibullCountModelFunctions.WeibullPMF import weibullPmf
from WeibullCountModelFunctions.frankCopula import copula
from itertools import combinations
from scipy.stats import norm
import bayesianModelFcns as bmf
import pickle
from helpers import standardizeTeamName


def bayesian(league):
    factor = 1.05                 # Expand the posteriors by this amount before using as priors -- old: 1.05
    f_thresh = 0.075         # A cap on team variable standard deviation to prevent blowup -- old: 0.075
    Δσ = 0.001               # The standard deviaton of the random walk variables -- old: 0.001

    # with open("./csv_data/" + league + "/last_prior.pkl","rb") as inputFile:
    #     priors = pickle.load(inputFile)

    # club_vals = pd.read_csv("./csv_data/" + league + "/transfermarkt.csv", encoding = "UTF-8")
    # club_val_map = {}
    # for index, row in club_vals.iterrows():
    #     if (row["Season"] not in club_val_map):
    #         club_val_map[row["Season"]] = {}
    #     fix = ""
    #     for i in range(len(row["Team"].split())):
    #         fix = fix + row["Team"].split()[i]
    #         if (i != len(row["Team"].split()) - 1):
    #             fix = fix + " "
    #     if ("Th." in row["Value"][1:]):
    #         club_val_map[row["Season"]][standardizeTeamName(fix,league)] = float(row["Value"][1:].split("Th")[0]) / 1000
    #     else:
    #         club_val_map[row["Season"]][standardizeTeamName(fix,league)] = float(row["Value"][1:].split("m")[0])
    #
    # print (club_val_map)

    train = pd.read_csv("./csv_data/" + league + "/betting.csv", encoding = "ISO-8859-1")
    for i in range(len(train.index)):
        try:
            train.at[i, "Date"] = datetime.date(int(train.at[i, "Date"].split("/")[2]), int(train.at[i, "Date"].split("/")[0]), int(train.at[i, "Date"].split("/")[1]))
        except:
            train.at[i, "Date"] = datetime.date(int(train.at[i, "Date"].split("-")[0]), int(train.at[i, "Date"].split("-")[1]), int(train.at[i, "Date"].split("-")[2]))
    train = train.sort_values(by=["Date"], ignore_index = True)
    finalDict = {}
    train = train.rename(columns={"Home Score": "home_team_reg_score"})
    train = train.rename(columns={"Away Score": "away_team_reg_score"})
    for i in range(len(train.index)):
        train.at[i, "Home"] = standardizeTeamName(train.at[i, "Home"], league)
        train.at[i, "Away"] = standardizeTeamName(train.at[i, "Away"], league)
    teams = train.Home.unique()
    teams = np.sort(teams)
    teams = pd.DataFrame(teams, columns=["team"])
    teams["i"] = teams.index


    teams_to_int = {}
    for index, row in teams.iterrows():
        teams_to_int[row["team"]] = row["i"]

    print (teams_to_int)

    all_teams_pair_combinations = combinations(teams['team'], 2)
    team_pairs_dict = {}
    team_pairs_heads_dict = {}
    pair_index = 0
    for pair in all_teams_pair_combinations:
        team_pairs_dict[(pair[0], pair[1])] = pair_index
        team_pairs_dict[(pair[1], pair[0])] = pair_index
        team_pairs_heads_dict[(pair[0], pair[1])] = pair[0]
        team_pairs_heads_dict[(pair[1], pair[0])] = pair[0]
        pair_index += 1

    train = train.merge(teams, left_on='Home', right_on='team', how='left')
    train = train.rename(columns={'i': 'i_home'}).drop('team', axis=1)
    train = train.merge(teams, left_on='Away', right_on='team', how='left')
    train = train.rename(columns={'i': 'i_away'}).drop('team', axis=1)
    train['i_pair'] = train.apply(lambda row: team_pairs_dict[(row['Home'], row['Away'])], axis=1)

    gwCount = 0
    gws = []
    for index, row in train.iterrows():
        if (index == 0):
            startIndex = 0
        elif (index != 0 and abs(train.at[startIndex,"Date"] - train.at[index,"Date"]).days > 3):
            gwCount += 1
            startIndex = index
        gws.append(gwCount)
    train["gw"] = gws

    for index, row in train.iterrows():
        if (index != 0 and abs(train.at[index,"Date"] - train.at[index-1,"Date"]).days > 40 and train.at[index,"Date"].year == 2012):
            splitIndex = index
        gws.append(gwCount)

    for col in train.columns:
        finalDict[col] = []
    for col in ["H_proj","A_proj","p_1","p_X","p_2","p_Open_home_cover","p_Close_home_cover","p_Open_over","p_Close_over"]:
        finalDict[col] = []


    num_teams = len(train.i_home.drop_duplicates())
    num_team_pairs = len(train.i_pair.drop_duplicates())

    warmUp = train.iloc[:splitIndex]
    train = train.iloc[splitIndex:]

    home_team = aesara.shared(warmUp.i_home.values)
    away_team = aesara.shared(warmUp.i_away.values)
    team_pair = aesara.shared(warmUp.i_pair.values)

    observed_home_goals = warmUp.home_team_reg_score.values
    observed_away_goals = warmUp.away_team_reg_score.values

    with pm.Model() as model:
        home = pm.Flat('home')
        sd_offense = pm.HalfStudentT('sd_offense', nu=3, sigma=2.5)
        sd_defense = pm.HalfStudentT('sd_defense', nu=3, sigma=2.5)
        intercept = pm.Flat('intercept')

        offense_star = pm.Normal('offense_star', mu=0, sigma=sd_offense, shape=num_teams)
        defense_star = pm.Normal('defense_star', mu=0, sigma=sd_defense, shape=num_teams)
        offense = pm.Deterministic('offense', offense_star - tt.mean(offense_star))
        defense = pm.Deterministic('defense', defense_star - tt.mean(defense_star))
        home_theta = tt.exp(intercept + home + offense[home_team] - defense[away_team])
        away_theta = tt.exp(intercept + offense[away_team] - defense[home_team])


        home_goals = pm.Poisson('home_goals', mu=home_theta, observed=observed_home_goals)
        away_goals = pm.Poisson('away_goals', mu=away_theta, observed=observed_away_goals)

    with model:
        trace = pm.sampling_jax.sample_numpyro_nuts(5000, tune=2000)
        # #print (trace.posterior.stack(sample=["chain", "draw"]).sample)
        # print (trace.posterior.mean(dim=["chain","draw"]))
        # tracedict = {"home":[],"intercept":[],"offense":[],"defense":[]}
        # #prints arrays of length 39
        # # for a in trace.posterior["offense"]:
        # #     print ("----------------------------")
        # #     for b in a.data:
        # #         print (b)
        # for a in trace.posterior["offense"]:
        #     print ("----------------------------")
        #     print (len(a.data))
        # #print (trace.to_dict())
        priors = bmf.get_model_posteriors(trace, num_teams)

    print (priors)
    oneIterComplete = False
    startIndex = 0
    new_teams = {}

    for index, row in train.iterrows():
        print (row["Date"])
        for col in train.columns:
            finalDict[col].append(row[col])
        # if (index != splitIndex and abs(row["Date"] - train.at[index-1,"Date"]).days > 30):
        #     bmf.fatten_priors(priors, 1.33, f_thresh)
        #THIS ONLY WORKS FOR 1 YEAR LEAGUES, NEED TO HARD CODE SEASONS FOR OTHER LEAGUES
        # if (index != splitIndex and row["Season"] != train.at[index-1,"Season"]):
        #     new_teams = {}
        #     #adjust priors for newly promoted/demoted teams based on market value *starting in 2013
        #     curYear = row["Date"].year
        #     if (curYear >= 2013):
        #         curOffStd = np.std(priors["offense"][0])
        #         curDefStd = np.std(priors["defense"][0])
        #         curVals = []
        #         for team in club_val_map[curYear]:
        #             curVals.append(club_val_map[curYear][team])
        #         curValsMean = np.average(curVals)
        #         curValsStd = np.std(curVals)
        #         for team in club_val_map[curYear]:
        #             if (team not in club_val_map[curYear-1]):
        #                 new_teams[teams_to_int[team]] = 0
        #                 val_z = (club_val_map[curYear][team] - curValsMean) / curValsStd
        #                 priors["offense"][0][teams_to_int[team]] = curOffStd * val_z / 4
        #                 priors["defense"][0][teams_to_int[team]] = curDefStd * val_z / 4
        if (index != splitIndex and row["gw"] - train.at[index-1,"gw"] == 1):

            # for i in range(len(priors["offense"][0])):
            #     if (i in new_teams and new_teams[i] <= 10):
            #         priors["offense"][1][i] = priors["offense"][1][i] * 2
            #         priors["defense"][1][i] = priors["defense"][1][i] * 2

            new_obs = train.iloc[startIndex:index]
            print ("SLICE INDEXES:", startIndex, index)
            home_team = aesara.shared(new_obs.i_home.values)
            away_team = aesara.shared(new_obs.i_away.values)
            team_pair = aesara.shared(new_obs.i_pair.values)

            observed_home_goals = new_obs.home_team_reg_score.values
            observed_away_goals = new_obs.away_team_reg_score.values

            posteriors = bmf.model_update(home_team, observed_home_goals, away_team, observed_away_goals, priors, num_teams, factor, f_thresh, Δσ)

            priors = posteriors

            for team in new_obs.i_home.values:
                if (team in new_teams):
                    new_teams[team] += 1
            for team in new_obs.i_away.values:
                if (team in new_teams):
                    new_teams[team] += 1

            startIndex = index
            oneIterComplete = True
        if (oneIterComplete):
            curPred = bmf.single_game_prediction(row, posteriors, teams_to_int, decimals = 5)
            for key in curPred:
                finalDict[key].append(curPred[key][0])
        else:
            for col in ["H_proj","A_proj","p_1","p_X","p_2","p_Open_home_cover","p_Close_home_cover","p_Open_over","p_Close_over"]:
                finalDict[col].append(np.nan)
        tempDF = pd.DataFrame.from_dict(finalDict)
        tempDF.to_csv("./csv_data/" + league + "/bayes_predictions_newGood.csv", index = False)
        with open("./csv_data/" + league + "/last_prior_newSeasonGood.pkl", "wb") as f:
            pickle.dump(priors, f)


def bayesian_new_season(league):
    factor = 1.05                 # Expand the posteriors by this amount before using as priors
    f_thresh = 0.075         # A cap on team variable standard deviation to prevent blowup
    Δσ = 0.001               # The standard deviaton of the random walk variables


    with open("./csv_data/" + league + "/last_prior.pkl","rb") as inputFile:
        priors = pickle.load(inputFile)
    train = pd.read_csv("./csv_data/" + league + "/betting.csv", encoding = "ISO-8859-1")
    for i in range(len(train.index)):
        try:
            train.at[i, "Date"] = datetime.date(int(train.at[i, "Date"].split("-")[0]), int(train.at[i, "Date"].split("-")[1]), int(train.at[i, "Date"].split("-")[2]))
        except:
            train.at[i, "Date"] = datetime.date(int(train.at[i, "Date"].split("/")[2]), int(train.at[i, "Date"].split("/")[0]), int(train.at[i, "Date"].split("/")[1]))
    train = train.sort_values(by=["Date"], ignore_index = True)
    train = train.rename(columns={"Home Score": "home_team_reg_score"})
    train = train.rename(columns={"Away Score": "away_team_reg_score"})
    for i in range(len(train.index)):
        train.at[i, "Home"] = standardizeTeamName(train.at[i, "Home"], league)
        train.at[i, "Away"] = standardizeTeamName(train.at[i, "Away"], league)
    teams = train.Home.unique()
    teams = np.sort(teams)
    teams = pd.DataFrame(teams, columns=["team"])
    teams["i"] = teams.index

    teams_to_int = {}
    for index, row in teams.iterrows():
        teams_to_int[row["team"]] = row["i"]

    all_teams_pair_combinations = combinations(teams['team'], 2)
    team_pairs_dict = {}
    team_pairs_heads_dict = {}
    pair_index = 0
    for pair in all_teams_pair_combinations:
        team_pairs_dict[(pair[0], pair[1])] = pair_index
        team_pairs_dict[(pair[1], pair[0])] = pair_index
        team_pairs_heads_dict[(pair[0], pair[1])] = pair[0]
        team_pairs_heads_dict[(pair[1], pair[0])] = pair[0]
        pair_index += 1

    train = train.merge(teams, left_on='Home', right_on='team', how='left')
    train = train.rename(columns={'i': 'i_home'}).drop('team', axis=1)
    train = train.merge(teams, left_on='Away', right_on='team', how='left')
    train = train.rename(columns={'i': 'i_away'}).drop('team', axis=1)
    train['i_pair'] = train.apply(lambda row: team_pairs_dict[(row['Home'], row['Away'])], axis=1)

    num_teams = len(train.i_home.drop_duplicates())
    num_team_pairs  = len(train.i_pair.drop_duplicates())


    train_new = pd.read_csv("./csv_data/" + league + "/betting_new.csv", encoding = "ISO-8859-1")
    train = train_new.iloc[len(train.index):]
    train = train.reset_index(drop=True)
    for i in range(len(train.index)):
        try:
            train.at[i, "Date"] = datetime.date(int(train.at[i, "Date"].split("-")[0]), int(train.at[i, "Date"].split("-")[1]), int(train.at[i, "Date"].split("-")[2]))
        except:
            train.at[i, "Date"] = datetime.date(int(train.at[i, "Date"].split("/")[2]), int(train.at[i, "Date"].split("/")[0]), int(train.at[i, "Date"].split("/")[1]))
    train = train.sort_values(by=["Date"], ignore_index = True)
    train = train.rename(columns={"Home Score": "home_team_reg_score"})
    train = train.rename(columns={"Away Score": "away_team_reg_score"})
    finalDict = {}
    for col in train.columns:
        finalDict[col] = []
    for col in ["H_proj","A_proj","p_1","p_X","p_2","p_Open_home_cover","p_Close_home_cover","p_Open_over","p_Close_over"]:
        finalDict[col] = []



    #ISSUE WHEN TEAMS NAMES WERE UPDATED FROM YEAR TO YEAR - GOING TO PRINT NEW NAME AND LET THERE BE AN ERROR THROWN
    #UPDATING AUTOMATICALLY ERASES OLD PRIORS IF TEAM NAME CHANGE
    tempDict = {"i_home":[],"i_away":[]}
    for index, row in train.iterrows():
        if (row["Home"] not in teams_to_int):
            priors["offense"][0] = list(priors["offense"][0])
            priors["offense"][1] = list(priors["offense"][1])
            priors["defense"][0] = list(priors["defense"][0])
            priors["defense"][1] = list(priors["defense"][1])
            for i in range(1000):
                print ("ERROR:", row["Home"])
            priors["offense"][0].append(0)
            priors["offense"][1].append(0.075)
            priors["defense"][0].append(0)
            priors["defense"][1].append(0.075)
            teams_to_int[row["Home"]] = len(teams_to_int)
            num_teams += 1
            with open("./csv_data/" + league + "/teams_to_int_NEW.pkl", "wb") as f:
                pickle.dump(teams_to_int, f)
        if (row["Away"] not in teams_to_int):
            priors["offense"][0] = list(priors["offense"][0])
            priors["offense"][1] = list(priors["offense"][1])
            priors["defense"][0] = list(priors["defense"][0])
            priors["defense"][1] = list(priors["defense"][1])
            for i in range(1000):
                print ("ERROR:", row["Away"])
            priors["offense"][0].append(0)
            priors["offense"][1].append(0.075)
            priors["defense"][0].append(0)
            priors["defense"][1].append(0.075)
            teams_to_int[row["Away"]] = len(teams_to_int)
            num_teams += 1
            with open("./csv_data/" + league + "/teams_to_int_NEW.pkl", "wb") as f:
                pickle.dump(teams_to_int, f)
        tempDict["i_home"].append(teams_to_int[row["Home"]])
        tempDict["i_away"].append(teams_to_int[row["Away"]])
    train["i_home"] = tempDict["i_home"]
    train["i_away"] = tempDict["i_away"]

    gwCount = 0
    gws = []
    for index, row in train.iterrows():
        if (index == 0):
            startIndex = 0
        elif (index != 0 and abs(train.at[startIndex,"Date"] - train.at[index,"Date"]).days > 3):
            gwCount += 1
            startIndex = index
        gws.append(gwCount)
    train["gw"] = gws

    #print (priors)

    startIndex = 0
    for index, row in train.iterrows():
        #print (row)
        for col in train.columns:
            if (col == "gw" or "i_" in col):
                continue
            finalDict[col].append(row[col])
        curPred = bmf.single_game_prediction(row, priors, teams_to_int, decimals = 5)
        for key in curPred:
            finalDict[key].append(curPred[key][0])
        if ((index == len(train.index) - 1 or row["gw"] - train.at[index+1,"gw"] == -1)):
            new_obs = train.iloc[startIndex:index+1]

            print (new_obs)

            home_team = aesara.shared(new_obs.i_home.values)
            away_team = aesara.shared(new_obs.i_away.values)

            observed_home_goals = new_obs.home_team_reg_score.values
            observed_away_goals = new_obs.away_team_reg_score.values


            posteriors = bmf.model_update(home_team, observed_home_goals, away_team, observed_away_goals, priors, num_teams, factor, f_thresh, Δσ)

            priors = posteriors

            startIndex = index + 1
        with open("./csv_data/" + league + "/last_prior_newSeason_notJax.pkl", "wb") as f:
            pickle.dump(priors, f)
        tempDF = pd.DataFrame.from_dict(finalDict)
        tempDF.to_csv("./csv_data/" + league + "/bayes_predictions_new_notJax.csv", index = False)


def bayesian_xg(league):
    factor = 1.05                 # Expand the posteriors by this amount before using as priors -- old: 1.05
    f_thresh = 0.075         # A cap on team variable standard deviation to prevent blowup -- old: 0.075
    Δσ = 0.001               # The standard deviaton of the random walk variables -- old: 0.001

    with open("./csv_data/" + league + "/last_prior.pkl","rb") as inputFile:
        priors = pickle.load(inputFile)

    train = pd.read_csv("./csv_data/" + league + "/betting_xg.csv", encoding = "ISO-8859-1")
    for i in range(len(train.index)):
        try:
            train.at[i, "Date"] = datetime.date(int(train.at[i, "Date"].split("/")[2]), int(train.at[i, "Date"].split("/")[0]), int(train.at[i, "Date"].split("/")[1]))
        except:
            train.at[i, "Date"] = datetime.date(int(train.at[i, "Date"].split("-")[0]), int(train.at[i, "Date"].split("-")[1]), int(train.at[i, "Date"].split("-")[2]))
    train = train.sort_values(by=["Date"], ignore_index = True)
    finalDict = {}
    train = train.rename(columns={"Home Score": "home_team_reg_score"})
    train = train.rename(columns={"Away Score": "away_team_reg_score"})
    for i in range(len(train.index)):
        train.at[i, "Home"] = standardizeTeamName(train.at[i, "Home"], league)
        train.at[i, "Away"] = standardizeTeamName(train.at[i, "Away"], league)
    teams = train.Home.unique()
    teams = np.sort(teams)
    teams = pd.DataFrame(teams, columns=["team"])
    teams["i"] = teams.index


    teams_to_int = {}
    for index, row in teams.iterrows():
        teams_to_int[row["team"]] = row["i"]

    print (teams_to_int)

    all_teams_pair_combinations = combinations(teams['team'], 2)
    team_pairs_dict = {}
    team_pairs_heads_dict = {}
    pair_index = 0
    for pair in all_teams_pair_combinations:
        team_pairs_dict[(pair[0], pair[1])] = pair_index
        team_pairs_dict[(pair[1], pair[0])] = pair_index
        team_pairs_heads_dict[(pair[0], pair[1])] = pair[0]
        team_pairs_heads_dict[(pair[1], pair[0])] = pair[0]
        pair_index += 1

    train = train.merge(teams, left_on='Home', right_on='team', how='left')
    train = train.rename(columns={'i': 'i_home'}).drop('team', axis=1)
    train = train.merge(teams, left_on='Away', right_on='team', how='left')
    train = train.rename(columns={'i': 'i_away'}).drop('team', axis=1)
    train['i_pair'] = train.apply(lambda row: team_pairs_dict[(row['Home'], row['Away'])], axis=1)

    gwCount = 0
    gws = []
    for index, row in train.iterrows():
        if (index == 0):
            startIndex = 0
        elif (index != 0 and abs(train.at[startIndex,"Date"] - train.at[index,"Date"]).days > 3):
            gwCount += 1
            startIndex = index
        gws.append(gwCount)
    train["gw"] = gws

    for index, row in train.iterrows():
        if (index != 0 and abs(train.at[index,"Date"] - train.at[index-1,"Date"]).days > 40 and train.at[index,"Date"].year == 2017):
            splitIndex = index
        gws.append(gwCount)

    for col in train.columns:
        finalDict[col] = []
    for col in ["H_proj","A_proj","p_1","p_X","p_2","p_Open_home_cover","p_Close_home_cover","p_Open_over","p_Close_over"]:
        finalDict[col] = []


    num_teams = len(train.i_home.drop_duplicates())
    num_team_pairs = len(train.i_pair.drop_duplicates())

    warmUp = train.iloc[:splitIndex]
    train = train.iloc[splitIndex:]

    home_team = aesara.shared(warmUp.i_home.values)
    away_team = aesara.shared(warmUp.i_away.values)
    team_pair = aesara.shared(warmUp.i_pair.values)

    observed_home_goals = warmUp.home_team_reg_score.values
    observed_away_goals = warmUp.away_team_reg_score.values

    with pm.Model() as model:
        home = pm.Flat('home')
        sd_offense = pm.HalfStudentT('sd_offense', nu=3, sigma=2.5)
        sd_defense = pm.HalfStudentT('sd_defense', nu=3, sigma=2.5)
        intercept = pm.Flat('intercept')

        offense_star = pm.Normal('offense_star', mu=0, sigma=sd_offense, shape=num_teams)
        defense_star = pm.Normal('defense_star', mu=0, sigma=sd_defense, shape=num_teams)
        offense = pm.Deterministic('offense', offense_star - tt.mean(offense_star))
        defense = pm.Deterministic('defense', defense_star - tt.mean(defense_star))
        home_theta = tt.exp(intercept + home + offense[home_team] - defense[away_team])
        away_theta = tt.exp(intercept + offense[away_team] - defense[home_team])


        home_goals = pm.Poisson('home_goals', mu=home_theta, observed=observed_home_goals)
        away_goals = pm.Poisson('away_goals', mu=away_theta, observed=observed_away_goals)

    with model:
        trace = pm.sampling_jax.sample_numpyro_nuts(5000, tune=2000)
        # #print (trace.posterior.stack(sample=["chain", "draw"]).sample)
        # print (trace.posterior.mean(dim=["chain","draw"]))
        # tracedict = {"home":[],"intercept":[],"offense":[],"defense":[]}
        # #prints arrays of length 39
        # # for a in trace.posterior["offense"]:
        # #     print ("----------------------------")
        # #     for b in a.data:
        # #         print (b)
        # for a in trace.posterior["offense"]:
        #     print ("----------------------------")
        #     print (len(a.data))
        # #print (trace.to_dict())
        priors = bmf.get_model_posteriors(trace, num_teams)

    oneIterComplete = False
    startIndex = 0
    new_teams = {}

    for index, row in train.iterrows():
        print (row["Date"])
        for col in train.columns:
            finalDict[col].append(row[col])
        if (index != splitIndex and row["gw"] - train.at[index-1,"gw"] == 1):

            new_obs = train.iloc[startIndex:index]
            print ("SLICE INDEXES:", startIndex, index)
            home_team = aesara.shared(new_obs.i_home.values)
            away_team = aesara.shared(new_obs.i_away.values)
            team_pair = aesara.shared(new_obs.i_pair.values)

            observed_home_goals = new_obs.h_xg.values
            observed_away_goals = new_obs.a_xg.values

            posteriors = bmf.model_update(home_team, observed_home_goals, away_team, observed_away_goals, priors, num_teams, factor, f_thresh, Δσ, xgUpdate = True)

            priors = posteriors

            startIndex = index
            oneIterComplete = True
        if (oneIterComplete):
            curPred = bmf.single_game_prediction(row, posteriors, teams_to_int, decimals = 5)
            for key in curPred:
                finalDict[key].append(curPred[key][0])
        else:
            for col in ["H_proj","A_proj","p_1","p_X","p_2","p_Open_home_cover","p_Close_home_cover","p_Open_over","p_Close_over"]:
                finalDict[col].append(np.nan)
        tempDF = pd.DataFrame.from_dict(finalDict)
        tempDF.to_csv("./csv_data/" + league + "/bayes_predictions_xg.csv", index = False)
        with open("./csv_data/" + league + "/last_prior_xg.pkl", "wb") as f:
            pickle.dump(priors, f)
