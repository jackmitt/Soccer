import pandas as pd
import numpy as np
import math
from WeibullPMF import weibullPmf
from frankCopula import copula

#logLikelihood function for ONE game
def logLikelihood(l1, c1, l2, c2, k, y1, y2):
    return (np.log(copula(weibullPmf(y1, l1, c1), weibullPmf(y2, l2, c2), k) - copula(weibullPmf(y1 - 1, l1, c1), weibullPmf(y2, l2, c2), k) - copula(weibullPmf(y1, l1, c1), weibullPmf(y2 - 1, l2, c2), k) + copula(weibullPmf(y1 - 1, l1, c1), weibullPmf(y2 - 1, l2, c2), k)))

print (logLikelihood(1.5, 1.05, 1.1, 0.98, -.4561, 10, 7))
