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



def fitWeibullParameters():
    train = pd.read_csv("./csv_data/England1/bayes_predictions.csv", encoding = "ISO-8859-1")
    train = train.iloc[380:2270]
    # aggLeagues = ["Algeria1","Australia1","Australia2","Brazil1","Brazil2","Czech1","Czech2","Denmark1","Denmark2","England2","England3","England4","Finland1","Finland2","France1","France2","France3","Germany1","Germany2","Germany3","Iran1","Italy1","Italy2","Japan1","Japan2","Korea1","Morocco1","Netherlands1","Netherlands2","Norway1","Norway2","Qatar1","Singapore1","SouthAfrica1","Spain1","Spain2","Sweden1","Sweden2","UAE1","USA1"]
    # for l in aggLeagues:
    #     new = pd.read_csv("./csv_data/" + l + "/train.csv", encoding = "ISO-8859-1")
    #     new = new[new["H_proj"].notna()]
    #     train = train.append(new, ignore_index = True)
    print (train)
    print (MLE(train))

def WeibullCountDistPredictions(league):
    # train = pd.read_csv("./csv_data/England1/train.csv", encoding = "ISO-8859-1")
    # train = train[train["H_proj"].notna()]
    # aggLeagues = ["England2","England3","England4"]
    # for l in aggLeagues:
    #     new = pd.read_csv("./csv_data/" + l + "/train.csv", encoding = "ISO-8859-1")
    #     new = new[new["H_proj"].notna()]
    #     train = train.append(new, ignore_index = True)
    test = pd.read_csv("./csv_data/" + league + "/bayes_predictions.csv", encoding = "ISO-8859-1")
    test = test[test["H_proj"].notna()]
    test = test.reset_index(drop=True)
    #games = len(train.index)
    dict = {}
    testCount = 0
    #[1.03212958 0.98436033 0.01603222] #OPTIMAL YESTERDAY
    #optimal = MLE(train)
    optimal = [1.0000, 1.0000, 0.25]
    alphaDictH = {}
    alphaDictA = {}
    cur = 0
    while (cur < len(test.index)):
        hCdf = []
        aCdf = []
        for j in range(11):
            if (j == 0):
                hCdf.append(weibullPmf(j, test.at[cur, "H_proj"], optimal[0], alphaDictH))
                aCdf.append(weibullPmf(j, test.at[cur, "A_proj"], optimal[1], alphaDictA))
            else:
                hCdf.append(weibullPmf(j, test.at[cur, "H_proj"], optimal[0], alphaDictH) + hCdf[j-1])
                aCdf.append(weibullPmf(j, test.at[cur, "A_proj"], optimal[1], alphaDictA) + aCdf[j-1])
        #Converts the distribution from joint CDF to joint PMF
        for j in range(11):
            if (j not in dict):
                dict[j] = {}
            for k in range(11):
                if (k not in dict[j]):
                    dict[j][k] = []
                if (j == 0 and k == 0):
                    dict[j][k].append(copula(hCdf[j], aCdf[k], optimal[2]))
                else:
                    tempProb = copula(hCdf[j], aCdf[k], optimal[2])
                    for p in range(j+1):
                        for q in range(k+1):
                            if (p == j and q == k):
                                break
                            tempProb -= dict[p][q][testCount]
                    dict[j][k].append(tempProb)
        cur += 1
        testCount += 1

    pred = {"w_p_1":[],"w_p_X":[],"w_p_2":[],"w_p_Open_home_cover":[],"w_p_Close_home_cover":[],"w_p_Open_over":[],"w_p_Close_over":[]}
    for key in pred:
        for i in range(len(test.index)):
            pred[key].append(0)
    for index in range(len(test.index)):
        p_spaces = {"Open_cover":0,"Close_cover":0,"Open_over":0,"Close_over":0}
        for j in range(11):
            for k in range(11):
                if (j > k):
                    pred["w_p_1"][index] += dict[j][k][index]
                elif (k > j):
                    pred["w_p_2"][index] += dict[j][k][index]
                else:
                    pred["w_p_X"][index] += dict[j][k][index]

                for x in ["Open","Close"]:
                    if (".5" in str(test.at[index, x + " AH"])):
                        p_spaces[x + "_cover"] += dict[j][k][index]
                        if (j > k + test.at[index, x + " AH"]):
                            pred["w_p_" + x + "_home_cover"][index] += dict[j][k][index]
                    elif (".75" not in str(test.at[index, x + " AH"]) and ".25" not in str(test.at[index, x + " AH"])):
                        if (j != k + test.at[index, x + " AH"]):
                            p_spaces[x + "_cover"] += dict[j][k][index]
                        if (j > k + test.at[index, x + " AH"]):
                            pred["w_p_" + x + "_home_cover"][index] += dict[j][k][index]
                    else:
                        parts = [test.at[index, x + " AH"] - 0.25,test.at[index, x + " AH"] + 0.25]
                        for part in parts:
                            if (".5" in str(part)):
                                p_spaces[x + "_cover"] += dict[j][k][index]
                                if (j > k + part):
                                    pred["w_p_" + x + "_home_cover"][index] += dict[j][k][index]
                            else:
                                if (j != k + part):
                                    p_spaces[x + "_cover"] += dict[j][k][index]
                                if (j > k + part):
                                    pred["w_p_" + x + "_home_cover"][index] += dict[j][k][index]

                    if (".5" in str(test.at[index, x + " OU"])):
                        p_spaces[x + "_over"] += dict[j][k][index]
                        if (j + k > test.at[index, x + " OU"]):
                            pred["w_p_" + x + "_over"][index] += dict[j][k][index]
                    elif (".75" not in str(test.at[index, x + " OU"]) and ".25" not in str(test.at[index, x + " OU"])):
                        if (j + k != test.at[index, x + " OU"]):
                            p_spaces[x + "_over"] += dict[j][k][index]
                        if (j + k > test.at[index, x + " OU"]):
                            pred["w_p_" + x + "_over"][index] += dict[j][k][index]
                    else:
                        parts = [test.at[index, x + " OU"] - 0.25,test.at[index, x + " OU"] + 0.25]
                        for part in parts:
                            if (".5" in str(part)):
                                p_spaces[x + "_over"] += dict[j][k][index]
                                if (j + k > part):
                                    pred["w_p_" + x + "_over"][index] += dict[j][k][index]
                            else:
                                if (j + k != part):
                                    p_spaces[x + "_over"] += dict[j][k][index]
                                if (j + k > part):
                                    pred["w_p_" + x + "_over"][index] += dict[j][k][index]

        for x in ["Open","Close"]:
            pred["w_p_" + x + "_home_cover"][index] = pred["w_p_" + x + "_home_cover"][index] / p_spaces[x + "_cover"]
            pred["w_p_" + x + "_over"][index] = pred["w_p_" + x + "_over"][index] / p_spaces[x + "_over"]


    for key in pred:
        test[key] = pred[key]
    test.to_csv("./csv_data/" + league + "/predictions.csv", index = False)

def bayesian(league):
    factor = 1.05                 # Expand the posteriors by this amount before using as priors -- old: 1.05
    f_thresh = 0.075         # A cap on team variable standard deviation to prevent blowup -- old: 0.075
    Δσ = 0.001               # The standard deviaton of the random walk variables -- old: 0.001

    # with open("./csv_data/" + league + "/last_prior.pkl","rb") as inputFile:
    #     priors = pickle.load(inputFile)
    train = pd.read_csv("./csv_data/" + league + "/betting.csv", encoding = "ISO-8859-1")
    for i in range(len(train.index)):
        train.at[i, "Date"] = datetime.date(int(train.at[i, "Date"].split("-")[0]), int(train.at[i, "Date"].split("-")[1]), int(train.at[i, "Date"].split("-")[2]))
    train = train.sort_values(by=["Date"], ignore_index = True)
    finalDict = {}
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
    num_team_pairs  = len(train.i_pair.drop_duplicates())

    warmUp = train.iloc[:splitIndex]
    train = train.iloc[splitIndex:]

    home_team = theano.shared(warmUp.i_home.values)
    away_team = theano.shared(warmUp.i_away.values)
    team_pair = theano.shared(warmUp.i_pair.values)

    observed_home_goals = warmUp.home_team_reg_score.values
    observed_away_goals = warmUp.away_team_reg_score.values

    with pm.Model() as model:
        home = pm.Flat('home')
        sd_offense = pm.HalfStudentT('sd_offense', nu=3, sd=2.5)
        sd_defense = pm.HalfStudentT('sd_defense', nu=3, sd=2.5)
        intercept = pm.Flat('intercept')

        offense_star = pm.Normal('offense_star', mu=0, sd=sd_offense, shape=num_teams)
        defense_star = pm.Normal('defense_star', mu=0, sd=sd_defense, shape=num_teams)
        offense = pm.Deterministic('offense', offense_star - tt.mean(offense_star))
        defense = pm.Deterministic('defense', defense_star - tt.mean(defense_star))
        home_theta = tt.exp(intercept + home + offense[home_team] - defense[away_team])
        away_theta = tt.exp(intercept + offense[away_team] - defense[home_team])


        home_goals = pm.Poisson('home_goals', mu=home_theta, observed=observed_home_goals)
        away_goals = pm.Poisson('away_goals', mu=away_theta, observed=observed_away_goals)

    with model:
        trace = pm.sample(5000, tune=2000, cores=1)
        priors = bmf.get_model_posteriors(trace, num_teams)

    oneIterComplete = False
    startIndex = 0
    for index, row in train.iterrows():
        for col in train.columns:
            finalDict[col].append(row[col])
        if (index != splitIndex and abs(row["Date"] - train.at[index-1,"Date"]).days > 30):
            bmf.fatten_priors(priors, 1.33, f_thresh)
        if (index != splitIndex and row["gw"] - train.at[index-1,"gw"] == 1):
            new_obs = train.iloc[startIndex:index]

            home_team = theano.shared(new_obs.i_home.values)
            away_team = theano.shared(new_obs.i_away.values)
            team_pair = theano.shared(new_obs.i_pair.values)

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
        tempDF = pd.DataFrame.from_dict(finalDict)
        tempDF.to_csv("./csv_data/" + league + "/bayes_predictions.csv", index = False)
        with open("./csv_data/" + league + "/last_prior.pkl", "wb") as f:
            pickle.dump(priors, f)
