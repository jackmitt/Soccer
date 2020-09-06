import pandas
import numpy
import math
from alpha import alpha

def weibullPmf(x, l, c):
    total = 0
    j = x
    for i in range(50):
        total += ((-1**(x+j+i)) * (l**(j+i)) * alpha(x, j + i, c)) / math.gamma(c*(j+i) + 1)
    return (total)
