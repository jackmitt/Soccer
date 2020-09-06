import pandas as pd
import numpy as np
import math

def copula(u, v, k):
    return ((-1/k)*np.log(1+((np.exp(-k*u) - 1) * (np.exp(-k*v) - 1) / (np.exp(-k) - 1))))
