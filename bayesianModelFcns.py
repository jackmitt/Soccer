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
from scipy.integrate import quad, dblquad
from math import factorial, exp, sqrt, pi

def get_model_posteriors(trace, n_teams):
    posteriors = {}
    h_μ, h_σ = norm.fit(trace['home'])
    posteriors['home'] = [h_μ, h_σ]
    i_μ, i_σ = norm.fit(trace['intercept'])
    posteriors['intercept'] = [i_μ, i_σ]
    o_μ = []
    o_σ = []
    d_μ = []
    d_σ = []
    for i in range(n_teams):
        oᵢ_μ, oᵢ_σ = norm.fit(trace['offense'][:,i])
        o_μ.append(oᵢ_μ)
        o_σ.append(oᵢ_σ)
        dᵢ_μ, dᵢ_σ = norm.fit(trace['defense'][:,i])
        d_μ.append(dᵢ_μ)
        d_σ.append(dᵢ_σ)
    posteriors['offense'] = [o_μ, o_σ]
    posteriors['defense'] = [d_μ, d_σ]

    return posteriors

def fatten_priors(prev_posteriors, factor, f_thresh):
    priors = prev_posteriors.copy()
    #priors['home'][1] = np.minimum(priors['home'][1] * factor, f_thresh)
    #priors['intercept'][1] = np.minimum(priors['intercept'][1] * factor, f_thresh)
    priors['offense'][1] = np.minimum(np.array(priors['offense'][1]) * factor, f_thresh)
    priors['defense'][1] = np.minimum(np.array(priors['defense'][1]) * factor, f_thresh)

    return priors

def model_iteration(idₕ, sₕ_obs, idₐ, sₐ_obs, priors, n_teams, Δσ, samples=2000, tune=1000, cores=1):

    with pm.Model():
        if (len(priors) == 0):
            h = pm.Flat('home')
            i = pm.Flat('intercept')
            sd_offense = pm.HalfStudentT('sd_offense', nu=3, sd=2.5)
            sd_defense = pm.HalfStudentT('sd_defense', nu=3, sd=2.5)

            o_star_init = pm.Normal('offense_star', mu=0, sd=sd_offense, shape=n_teams)
            Δ_o = pm.Normal('Δ_o', mu=0.0, sigma=Δσ, shape=n_teams)
            o_star = pm.Deterministic('o_star', o_star_init + Δ_o)
            o = pm.Deterministic('offense', o_star - tt.mean(o_star))

            d_star_init = pm.Normal('defense_star', mu=0, sd=sd_defense, shape=n_teams)
            Δ_d = pm.Normal('Δ_d', mu=0.0, sigma=Δσ, shape=n_teams)
            d_star = pm.Deterministic('d_star', d_star_init + Δ_d)
            d = pm.Deterministic('defense', d_star - tt.mean(d_star))
        else:
            # Global model parameters
            h = pm.Normal('home', mu=priors['home'][0], sigma=priors['home'][1])
            i = pm.Normal('intercept', mu=priors['intercept'][0], sigma=priors['intercept'][1])

            # Team-specific poisson model parameters
            o_star_init = pm.Normal('o_star_init', mu=priors['offense'][0], sigma=priors['offense'][1], shape=n_teams)
            Δ_o = pm.Normal('Δ_o', mu=0.0, sigma=Δσ, shape=n_teams)
            o_star = pm.Deterministic('o_star', o_star_init + Δ_o)
            o = pm.Deterministic('offense', o_star - tt.mean(o_star))

            d_star_init = pm.Normal('d_star_init', mu=priors['defense'][0], sigma=priors['defense'][1], shape=n_teams)
            Δ_d = pm.Normal('Δ_d', mu=0.0, sigma=Δσ, shape=n_teams)
            d_star = pm.Deterministic('d_star', d_star_init + Δ_d)
            d = pm.Deterministic('defense', d_star - tt.mean(d_star))

        λₕ = tt.exp(i + h + o[idₕ] - d[idₐ])
        λₐ = tt.exp(i + o[idₐ] - d[idₕ])

        # Likelihood of observed data
        sₕ = pm.Poisson('sₕ', mu=λₕ, observed=sₕ_obs)
        sₐ = pm.Poisson('sₐ', mu=λₐ, observed=sₐ_obs)

        trace = pm.sample(
            samples,
            tune=tune,
            chains=3,
            cores=cores,
            progressbar=True,
            return_inferencedata=False
        )

        posteriors = get_model_posteriors(trace, n_teams)

        return posteriors

def model_update(idₕ, sₕ_obs, idₐ, sₐ_obs, priors, n_teams, f, f_thresh, Δσ):
    if (len(priors) != 0):
        priors = fatten_priors(priors, f, f_thresh)
    posteriors = model_iteration(idₕ, sₕ_obs, idₐ, sₐ_obs, priors, n_teams, Δσ)

    return posteriors

def bayesian_poisson_pdf(μ, σ, max_y=10):
    def integrand(x, y, σ, μ):
        pois = (np.exp(x)**y)*np.exp(-np.exp(x))/factorial(y)
        norm = np.exp(-0.5*((x-μ)/σ)**2.0)/(σ * sqrt(2.0*pi))
        return  pois * norm

    lwr = -3.0
    upr = 5.0

    y = np.arange(0,max_y)
    p = []
    for yi in y:
        I = quad(integrand, lwr, upr, args=(yi,σ,μ))
        p.append(I[0])
    p.append(1.0 - sum(p))

    return p

def single_game_prediction(row, posteriors, teams_to_int, decimals = 5):
    precision = f".{decimals}f"
    game_pred = {"H_proj":[],"A_proj":[],"p_1":[0],"p_X":[0],"p_2":[0],"p_Open_home_cover":[0],"p_Close_home_cover":[0],"p_Open_over":[0],"p_Close_over":[0]}
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
    p_spaces = {"Open_cover":0,"Close_cover":0,"Open_over":0,"Close_over":0}
    for sₕ, pₕ in enumerate(home_score_pdf):
        for sₐ, pₐ in enumerate(away_score_pdf):
            p = pₕ * pₐ
            if sₕ > sₐ:
                game_pred["p_1"][0] += p
            elif sₐ > sₕ:
                game_pred["p_2"][0] += p
            else:
                game_pred["p_X"][0] += p

            for x in ["Open","Close"]:
                if (".5" in str(row[x + " AH"])):
                    p_spaces[x + "_cover"] += p
                    if (sₕ > sₐ + row[x + " AH"]):
                        game_pred["p_" + x + "_home_cover"][0] += p
                elif (".75" not in str(row[x + " AH"]) and ".25" not in str(row[x + " AH"])):
                    if (sₕ != sₐ + row[x + " AH"]):
                        p_spaces[x + "_cover"] += p
                    if (sₕ > sₐ + row[x + " AH"]):
                        game_pred["p_" + x + "_home_cover"][0] += p
                else:
                    parts = [row[x + " AH"] - 0.25,row[x + " AH"] + 0.25]
                    for part in parts:
                        if (".5" in str(part)):
                            p_spaces[x + "_cover"] += p
                            if (sₕ > sₐ + part):
                                game_pred["p_" + x + "_home_cover"][0] += p
                        else:
                            if (sₕ != sₐ + part):
                                p_spaces[x + "_cover"] += p
                            if (sₕ > sₐ + part):
                                game_pred["p_" + x + "_home_cover"][0] += p

                if (".5" in str(row[x + " OU"])):
                    p_spaces[x + "_over"] += p
                    if (sₕ + sₐ > row[x + " OU"]):
                        game_pred["p_" + x + "_over"][0] += p
                elif (".75" not in str(row[x + " OU"]) and ".25" not in str(row[x + " OU"])):
                    if (sₕ + sₐ != row[x + " OU"]):
                        p_spaces[x + "_over"] += p
                    if (sₕ + sₐ > row[x + " OU"]):
                        game_pred["p_" + x + "_over"][0] += p
                else:
                    parts = [row[x + " OU"] - 0.25,row[x + " OU"] + 0.25]
                    for part in parts:
                        if (".5" in str(part)):
                            p_spaces[x + "_over"] += p
                            if (sₕ + sₐ > part):
                                game_pred["p_" + x + "_over"][0] += p
                        else:
                            if (sₕ + sₐ != part):
                                p_spaces[x + "_over"] += p
                            if (sₕ + sₐ > part):
                                game_pred["p_" + x + "_over"][0] += p
    for x in ["Open","Close"]:
        game_pred["p_" + x + "_home_cover"][0] = game_pred["p_" + x + "_home_cover"][0] / p_spaces[x + "_cover"]
        game_pred["p_" + x + "_over"][0] = game_pred["p_" + x + "_over"][0] / p_spaces[x + "_over"]
    return game_pred
