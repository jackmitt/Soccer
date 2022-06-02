import pandas as pd
import numpy as np
import datetime
import pymc3 as pm
import theano.tensor as tt
import theano
from WeibullCountModelFunctions.MLE import MLE
from WeibullCountModelFunctions.WeibullPMF import weibullPmf
from WeibullCountModelFunctions.frankCopula import copula
from itertools import combinations
from scipy.stats import norm
import bayesianModelFcns as bmf
import pickle
import scrapers as scr
from os.path import exists
from bayesianModelFcns import bayesian_poisson_pdf
from helpers import grade_bets

def kellyStake(p, decOdds, kellyDiv):
    if ((p - (1 - p)/(decOdds - 1)) / kellyDiv > 0.05):
        return 0.05
    return ((p - (1 - p)/(decOdds - 1)) / kellyDiv)

def update(league):
    factor = 1.05                 # Expand the posteriors by this amount before using as priors
    f_thresh = 0.075         # A cap on team variable standard deviation to prevent blowup
    Δσ = 0.001               # The standard deviaton of the random walk variables


    if (exists("./csv_data/" + league + "/current/last_prior.pkl")):
        with open("./csv_data/" + league + "/current/last_prior.pkl","rb") as inputFile:
            priors = pickle.load(inputFile)
    else:
        with open("./csv_data/" + league + "/last_prior.pkl","rb") as inputFile:
            priors = pickle.load(inputFile)
    train = pd.read_csv("./csv_data/" + league + "/betting.csv", encoding = "ISO-8859-1")
    for i in range(len(train.index)):
        train.at[i, "Date"] = datetime.date(int(train.at[i, "Date"].split("-")[0]), int(train.at[i, "Date"].split("-")[1]), int(train.at[i, "Date"].split("-")[2]))
    train = train.sort_values(by=["Date"], ignore_index = True)
    train = train.rename(columns={"Home Score": "home_team_reg_score"})
    train = train.rename(columns={"Away Score": "away_team_reg_score"})
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


    train = pd.read_csv("./csv_data/" + league + "/current/results.csv", encoding = "ISO-8859-1")
    for i in range(len(train.index)):
        train.at[i, "Date"] = datetime.date(int(train.at[i, "Date"].split("-")[0]), int(train.at[i, "Date"].split("-")[1]), int(train.at[i, "Date"].split("-")[2]))
    finalDict = {}
    for col in train.columns:
        finalDict[col] = []

    if (exists("./csv_data/" + league + "/current/teams_to_int.pkl")):
        with open("./csv_data/" + league + "/current/teams_to_int.pkl","rb") as inputFile:
            teams_to_int = pickle.load(inputFile)
        num_teams = len(teams_to_int)


    tempDict = {"i_home":[],"i_away":[]}
    for index, row in train.iterrows():
        if (row["Home"] not in teams_to_int):
            priors["offense"][0].append(0)
            priors["offense"][1].append(0.075)
            priors["defense"][0].append(0)
            priors["defense"][1].append(0.075)
            teams_to_int[row["Home"]] = len(teams_to_int)
            num_teams += 1
            with open("./csv_data/" + league + "/current/teams_to_int.pkl", "wb") as f:
                pickle.dump(teams_to_int, f)
        if (row["Away"] not in teams_to_int):
            priors["offense"][0].append(0)
            priors["offense"][1].append(0.075)
            priors["defense"][0].append(0)
            priors["defense"][1].append(0.075)
            teams_to_int[row["Away"]] = len(teams_to_int)
            num_teams += 1
            with open("./csv_data/" + league + "/current/teams_to_int.pkl", "wb") as f:
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

    print (priors)

    startIndex = 0
    includedInPrior = []
    for index, row in train.iterrows():
        #print (row)
        for col in train.columns:
            if (col == "gw" or "i_" in col):
                continue
            finalDict[col].append(row[col])
        if (index == 0 and row["includedInPrior"] == 0):
            bmf.fatten_priors(priors, 1.33, f_thresh)
        if (index == 0):
            includedInPrior.append(1)
            continue
        if (row["includedInPrior"] == 0 and train.at[index-1,"includedInPrior"] == 1):
            startIndex = index
        if ((index == len(train.index) - 1 or row["gw"] - train.at[index+1,"gw"] == -1) and row["includedInPrior"] == 0):
            new_obs = train.iloc[startIndex:index+1]

            print (new_obs)

            home_team = theano.shared(new_obs.i_home.values)
            away_team = theano.shared(new_obs.i_away.values)

            observed_home_goals = new_obs.home_team_reg_score.values
            observed_away_goals = new_obs.away_team_reg_score.values


            posteriors = bmf.model_update(home_team, observed_home_goals, away_team, observed_away_goals, priors, num_teams, factor, f_thresh, Δσ)

            priors = posteriors

            startIndex = index + 1
        includedInPrior.append(1)
        with open("./csv_data/" + league + "/current/last_prior.pkl", "wb") as f:
            pickle.dump(priors, f)
    train = pd.read_csv("./csv_data/" + league + "/current/results.csv", encoding = "ISO-8859-1")
    train["includedInPrior"] = includedInPrior
    train.to_csv("./csv_data/" + league + "/current/results.csv", index = False)

def single_game_prediction(league, row, teams_to_int, decimals = 5):
    with open("./csv_data/" + league + "/current/last_prior.pkl","rb") as inputFile:
        posteriors = pickle.load(inputFile)
    precision = f".{decimals}f"
    game_pred = {"H_proj":[],"A_proj":[],"p_home_cover":[0],"p_over":[0]}
    idₕ = teams_to_int[row["Home"]]
    idₐ = teams_to_int[row["Away"]]
    i_μ = posteriors["intercept"][0]
    i_σ = posteriors["intercept"][1]
    h_μ = posteriors["home"][0]
    h_σ = posteriors["home"][1]
    oₕ_μ = posteriors["offense"][0][idₕ]
    oₕ_σ = posteriors["offense"][1][idₕ]
    oₐ_μ = posteriors["offense"][0][idₐ]
    oₐ_σ = posteriors["offense"][1][idₐ]
    dₕ_μ = posteriors["defense"][0][idₕ]
    dₕ_σ = posteriors["defense"][1][idₕ]
    dₐ_μ = posteriors["defense"][0][idₐ]
    dₐ_σ = posteriors["defense"][1][idₐ]
    # Normal(μ₁,σ₁²) + Normal(μ₂,σ₂²) = Normal(μ₁ + μ₂, σ₁² + σ₂²)
    log_λₕ_μ = i_μ + h_μ + oₕ_μ - dₐ_μ
    game_pred["H_proj"].append(np.exp(log_λₕ_μ))
    log_λₕ_σ = np.sqrt(i_σ ** 2 + h_σ ** 2 + oₕ_σ ** 2 + dₐ_σ ** 2)
    log_λₐ_μ = i_μ + oₐ_μ - dₕ_μ
    game_pred["A_proj"].append(np.exp(log_λₐ_μ))
    log_λₐ_σ = np.sqrt(i_σ ** 2 + oₐ_σ ** 2 + dₕ_σ ** 2)
    home_score_pdf = bayesian_poisson_pdf(log_λₕ_μ, log_λₕ_σ)
    away_score_pdf = bayesian_poisson_pdf(log_λₐ_μ, log_λₐ_σ)
    p_spaces = {"cover":0,"over":0}
    for sₕ, pₕ in enumerate(home_score_pdf):
        for sₐ, pₐ in enumerate(away_score_pdf):
            p = pₕ * pₐ

            for x in [""]:
                if (".5" in str(row[x + "AH"])):
                    p_spaces[x + "cover"] += p
                    if (sₕ > sₐ + row[x + "AH"]):
                        game_pred["p" + x + "_home_cover"][0] += p
                elif (".75" not in str(row[x + "AH"]) and ".25" not in str(row[x + "AH"])):
                    if (sₕ != sₐ + row[x + "AH"]):
                        p_spaces[x + "cover"] += p
                    if (sₕ > sₐ + row[x + "AH"]):
                        game_pred["p" + x + "_home_cover"][0] += p
                else:
                    parts = [row[x + "AH"] - 0.25,row[x + "AH"] + 0.25]
                    for part in parts:
                        if (".5" in str(part)):
                            p_spaces[x + "cover"] += p
                            if (sₕ > sₐ + part):
                                game_pred["p" + x + "_home_cover"][0] += p
                        else:
                            if (sₕ != sₐ + part):
                                p_spaces[x + "cover"] += p
                            if (sₕ > sₐ + part):
                                game_pred["p" + x + "_home_cover"][0] += p

                if (".5" in str(row[x + "OU"])):
                    p_spaces[x + "over"] += p
                    if (sₕ + sₐ > row[x + "OU"]):
                        game_pred["p" + x + "_over"][0] += p
                elif (".75" not in str(row[x + "OU"]) and ".25" not in str(row[x + "OU"])):
                    if (sₕ + sₐ != row[x + "OU"]):
                        p_spaces[x + "over"] += p
                    if (sₕ + sₐ > row[x + "OU"]):
                        game_pred["p" + x + "_over"][0] += p
                else:
                    parts = [row[x + "OU"] - 0.25,row[x + "OU"] + 0.25]
                    for part in parts:
                        if (".5" in str(part)):
                            p_spaces[x + "over"] += p
                            if (sₕ + sₐ > part):
                                game_pred["p" + x + "_over"][0] += p
                        else:
                            if (sₕ + sₐ != part):
                                p_spaces[x + "over"] += p
                            if (sₕ + sₐ > part):
                                game_pred["p" + x + "_over"][0] += p
    game_pred["p_home_cover"][0] = game_pred["p_home_cover"][0] / p_spaces["cover"]
    game_pred["p_over"][0] = game_pred["p_over"][0] / p_spaces["over"]
    return game_pred

def bet_on_pinny_games(league):
    if (exists("./csv_data/" + league + "/current/teams_to_int.pkl")):
        with open("./csv_data/" + league + "/current/teams_to_int.pkl","rb") as inputFile:
            teams_to_int = pickle.load(inputFile)
    else:
        train = pd.read_csv("./csv_data/" + league + "/betting.csv", encoding = "ISO-8859-1")
        for i in range(len(train.index)):
            train.at[i, "Date"] = datetime.date(int(train.at[i, "Date"].split("-")[0]), int(train.at[i, "Date"].split("-")[1]), int(train.at[i, "Date"].split("-")[2]))
        train = train.sort_values(by=["Date"], ignore_index = True)
        train = train.rename(columns={"Home Score": "home_team_reg_score"})
        train = train.rename(columns={"Away Score": "away_team_reg_score"})
        teams = train.Home.unique()
        teams = np.sort(teams)
        teams = pd.DataFrame(teams, columns=["team"])
        teams["i"] = teams.index

        teams_to_int = {}
        for index, row in teams.iterrows():
            teams_to_int[row["team"]] = row["i"]

    bankroll = 13000
    dict = {"Home":[],"Away":[],"H_proj":[],"A_proj":[],"pinny_AH":[],"pinny_home_AH_odds":[],"pinny_away_AH_odds":[],"pinny_OU":[],"pinny_over_odds":[],"pinny_under_odds":[],"p_home_cover":[],"p_over":[],"AH Bet":[],"AH Bet Amount":[],"AH Bet Odds":[],"AH Bet Book":[],"OU Bet":[],"OU Bet Amount":[],"OU Bet Odds":[],"OU Bet Book":[]}
    for index, row in scr.pinnacle(league).iterrows():
        dict["Home"].append(row["Home"])
        dict["Away"].append(row["Away"])
        dict["pinny_AH"].append(row["AH"])
        dict["pinny_home_AH_odds"].append(row["Home AH Odds"])
        dict["pinny_away_AH_odds"].append(row["Away AH Odds"])
        dict["pinny_OU"].append(row["OU"])
        dict["pinny_over_odds"].append(row["Over Odds"])
        dict["pinny_under_odds"].append(row["Under Odds"])
        game_pred = single_game_prediction(league,row,teams_to_int)
        for key in game_pred:
            dict[key].append(game_pred[key][0])
        if ((dict["pinny_home_AH_odds"][-1] - 1) * dict["p_home_cover"][-1] - (1 - dict["p_home_cover"][-1]) > 0.1):
            if (0-row["AH"] > 0):
                dict["AH Bet"].append(row["Home"] + " +" + str(0-row["AH"]))
            elif (0-row["AH"] < 0):
                dict["AH Bet"].append(row["Home"] + " " + str(0-row["AH"]))
            else:
                dict["AH Bet"].append(row["Home"] + " 0")
            dict["AH Bet Amount"].append(kellyStake(dict["p_home_cover"][-1], dict["pinny_home_AH_odds"][-1], 8) * bankroll)
            dict["AH Bet Odds"].append(row["Home AH Odds"])
            dict["AH Bet Book"].append("PS3838")
        elif ((dict["pinny_away_AH_odds"][-1] - 1) * (1 - dict["p_home_cover"][-1]) - (1 - (1 - dict["p_home_cover"][-1])) > 0.1):
            if (row["AH"] > 0):
                dict["AH Bet"].append(row["Away"] + " +" + str(row["AH"]))
            elif (row["AH"] < 0):
                dict["AH Bet"].append(row["Away"] + " " + str(row["AH"]))
            else:
                dict["AH Bet"].append(row["Away"] + " 0")
            dict["AH Bet Amount"].append(kellyStake(1-dict["p_home_cover"][-1], dict["pinny_away_AH_odds"][-1], 8) * bankroll)
            dict["AH Bet Odds"].append(row["Away AH Odds"])
            dict["AH Bet Book"].append("PS3838")
        else:
            dict["AH Bet"].append(np.nan)
            dict["AH Bet Amount"].append(np.nan)
            dict["AH Bet Odds"].append(np.nan)
            dict["AH Bet Book"].append(np.nan)
        if ((dict["pinny_over_odds"][-1] - 1) * dict["p_over"][-1] - (1 - dict["p_over"][-1]) > 0.1):
            dict["OU Bet"].append("Over")
            dict["OU Bet Amount"].append(kellyStake(dict["p_over"][-1], dict["pinny_over_odds"][-1], 8) * bankroll)
            dict["OU Bet Odds"].append(row["Over Odds"])
            dict["OU Bet Book"].append("PS3838")
        elif ((dict["pinny_under_odds"][-1] - 1) * (1 - dict["p_over"][-1]) - (1 - (1 - dict["p_over"][-1])) > 0.1):
            dict["OU Bet"].append("Under")
            dict["OU Bet Amount"].append(kellyStake(1-dict["p_over"][-1], dict["pinny_under_odds"][-1], 8) * bankroll)
            dict["OU Bet Odds"].append(row["Under Odds"])
            dict["OU Bet Book"].append("PS3838")
        else:
            dict["OU Bet"].append(np.nan)
            dict["OU Bet Amount"].append(np.nan)
            dict["OU Bet Odds"].append(np.nan)
            dict["OU Bet Book"].append(np.nan)
    df = pd.DataFrame.from_dict(dict)
    if (exists("./csv_data/" + league + "/current/bets.csv")):
        oldbets = pd.read_csv("./csv_data/" + league + "/current/bets.csv", encoding = "ISO-8859-1")
        oldbets = oldbets.append(df)
        oldbets.to_csv("./csv_data/" + league + "/current/bets.csv", index = False)
    else:
        df.to_csv("./csv_data/" + league + "/current/bets.csv", index = False)

def bet_adjustments(league):
    if (exists("./csv_data/" + league + "/current/teams_to_int.pkl")):
        with open("./csv_data/" + league + "/current/teams_to_int.pkl","rb") as inputFile:
            teams_to_int = pickle.load(inputFile)
    else:
        train = pd.read_csv("./csv_data/" + league + "/betting.csv", encoding = "ISO-8859-1")
        for i in range(len(train.index)):
            train.at[i, "Date"] = datetime.date(int(train.at[i, "Date"].split("-")[0]), int(train.at[i, "Date"].split("-")[1]), int(train.at[i, "Date"].split("-")[2]))
        train = train.sort_values(by=["Date"], ignore_index = True)
        train = train.rename(columns={"Home Score": "home_team_reg_score"})
        train = train.rename(columns={"Away Score": "away_team_reg_score"})
        teams = train.Home.unique()
        teams = np.sort(teams)
        teams = pd.DataFrame(teams, columns=["team"])
        teams["i"] = teams.index

        teams_to_int = {}
        for index, row in teams.iterrows():
            teams_to_int[row["team"]] = row["i"]

    bankroll = 13000
    dict = {"Home":[],"Away":[],"H_proj":[],"A_proj":[],"pinny_AH":[],"pinny_home_AH_odds":[],"pinny_away_AH_odds":[],"pinny_OU":[],"pinny_over_odds":[],"pinny_under_odds":[],"p_home_cover":[],"p_over":[],"AH Bet":[],"AH Bet Amount":[],"AH Bet Odds":[],"AH Bet Book":[],"OU Bet":[],"OU Bet Amount":[],"OU Bet Odds":[],"OU Bet Book":[]}
    for index, row in scr.pinnacle(league).iterrows():
        dict["Home"].append(row["Home"])
        dict["Away"].append(row["Away"])
        dict["pinny_AH"].append(row["AH"])
        dict["pinny_home_AH_odds"].append(row["Home AH Odds"])
        dict["pinny_away_AH_odds"].append(row["Away AH Odds"])
        dict["pinny_OU"].append(row["OU"])
        dict["pinny_over_odds"].append(row["Over Odds"])
        dict["pinny_under_odds"].append(row["Under Odds"])
        game_pred = single_game_prediction(league,row,teams_to_int)
        for key in game_pred:
            dict[key].append(game_pred[key][0])
        if ((dict["pinny_home_AH_odds"][-1] - 1) * dict["p_home_cover"][-1] - (1 - dict["p_home_cover"][-1]) > 0.1):
            if (0-row["AH"] > 0):
                dict["AH Bet"].append(row["Home"] + " +" + str(0-row["AH"]))
            elif (0-row["AH"] < 0):
                dict["AH Bet"].append(row["Home"] + " " + str(0-row["AH"]))
            else:
                dict["AH Bet"].append(row["Home"] + " 0")
            dict["AH Bet Amount"].append(kellyStake(dict["p_home_cover"][-1], dict["pinny_home_AH_odds"][-1], 8) * bankroll)
            dict["AH Bet Odds"].append(row["Home AH Odds"])
            dict["AH Bet Book"].append("PS3838")
        elif ((dict["pinny_away_AH_odds"][-1] - 1) * (1 - dict["p_home_cover"][-1]) - (1 - (1 - dict["p_home_cover"][-1])) > 0.1):
            if (row["AH"] > 0):
                dict["AH Bet"].append(row["Away"] + " +" + str(row["AH"]))
            elif (row["AH"] < 0):
                dict["AH Bet"].append(row["Away"] + " " + str(row["AH"]))
            else:
                dict["AH Bet"].append(row["Away"] + " 0")
            dict["AH Bet Amount"].append(kellyStake(1-dict["p_home_cover"][-1], dict["pinny_away_AH_odds"][-1], 8) * bankroll)
            dict["AH Bet Odds"].append(row["Away AH Odds"])
            dict["AH Bet Book"].append("PS3838")
        else:
            dict["AH Bet"].append(np.nan)
            dict["AH Bet Amount"].append(np.nan)
            dict["AH Bet Odds"].append(np.nan)
            dict["AH Bet Book"].append(np.nan)
        if ((dict["pinny_over_odds"][-1] - 1) * dict["p_over"][-1] - (1 - dict["p_over"][-1]) > 0.1):
            dict["OU Bet"].append("Over")
            dict["OU Bet Amount"].append(kellyStake(dict["p_over"][-1], dict["pinny_over_odds"][-1], 8) * bankroll)
            dict["OU Bet Odds"].append(row["Over Odds"])
            dict["OU Bet Book"].append("PS3838")
        elif ((dict["pinny_under_odds"][-1] - 1) * (1 - dict["p_over"][-1]) - (1 - (1 - dict["p_over"][-1])) > 0.1):
            dict["OU Bet"].append("Under")
            dict["OU Bet Amount"].append(kellyStake(1-dict["p_over"][-1], dict["pinny_under_odds"][-1], 8) * bankroll)
            dict["OU Bet Odds"].append(row["Under Odds"])
            dict["OU Bet Book"].append("PS3838")
        else:
            dict["OU Bet"].append(np.nan)
            dict["OU Bet Amount"].append(np.nan)
            dict["OU Bet Odds"].append(np.nan)
            dict["OU Bet Book"].append(np.nan)
    df = pd.DataFrame.from_dict(dict)
    oldbets = pd.read_csv("./csv_data/" + league + "/current/bets.csv", encoding = "ISO-8859-1")
    print ("------------------------------------------------")

    for index, row in oldbets.iterrows():
        if (row["AH Bet"] == row["AH Bet"] and row["AH Result"] != row["AH Result"]):
            for i, r in df.iterrows():
                if (r["Home"] == row["Home"] and r["Away"] == row["Away"]):
                    if ((row["pinny_home_AH_odds"] - 1) * row["p_home_cover"] - (1 - row["p_home_cover"]) > 0.1):
                        if (kellyStake(row["p_home_cover"], row["pinny_home_AH_odds"], 8) * bankroll > row["AH Bet Amount"]):
                            if (r["pinny_AH"] < row["pinny_AH"] or (r["pinny_AH"] == row["pinny_AH"] and r["pinny_home_AH_odds"] > row["pinny_home_AH_odds"])):
                                print (row["Home"], 0-float(r["pinny_AH"]), kellyStake(row["p_home_cover"], row["pinny_home_AH_odds"], 8) * bankroll - row["AH Bet Amount"])
                    elif ((row["pinny_away_AH_odds"] - 1) * (1 - row["p_home_cover"]) - (1 - (1 - row["p_home_cover"])) > 0.1):
                        if (kellyStake(1-row["p_home_cover"], row["pinny_away_AH_odds"], 8) * bankroll > row["AH Bet Amount"]):
                            if (r["pinny_AH"] > row["pinny_AH"] or (r["pinny_AH"] == row["pinny_AH"] and r["pinny_away_AH_odds"] > row["pinny_away_AH_odds"])):
                                print (row["Away"], float(r["pinny_AH"]), kellyStake(1-row["p_home_cover"], row["pinny_away_AH_odds"], 8) * bankroll - row["AH Bet Amount"])

leagues = ["Japan2","Brazil1","Brazil2"]
for league in leagues:
#league = "Norway1"
    scr.nowgoalCurSeason(league)
    print(grade_bets(league = league))
    update(league)
    bet_on_pinny_games(league)
#bet_adjustments(league)


