## Workflow

### Data Extraction
* The core data for modeling is goals and expected goals
* Data on betting markets is also required for backtesting

[scrapers.py](https://github.com/jackmitt/Soccer/blob/master/scrapers.py) --> contains functions for scraping data publicly available web data using Selenium + BeautifulSoup

[footy_stats_api.py](https://github.com/jackmitt/Soccer/blob/master/footy_stats_api.py) --> pulls historical data from API and saves locally

### Data Cleaning / Feature Engineering
* Pandas/numpy used throughout, although the *Database* class from [helpers.py](https://github.com/jackmitt/Soccer/blob/master/helpers.py) aims to simplify things

[data_manipulation.py](https://github.com/jackmitt/Soccer/blob/master/data_manipulation.py) --> methods for preparing the data for modeling

*For soccer, there is not much to do for this step given the limited predictive data that is publicly accessible - this step is much more involved for [intl_basketball](https://github.com/jackmitt/intl_basketball)*

### Modeling
* In addition to global intercept and homefield parameters, each team has an offensive and defensive parameter
* Goals are modeled in a similar way to a Poisson log-linear glm; i.e. log(goal_mean_a) ~ intercept + (homefield if team a is home) + offensive_a - defensive_b
* For every gameweek, priors are used for predictions, then the priors are used to calculate posteriors, then the posteriors become the priors for the next gameweek
* Calculating of posteriors relies on Markov Chain Monte Carlo methods - I used PyMC with jax sampling on a Linux system across multiple cores for necessary speed improvements
* The two predicted goal parameters are presumed independent and the joint probability distribution is calculated as such using the Poisson distribution[^1]

[bayesianModelFcns.py](https://github.com/jackmitt/Soccer/blob/master/bayesianModelFcns.py) --> houses the functions for the Bayesian hierarchical model

[predictions.py](https://github.com/jackmitt/Soccer/blob/master/predictions.py) --> bayesian() function calls on above functions to chronologically iterate through data making predictions then updating the parameters

[^1]: Many have proposed alternate methods [(Weibull Count Model, for example)](https://blogs.salford.ac.uk/business-school/wp-content/uploads/sites/7/2016/09/paper.pdf) given the shortcomings of the Poisson distribution and the clearly dependent nature of goals scored between two teams. After trying a Weibull Count distribution model with a copula [myself](https://github.com/jackmitt/Soccer/tree/master/WeibullCountModelFunctions), my results were not significantly better enough to prefer that over the simple independent Poisson model.

### Evaluation of Backtesting
* Traditional determinations of model fit are not meaningful; instead, we are concerned with the performance of our bets against the market
* There are two primary markets for each game: the Asian handicap market, which considers the difference of scores between the two teams, and the totals market, which considers the sum of scores
* For each market, an event is given (For example, A beats B by at least goal), and we can derive our probability for that event simply using our predicted joint probability distribution
* Bet sizing is chosen to be a fraction of the [Kelly Criterion](https://www.princeton.edu/~wbialek/rome/refs/kelly_56.pdf)
* An additional metric, market movement, is used for evaluation of our bet on the opening of a market under the theory that these markets are efficient

[evaluations.py](https://github.com/jackmitt/Soccer/blob/master/evaluations.py) --> all methods discussed above lie in this file

## Automated Trading
* The entire workflow needed for up-to-date modeling and predictions was automated and ran on a dedicated server (a mini computer in my closet) 

[asian_odds_api.py](https://github.com/jackmitt/Soccer/blob/master/asian_odds_api.py) --> includes all the modules defining interaction with the API for sending and recieving market data
[automatedBettingScript.py](https://github.com/jackmitt/Soccer/blob/master/automatedBettingScript.py) --> constantly checks market data, makes use of modules from every part of the workflow, and places bets when value is identified

## Scope
Though more leagues went through the workflow in consideration, the following were a part of the automated trading and of the most concern:
* English Premier League
* La Liga
* Bundesliga
* Liga Portugal
* Eliteserien
* Superliga
* Eredivisie
* Croatian Football League
* Scottish Premiership
* Brasileiro Série A
* K League 1
* J1 League
* J2 League
