import math

def alpha(x,j,c,alphaDict = {}):

    return babyAlpha(x,j,c,alphaDict)

# x is always less than j by at least one
def babyAlpha(x,j,c,alphaDict):
    # x is supercript, j is subscript
    if (x==0):
        return math.gamma(c*j+1)/math.gamma(j+1)
    elif (x in alphaDict):
        if (j in alphaDict[x]):
            return alphaDict[x][j]
        else:
            oldDict = alphaDict[x]
            oldDict[j] = alfHelp(x,j,c)
            alphaDict[x] = oldDict
            return alphaDict[x][j]
    else:
        newDict = {j:alfHelp(x,j,c)}
        alphaDict[x] = newDict

        return alphaDict[x][j]

def alfHelp(x,j,c):
    alf = 0
        # summation from x to j-1
    for m in range(x,j):
        alf += alpha(x-1,m,c)*math.gamma(c*j-c*m+1)/math.gamma(j-m+1)

    return alf

print (alpha(2,2,1))
