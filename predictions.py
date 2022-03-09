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


def fitWeibullParameters():
    train = pd.read_csv("./csv_data/England1/train.csv", encoding = "ISO-8859-1")
    train = train[train["H_proj"].notna()]
    aggLeagues = ["Algeria1","Australia1","Australia2","Brazil1","Brazil2","Czech1","Czech2","Denmark1","Denmark2","England2","England3","England4","Finland1","Finland2","France1","France2","France3","Germany1","Germany2","Germany3","Iran1","Italy1","Italy2","Japan1","Japan2","Korea1","Morocco1","Netherlands1","Netherlands2","Norway1","Norway2","Qatar1","Singapore1","SouthAfrica1","Spain1","Spain2","Sweden1","Sweden2","UAE1","USA1"]
    for l in aggLeagues:
        new = pd.read_csv("./csv_data/" + l + "/train.csv", encoding = "ISO-8859-1")
        new = new[new["H_proj"].notna()]
        train = train.append(new, ignore_index = True)
    print (train)
    print (MLE(train))

def WeibullCountDistPredictions(league):
    train = pd.read_csv("./csv_data/England1/train.csv", encoding = "ISO-8859-1")
    train = train[train["H_proj"].notna()]
    aggLeagues = ["England2","England3","England4"]
    for l in aggLeagues:
        new = pd.read_csv("./csv_data/" + l + "/train.csv", encoding = "ISO-8859-1")
        new = new[new["H_proj"].notna()]
        train = train.append(new, ignore_index = True)
    test = pd.read_csv("./csv_data/" + league + "/test.csv", encoding = "ISO-8859-1")
    test = test[test["H_proj"].notna()]
    test = test.reset_index(drop=True)
    games = len(train.index)
    dict = {}
    testCount = 0
    #[1.03212958 0.98436033 0.01603222] #OPTIMAL YESTERDAY
    #optimal = MLE(train)
    optimal = [1.0308, 0.98436033, 0.01603222]
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

    pred = {"p_1":[],"p_X":[],"p_2":[],"p_Open_home_cover":[],"p_Close_home_cover":[],"p_Open_over":[],"p_Close_over":[]}
    for key in pred:
        for i in range(len(test.index)):
            pred[key].append(0)
    for index in range(len(test.index)):
        p_spaces = {"Open_cover":0,"Close_cover":0,"Open_over":0,"Close_over":0}
        for j in range(11):
            for k in range(11):
                if (j > k):
                    pred["p_1"][index] += dict[j][k][index]
                elif (k > j):
                    pred["p_2"][index] += dict[j][k][index]
                else:
                    pred["p_X"][index] += dict[j][k][index]

                for x in ["Open","Close"]:
                    if ("0.5" in str(test.at[index, x + " AH"])):
                        p_spaces[x + "_cover"] += dict[j][k][index]
                        if (j > k + test.at[index, x + " AH"]):
                            pred["p_" + x + "_home_cover"][index] += dict[j][k][index]
                    elif ("0.75" not in str(test.at[index, x + " AH"]) and "0.25" not in str(test.at[index, x + " AH"])):
                        if (j != k + test.at[index, x + " AH"]):
                            p_spaces[x + "_cover"] += dict[j][k][index]
                        if (j > k + test.at[index, x + " AH"]):
                            pred["p_" + x + "_home_cover"][index] += dict[j][k][index]
                    else:
                        parts = [test.at[index, x + " AH"] - 0.25,test.at[index, x + " AH"] + 0.25]
                        for part in parts:
                            if ("0.5" in str(part)):
                                p_spaces[x + "_cover"] += dict[j][k][index]
                                if (j > k + part):
                                    pred["p_" + x + "_home_cover"][index] += dict[j][k][index]
                            else:
                                if (j != k + part):
                                    p_spaces[x + "_cover"] += dict[j][k][index]
                                if (j > k + part):
                                    pred["p_" + x + "_home_cover"][index] += dict[j][k][index]

                    if ("0.5" in str(test.at[index, x + " OU"])):
                        p_spaces[x + "_over"] += dict[j][k][index]
                        if (j + k > test.at[index, x + " OU"]):
                            pred["p_" + x + "_over"][index] += dict[j][k][index]
                    elif ("0.75" not in str(test.at[index, x + " OU"]) and "0.25" not in str(test.at[index, x + " OU"])):
                        if (j + k != test.at[index, x + " OU"]):
                            p_spaces[x + "_over"] += dict[j][k][index]
                        if (j + k > test.at[index, x + " OU"]):
                            pred["p_" + x + "_over"][index] += dict[j][k][index]
                    else:
                        parts = [test.at[index, x + " OU"] - 0.25,test.at[index, x + " OU"] + 0.25]
                        for part in parts:
                            if ("0.5" in str(part)):
                                p_spaces[x + "_over"] += dict[j][k][index]
                                if (j + k > part):
                                    pred["p_" + x + "_over"][index] += dict[j][k][index]
                            else:
                                if (j + k != part):
                                    p_spaces[x + "_over"] += dict[j][k][index]
                                if (j + k > part):
                                    pred["p_" + x + "_over"][index] += dict[j][k][index]

        for x in ["Open","Close"]:
            pred["p_" + x + "_home_cover"][index] = pred["p_" + x + "_home_cover"][index] / p_spaces[x + "_cover"]
            pred["p_" + x + "_over"][index] = pred["p_" + x + "_over"][index] / p_spaces[x + "_over"]


    for key in pred:
        test[key] = pred[key]
    test.to_csv("./csv_data/" + league + "/predictions.csv", index = False)

def bayesian(league):
    train = pd.read_csv("./csv_data/England1/train.csv", encoding = "ISO-8859-1")
    # train = train[train["H_proj"].notna()]
    # aggLeagues = ["England2","England3","England4"]
    # for l in aggLeagues:
    #     new = pd.read_csv("./csv_data/" + l + "/train.csv", encoding = "ISO-8859-1")
    #     new = new[new["H_proj"].notna()]
    #     train = train.append(new, ignore_index = True)
    train = train[["Home","Away","Home Score","Away Score"]]
    train = train.rename(columns={"Home Score": "home_team_reg_score"})
    train = train.rename(columns={"Away Score": "away_team_reg_score"})
    teams = train.Home.unique()
    teams = np.sort(teams)
    teams = pd.DataFrame(teams, columns=["team"])
    teams["i"] = teams.index

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

    test = train.iloc[len(train.index)-10:]
    train = train.iloc[0:len(train.index)-10]


    num_teams = len(train.i_home.drop_duplicates())
    num_team_pairs  = len(train.i_pair.drop_duplicates())

    home_team = theano.shared(train.i_home.values)
    away_team = theano.shared(train.i_away.values)
    team_pair = theano.shared(train.i_pair.values)

    observed_home_goals = train.home_team_reg_score.values
    observed_away_goals = train.away_team_reg_score.values

    with pm.Model() as model:
        # Global model parameters
        home = pm.Flat('home')
        sd_offence = pm.HalfStudentT('sd_offence', nu=3, sd=2.5)
        sd_defence = pm.HalfStudentT('sd_defence', nu=3, sd=2.5)
        intercept = pm.Flat('intercept')
    #
        # Team-specific poisson model parameters
        offence_star = pm.Normal('offence_star', mu=0, sd=sd_offence, shape=num_teams)
        defence_star = pm.Normal('defence_star', mu=0, sd=sd_defence, shape=num_teams)
        offence = pm.Deterministic('offence', offence_star - tt.mean(offence_star))
        defence = pm.Deterministic('defence', defence_star - tt.mean(defence_star))
        home_theta = tt.exp(intercept + home + offence[home_team] - defence[away_team])
        away_theta = tt.exp(intercept + offence[away_team] - defence[home_team])
    #
    #
        # Likelihood of observed data
        home_goals = pm.Poisson('home_goals', mu=home_theta, observed=observed_home_goals)
        away_goals = pm.Poisson('away_goals', mu=away_theta, observed=observed_away_goals)

    with model:
        trace = pm.sample(2000, tune=1000, cores=1)

    home_team.set_value(test.i_home.values)
    away_team.set_value(test.i_away.values)
    team_pair.set_value(test.i_pair.values)

    with model:
        post_pred = pm.sample_posterior_predictive(trace)

    preds = []
    for i in range(10):
        preds.append([])
    for x in post_pred["home_goals"]:
        for i in range(len(x)):
            preds[i].append(x[i])

    avgGoals = []
    for game in preds:
        avgGoals.append(np.average(game))
    test["H_proj"] = avgGoals

    preds = []
    for i in range(10):
        preds.append([])
    for x in post_pred["away_goals"]:
        for i in range(len(x)):
            preds[i].append(x[i])

    avgGoals = []
    for game in preds:
        avgGoals.append(np.average(game))
    test["A_proj"] = avgGoals
    test.to_csv("HMMMM.csv")

bayesian("England1")
