import functionization as fn
import pandas as pd

data = pd.read_csv('./EPL_Csvs/allRawData.csv', encoding = "ISO-8859-1")
temp = fn.preMatchAverages(data, 5)
temp = fn.poissonFormat(temp, dropT = False, dropE = False)
train, test = fn.trainTestSplit(temp, 2017)
train, test = fn.poissonRegression(train, test)
train, test = fn.PoissonMeansForWeibull(train, test)
test = fn.WeibullCountDist(train, test)
pred = fn.weibullBettingProbabilities(test)
pred = fn.cleanOdds(pred)
pred = fn.naiveEvaluation(pred, unique=False)
fn.seasonSim(pred, 10, 15, 2, noML = True)
