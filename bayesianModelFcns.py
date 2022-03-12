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
    priors['home'][1] = np.minimum(priors['home'][1] * factor, f_thresh)
    priors['intercept'][1] = np.minimum(priors['intercept'][1] * factor, f_thresh)
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
