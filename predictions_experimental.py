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
from os.path import exists
import os
import concurrent.futures


def bayesian():
    factor = 1.05                 # Expand the posteriors by this amount before using as priors -- old: 1.05
    f_thresh = 0.075         # A cap on team variable standard deviation to prevent blowup -- old: 0.075
    Δσ = 0.001               # The standard deviaton of the random walk variables -- old: 0.001

    for league in ["England1","England2","England3","England4"]:
        if (not exists("./csv_data/" + league + "/betting_years/")):
            os.makedirs("./csv_data/" + league + "/betting_years/")
            start_i = 0
            train = pd.read_csv("./csv_data/" + league + "/betting.csv", encoding = "ISO-8859-1")
            for i in range(len(train.index)):
                try:
                    train.at[i, "Date"] = datetime.date(int(train.at[i, "Date"].split("/")[2]), int(train.at[i, "Date"].split("/")[0]), int(train.at[i, "Date"].split("/")[1]))
                except:
                    train.at[i, "Date"] = datetime.date(int(train.at[i, "Date"].split("-")[0]), int(train.at[i, "Date"].split("-")[1]), int(train.at[i, "Date"].split("-")[2]))
            train = train.sort_values(by=["Date"], ignore_index = True)
            cur_year = 2008
            for i in range(len(train.index)):
                if (i == 0):
                    continue
                if ((train.at[i, "Date"].month in [7,8,9] and abs(train.at[i, "Date"] - train.at[i-1, "Date"]).days > 30) or i == len(train.index) - 1):
                    print (train.iloc[start_i:i])
                    train.iloc[start_i:i].to_csv("./csv_data/" + league + "/betting_years/" + str(cur_year) + ".csv", index = False)
                    start_i = i
                    cur_year += 1

    finalDict = {"League":[]}

    for year in ["2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020"]:
        if (exists("./csv_data/England/last_prior_year_end" + year + ".pkl")):
            with open("./csv_data/England/last_prior_year_end" + year + ".pkl","rb") as inputFile:
                priors = pickle.load(inputFile)
                posteriors = priors
            with open("./csv_data/England/teams_to_int_year_end" + year + ".pkl","rb") as inputFile:
                teams_to_int = pickle.load(inputFile)
            num_teams = len(teams_to_int.keys())
            teams_dict = {"team":[],"i":[]}
            for key in teams_to_int:
                teams_dict["i"].append(teams_to_int[key])
                teams_dict["team"].append(key)
            teams = pd.DataFrame.from_dict(teams_dict)
            finalDict = pd.read_csv("./csv_data/England/bayes_predictions_experimental.csv", encoding = "ISO-8859-1").to_dict(orient="list")
            oneIterComplete = True
            continue
        cur_league_dict = {1:[],2:[],3:[],4:[]}
        train = pd.read_csv("./csv_data/England1/betting_years/" + year + ".csv", encoding = "ISO-8859-1")
        cur_league_dict[1].extend(train.Home.unique())
        for league in ["England2","England3","England4"]:
            new_league = pd.read_csv("./csv_data/" + league + "/betting_years/" + year + ".csv", encoding = "ISO-8859-1")
            cur_league_dict[int(league.split("England")[1])].extend(new_league.Home.unique())
            train = train.append(new_league)
            if ("England4" == league and year != "2008"):
                for x in new_league.Home.unique():
                    if (x not in teams_to_int.keys()):
                        priors["offense"][0] = list(priors["offense"][0])
                        priors["offense"][1] = list(priors["offense"][1])
                        priors["defense"][0] = list(priors["defense"][0])
                        priors["defense"][1] = list(priors["defense"][1])
                        priors["offense"][0].append(-0.25)
                        priors["offense"][1].append(0.075)
                        priors["defense"][0].append(-0.25)
                        priors["defense"][1].append(0.075)
                        teams_to_int[x] = num_teams
                        teams.loc[len(teams.index)] = [x, num_teams]
                        num_teams += 1
                        with open("./csv_data/England/last_prior_year_start" + year + ".pkl", "wb") as f:
                            pickle.dump(priors, f)
                        with open("./csv_data/England/teams_to_int_year_start" + year + ".pkl", "wb") as f:
                            pickle.dump(teams_to_int, f)


        train = train.reset_index(drop=True)
        for i in range(len(train.index)):
            try:
                train.at[i, "Date"] = datetime.date(int(train.at[i, "Date"].split("/")[2]), int(train.at[i, "Date"].split("/")[0]), int(train.at[i, "Date"].split("/")[1]))
            except:
                train.at[i, "Date"] = datetime.date(int(train.at[i, "Date"].split("-")[0]), int(train.at[i, "Date"].split("-")[1]), int(train.at[i, "Date"].split("-")[2]))

        train = train.sort_values(by=["Date"], ignore_index = True)
        train = train.rename(columns={"Home Score": "home_team_reg_score"})
        train = train.rename(columns={"Away Score": "away_team_reg_score"})
        for i in range(len(train.index)):
            train.at[i, "Home"] = standardizeTeamName(train.at[i, "Home"], league)
            train.at[i, "Away"] = standardizeTeamName(train.at[i, "Away"], league)

        if (year == "2008"):
            teams = train.Home.unique()
            teams = np.sort(teams)
            teams = pd.DataFrame(teams, columns=["team"])
            teams["i"] = teams.index
            teams_to_int = {}
            for index, row in teams.iterrows():
                teams_to_int[row["team"]] = row["i"]

            num_teams = len(teams_to_int.keys())


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

        if (year == "2008"):
            for col in train.columns:
                finalDict[col] = []
            for col in ["H_proj","A_proj","p_1","p_X","p_2","p_Open_home_cover","p_Close_home_cover","p_Open_over","p_Close_over"]:
                finalDict[col] = []
            oneIterComplete = False
        start_index = 0
        if (year == "2008"):
            priors = {"home":[0.2,0.075],"intercept":[0.1,0.075],"offense":[[],[]],"defense":[[],[]]}
            for team in teams_to_int:
                if (team in cur_league_dict[1]):
                    priors["offense"][0].append(0.5)
                    priors["defense"][0].append(0.5)
                elif (team in cur_league_dict[2]):
                    priors["offense"][0].append(0.25)
                    priors["defense"][0].append(0.25)
                elif (team in cur_league_dict[3]):
                    priors["offense"][0].append(0)
                    priors["defense"][0].append(0)
                elif (team in cur_league_dict[4]):
                    priors["offense"][0].append(-0.25)
                    priors["defense"][0].append(-0.25)
                priors["offense"][1].append(0.075)
                priors["defense"][1].append(0.075)

        for index, row in train.iterrows():
            print (row["Date"])
            for col in train.columns:
                finalDict[col].append(row[col])
            for key in cur_league_dict:
                if (row["Home"] in cur_league_dict[key]):
                    finalDict["League"].append("England" + str(key))
            if (index != 0 and (row["gw"] - train.at[index-1,"gw"] == 1 or index == len(train.index) - 1)):
                new_obs = train.iloc[startIndex:index]
                print ("SLICE INDEXES:", startIndex, index)
                print (priors)
                home_team = aesara.shared(new_obs.i_home.values)
                away_team = aesara.shared(new_obs.i_away.values)
                team_pair = aesara.shared(new_obs.i_pair.values)

                observed_home_goals = new_obs.home_team_reg_score.values
                observed_away_goals = new_obs.away_team_reg_score.values

                posteriors = bmf.model_update(home_team, observed_home_goals, away_team, observed_away_goals, priors, num_teams, factor, f_thresh, Δσ)

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
        for key in finalDict:
            print (key, len(finalDict[key]))
        tempDF = pd.DataFrame.from_dict(finalDict)
        tempDF.to_csv("./csv_data/England/bayes_predictions_experimental.csv", index = False)
        with open("./csv_data/England/last_prior_year_end" + year + ".pkl", "wb") as f:
            pickle.dump(priors, f)
        with open("./csv_data/England/teams_to_int_year_end" + year + ".pkl", "wb") as f:
            pickle.dump(teams_to_int, f)
        return (1)

def reset_ram_run(*args, **kwargs):
    with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
        future = executor.submit(bayesian, *args, **kwargs)
        return future.result()

while (not exists("./csv_data/England/last_prior_year_end2020.pkl")):
    reset_ram_run()
