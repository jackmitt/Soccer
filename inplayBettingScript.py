import pandas as pd
import numpy as np
import datetime
import pymc3 as pm
import theano.tensor as tt
import theano
from itertools import combinations
from scipy.stats import norm
import bayesianModelFcns as bmf
import pickle
import scrapers as scr
from os.path import exists
from bayesianModelFcns import bayesian_poisson_pdf
import asian_odds_api as api
from helpers import standardizeTeamName
from helpers import convert_league
import math
import time

#where d0 is the avg odds already bet, d1 is the quoted odds, k0 is the stake already bet (in pct of bankroll) at d0 odds
#returns pct of bankroll you should bet at d1 odds on top of k0 @ d0
#algebraically derived from the kelly criterion
#if negative, then don't bet any more at the current odds
def new_kelly(p, d0, d1, k0, kellyDiv):
    #simplifying constants
    x = d0 * k0*kellyDiv
    y = p - k0*kellyDiv
    z = 1 - p

    #quadratic coefs
    a = 1 - d1
    b = k0*kellyDiv - x - y - z + y*d1
    c = x*y - y*k0*kellyDiv - z*k0*kellyDiv

    #opt_1 = (-b + math.sqrt(b**2 - 4*a*c)) / (2*a)
    opt_2 = (-b - math.sqrt(b**2 - 4*a*c)) / (2*a)

    if (opt_2/kellyDiv + k0 > 0.04):
        return (0.04 - k0)
    return(opt_2/kellyDiv)

def single_game_prediction(league, row, teams_to_int, min_remaining, decimals = 5):
    with open("./csv_data/" + league + "/current/last_prior.pkl","rb") as inputFile:
        posteriors = pickle.load(inputFile)
    precision = f".{decimals}f"
    game_pred = {"H_proj":[],"A_proj":[],"p_home_cover":[0]}
    idₕ = teams_to_int[standardizeTeamName(row["Home"], league)]
    idₐ = teams_to_int[standardizeTeamName(row["Away"], league)]
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
    log_λₕ_μ = np.log(np.exp(i_μ + h_μ + oₕ_μ - dₐ_μ) * min_remaining / 90)
    game_pred["H_proj"].append(np.exp(log_λₕ_μ))
    #log_λₕ_σ = np.sqrt(i_σ ** 2 + h_σ ** 2 + oₕ_σ ** 2 + dₐ_σ ** 2) * min_remaining / 90
    log_λₐ_μ = np.log(np.exp(i_μ + oₐ_μ - dₕ_μ) * min_remaining / 90)
    game_pred["A_proj"].append(np.exp(log_λₐ_μ))
    #log_λₐ_σ = np.sqrt(i_σ ** 2 + oₐ_σ ** 2 + dₕ_σ ** 2) * min_remaining / 90
    #home_score_pdf = bayesian_poisson_pdf(log_λₕ_μ, log_λₕ_σ, max_y = 3)
    #away_score_pdf = bayesian_poisson_pdf(log_λₐ_μ, log_λₐ_σ, max_y = 3)
    home_score_pdf = []
    for i in range(11):
        home_score_pdf.append(np.exp(log_λₕ_μ)**i * np.exp(-np.exp(log_λₕ_μ)) / math.factorial(i))
    away_score_pdf = []
    for i in range(11):
        away_score_pdf.append(np.exp(log_λₐ_μ)**i * np.exp(-np.exp(log_λₐ_μ)) / math.factorial(i))
    p_spaces = {"cover":0}
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

    game_pred["p_home_cover"][0] = game_pred["p_home_cover"][0] / p_spaces["cover"]
    return game_pred

def predict_pinnacle_games(league, url, token):
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

    lines = api.get_best_pinnacle_lines(url, token, [convert_league(league)])

    dict = {}
    for match in lines:
        dict[lines[match]["GameId"]] = {"Date":lines[match]["Date"],"MatchId":match,"Home":standardizeTeamName(lines[match]["Home"], league),"Away":standardizeTeamName(lines[match]["Away"], league),"AH":lines[match]["AH"],"MarketTypeId":lines[match]["MarketTypeId"],"home_odds":lines[match]["home_odds"],"away_odds":lines[match]["away_odds"]}
        game_pred = single_game_prediction(league,lines[match],teams_to_int)
        for key in game_pred:
            dict[lines[match]["GameId"]][key] = game_pred[key][0]
    return (dict)

def get_placement_info(league, url, token):
    predictions = predict_pinnacle_games(league, url, token)
    for GameId in predictions:
        if (predictions[GameId]["p_home_cover"] < 0.5 and (predictions[GameId]["away_odds"] - 1) * (1 - predictions[GameId]["p_home_cover"]) - predictions[GameId]["p_home_cover"] > 0.1):
            OddsName = "AwayOdds"
        elif ((predictions[GameId]["home_odds"] - 1) * predictions[GameId]["p_home_cover"] - (1 - predictions[GameId]["p_home_cover"]) > 0.1):
            OddsName = "HomeOdds"
        else:
            continue
        predictions[GameId]["OddsName"] = OddsName
        predictions[GameId]["placement_info"] = api.get_placement_info(url, token, GameId, OddsName, predictions[GameId]["MarketTypeId"])
    print (predictions)
    return (predictions)

def bet(league, url, token):
    placement = get_placement_info(league, url, token)
    bankroll = api.get_account_balance(url, token)
    print ("Current Bankroll:", bankroll)
    bet_refs = {"Date":[],"League":[],"MatchId":[],"Home":[],"Away":[],"Ref":[],"AH":[],"Odds":[],"Stake":[],"Side":[]}
    cur_bets = api.get_current_bets(url, token)
    print (cur_bets)
    for game in placement:
        if ("placement_info" in placement[game]):
            if (len(placement[game]["placement_info"]) == 0):
                print ("Failed to retrieve placement info for " + placement[game]["Home"] + " vs. " + placement[game]["Away"])
                continue
            avg_taken_odds = 0
            total_staked = 0
            best_odds = {"Book":"PIN","max":placement[game]["placement_info"]["PIN"]["max"],"min":placement[game]["placement_info"]["PIN"]["min"],"odds":placement[game]["placement_info"]["PIN"]["odds"],"AH":placement[game]["AH"]}
            for book in placement[game]["placement_info"]:
                if (placement[game]["placement_info"][book]["odds"] > best_odds["odds"]):
                    best_odds = {"Book":book,"max":placement[game]["placement_info"][book]["max"],"min":placement[game]["placement_info"][book]["min"],"odds":placement[game]["placement_info"][book]["odds"],"AH":placement[game]["AH"]}
            #Hard code exclude brann bets
            if (placement[game]["Home"] == "Brann" or placement[game]["Away"] == "Brann"):
                continue
            if ((placement[game]["Home"], placement[game]["Away"]) in cur_bets):
                if (cur_bets[(placement[game]["Home"], placement[game]["Away"])][0]["AH"] != best_odds["AH"]):
                    print ("AH has changed for " + placement[game]["Home"] + " vs. " + placement[game]["Away"] + ": Aborting...")
                    continue
                weighted_avg_odds = 0
                for bet in cur_bets[(placement[game]["Home"], placement[game]["Away"])]:
                    weighted_avg_odds += bet["Odds"] * bet["Stake"]
                    total_staked += bet["Stake"]
                avg_taken_odds = weighted_avg_odds / total_staked
                total_staked = total_staked / bankroll
            print ("Prev bet:", avg_taken_odds, total_staked)
            if (placement[game]["OddsName"] == "HomeOdds"):
                p = placement[game]["p_home_cover"]
            elif (placement[game]["OddsName"] == "AwayOdds"):
                p = 1 - placement[game]["p_home_cover"]
            desired_bet = new_kelly(p, avg_taken_odds, best_odds["odds"], total_staked, 12)*bankroll
            if (desired_bet > best_odds["max"]):
                desired_bet = best_odds["max"]
            elif (desired_bet < best_odds["min"]):
                continue
            print ("NEW BET:", desired_bet)
            print ("BOOKIEODDS:", best_odds["Book"] + ":" + str(best_odds["odds"]))
            return_ref = api.place_bet(url, token, game, placement[game]["MarketTypeId"], placement[game]["OddsName"], desired_bet, best_odds["Book"] + ":" + str(best_odds["odds"]))
            if (return_ref != -1):
                bet_refs["Date"].append(placement[game]["Date"].split()[0])
                bet_refs["League"].append(league)
                bet_refs["MatchId"].append(placement[game]["MatchId"])
                bet_refs["Home"].append(placement[game]["Home"])
                bet_refs["Away"].append(placement[game]["Away"])
                bet_refs["Ref"].append(return_ref)
                bet_refs["AH"].append(placement[game]["AH"])
                bet_refs["Odds"].append(best_odds["odds"])
                bet_refs["Stake"].append(desired_bet)
                bet_refs["Side"].append(placement[game]["OddsName"])
            print ("Just placed bet", (placement[game]["Home"], placement[game]["Away"]))
    df = pd.DataFrame.from_dict(bet_refs)
    if (exists("./csv_data/api_bets.csv")):
        oldbets = pd.read_csv("./csv_data/api_bets.csv", encoding = "ISO-8859-1")
        oldbets = oldbets.append(df)
        oldbets.to_csv("./csv_data/api_bets.csv", index = False)
    else:
        df.to_csv("./csv_data/api_bets.csv", index = False)

def check_accepted_bets(url, token):
    api_bets = pd.read_csv("./csv_data/api_bets.csv")
    accept = []
    for index, row in api_bets.iterrows():
        if (row["Accepted"] == "T" or (api.get_bet_by_ref(url, token, row["Ref"])["Code"] == 0 and api.get_bet_by_ref(url, token, row["Ref"])["Data"][0]["Status"] == "Running")):
            accept.append("T")
        else:
            accept.append("F")
    api_bets["Accepted"] = accept
    api_bets.to_csv("./csv_data/api_bets.csv", index = False)

# url, token = api.login()
# api.get_inplay_best_pinnacle_lines(url, token)
#
#
# api.logout(url, token)

league = "Japan1"

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

row = {"Home":"Kashima Antlers", "Away":"Vissel Kobe", "AH":-0.5}

print (single_game_prediction(league, row, teams_to_int, 3))
