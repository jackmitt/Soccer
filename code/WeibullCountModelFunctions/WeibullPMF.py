import pandas
import numpy
import math
from WeibullCountModelFunctions.alpha import alpha

def weibullPmf(x, l, c, alphaDict):
    if (x < 0):
        return 0
    total = 0
    j = x
    for i in range(50):
        total += (((-1)**(x+j+i)) * (l**(j+i)) * alpha(x, j + i, c, alphaDict)) / math.gamma(c*(j+i) + 1)
    return (total)
