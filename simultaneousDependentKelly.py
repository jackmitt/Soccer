import math
import time
import random
import pandas as pd
import numpy as np
import itertools
import numpy as np
import scipy.optimize
from datetime import datetime
from collections import defaultdict
from scipy.optimize import NonlinearConstraint

#calculates expected log growth rate through Monte Carlo simulation
#pass in array of calculated probabilities, array of implicit probabilities from the book, and array of wagers (in proportions of bankroll)
#if another list of wagers is passed into altWager, then the difference is returned. Else, the log growth rate for that one list is returned
def expected_log_growth(betNames, pt, pb, wager, altWager):
    payout = []
    gradients = []
    for prob in pb:
        payout.append((1/prob) - 1)
    numEvents = len(pb)
    logGrowthCalculations = []
    logGrowthCalculationsAlt = []
    numIter = 100
    for m in range(numIter):
        simLogGrowth = 0
        simLogGrowthAlt = 0
        rng = random.randint(1,100000)/100000
        totalPassed = 0
        score = []
        for i in range(len(pt)):
            for j in range(len(pt)):
                if (totalPassed + pt[i][j] > rng or (i == len(pt) - 1) and j == len(pt) - 1):
                    score.append(i)
                    score.append(j)
                    break
                totalPassed += pt[i][j]
        for i in range(len(betNames)):
            if (betNames[i] == "BRC"):
                simLogGrowth += np.log(1)
                simLogGrowthAlt += np.log(1)
            if (betNames[i] == "1"):
                if (score[0] > score[1]):
                    simLogGrowth += np.log(1 + wager[i]*payout[i])
                    simLogGrowthAlt += np.log(1 + altWager[i]*payout[i])
                else:
                    slg = min(wager[i], 0.9999999999)
                    slga = min(altWager[i], 0.9999999999)
                    simLogGrowth += np.log(1 - slg)
                    simLogGrowthAlt += np.log(1 - slga)
            elif (betNames[i] == "2"):
                if (score[1] > score[0]):
                    simLogGrowth += np.log(1 + wager[i]*payout[i])
                    simLogGrowthAlt += np.log(1 + altWager[i]*payout[i])
                else:
                    slg = min(wager[i], 0.9999999999)
                    slga = min(altWager[i], 0.9999999999)
                    simLogGrowth += np.log(1 - slg)
                    simLogGrowthAlt += np.log(1 - slga)
            elif (betNames[i] == "X"):
                if (score[1] == score[0]):
                    simLogGrowth += np.log(1 + wager[i]*payout[i])
                    simLogGrowthAlt += np.log(1 + altWager[i]*payout[i])
                else:
                    slg = min(wager[i], 0.9999999999)
                    slga = min(altWager[i], 0.9999999999)
                    simLogGrowth += np.log(1 - slg)
                    simLogGrowthAlt += np.log(1 - slga)

            if ("AH" in betNames[i]):
                if (betNames[i].split()[1].split(".")[1] != "25" and betNames[i].split()[1].split(".")[1] != "75"):
                    if ("(1)" in betNames[i]):
                        if (score[1] - score[0] < float(betNames[i].split()[1])):
                            simLogGrowth += np.log(1 + wager[i]*payout[i])
                            simLogGrowthAlt += np.log(1 + altWager[i]*payout[i])
                        elif (score[1] - score[0] > float(betNames[i].split()[1])):
                            slg = min(wager[i], 0.9999999999)
                            slga = min(altWager[i], 0.9999999999)
                            simLogGrowth += np.log(1 - slg)
                            simLogGrowthAlt += np.log(1 - slga)
                    else:
                        if (score[0] - score[1] < 0-float(betNames[i].split()[1])):
                            simLogGrowth += np.log(1 + wager[i]*payout[i])
                            simLogGrowthAlt += np.log(1 + altWager[i]*payout[i])
                        elif (score[0] - score[1] > 0-float(betNames[i].split()[1])):
                            slg = min(wager[i], 0.9999999999)
                            slga = min(altWager[i], 0.9999999999)
                            simLogGrowth += np.log(1 - slg)
                            simLogGrowthAlt += np.log(1 - slga)
                else:
                    if (betNames[i].split()[1][0] == "-" and betNames[i].split()[1].split(".")[1] == "75"):
                        toAdd = -0.25
                    elif (betNames[i].split()[1][0] != "-" and betNames[i].split()[1].split(".")[1] == "25"):
                        toAdd = -0.25
                    else:
                        toAdd = 0.25
                    if ("(1)" in betNames[i]):
                        if (score[1] - score[0] < float(betNames[i].split()[1]) + toAdd):
                            simLogGrowth += np.log(1 + wager[i]*payout[i])
                            simLogGrowthAlt += np.log(1 + altWager[i]*payout[i])
                        elif (score[1] - score[0] > float(betNames[i].split()[1]) + toAdd):
                            slg = min(wager[i], 0.9999999999)
                            slga = min(altWager[i], 0.9999999999)
                            simLogGrowth += np.log(1 - slg)
                            simLogGrowthAlt += np.log(1 - slga)
                        else:
                            if ((betNames[i].split()[1][0] == "-" and betNames[i].split()[1].split(".")[1] == "75") or (betNames[i].split()[1][0] != "-" and betNames[i].split()[1].split(".")[1] == "25")):
                                simLogGrowth += np.log(1 + wager[i]*payout[i]/2)
                                simLogGrowthAlt += np.log(1 + altWager[i]*payout[i]/2)
                            else:
                                simLogGrowth += np.log(1 - wager[i]/2)
                                simLogGrowthAlt += np.log(1 - altWager[i]/2)
                    else:
                        if (score[0] - score[1] < 0-float(betNames[i].split()[1]) - toAdd):
                            simLogGrowth += np.log(1 + wager[i]*payout[i])
                            simLogGrowthAlt += np.log(1 + altWager[i]*payout[i])
                        elif (score[0] - score[1] > 0-float(betNames[i].split()[1]) - toAdd):
                            slg = min(wager[i], 0.9999999999)
                            slga = min(altWager[i], 0.9999999999)
                            simLogGrowth += np.log(1 - slg)
                            simLogGrowthAlt += np.log(1 - slga)
                        else:
                            if ((betNames[i].split()[1][0] == "-" and betNames[i].split()[1].split(".")[1] == "25") or (betNames[i].split()[1][0] != "-" and betNames[i].split()[1].split(".")[1] == "75")):
                                simLogGrowth += np.log(1 + wager[i]*payout[i]/2)
                                simLogGrowthAlt += np.log(1 + altWager[i]*payout[i]/2)
                            else:
                                simLogGrowth += np.log(1 - wager[i]/2)
                                simLogGrowthAlt += np.log(1 - altWager[i]/2)

            if ("Over" in betNames[i] or "Under" in betNames[i]):
                if (betNames[i].split()[1].split(".")[1] != "25" and betNames[i].split()[1].split(".")[1] != "75"):
                    if ("Over" in betNames[i]):
                        if (score[0] + score[1] > float(betNames[i].split()[1])):
                            simLogGrowth += np.log(1 + wager[i]*payout[i])
                            simLogGrowthAlt += np.log(1 + altWager[i]*payout[i])
                        elif (score[0] + score[1] < float(betNames[i].split()[1])):
                            slg = min(wager[i], 0.9999999999)
                            slga = min(altWager[i], 0.9999999999)
                            simLogGrowth += np.log(1 - slg)
                            simLogGrowthAlt += np.log(1 - slga)
                    else:
                        if (score[0] + score[1] < float(betNames[i].split()[1])):
                            simLogGrowth += np.log(1 + wager[i]*payout[i])
                            simLogGrowthAlt += np.log(1 + altWager[i]*payout[i])
                        elif (score[0] + score[1] > float(betNames[i].split()[1])):
                            slg = min(wager[i], 0.9999999999)
                            slga = min(altWager[i], 0.9999999999)
                            simLogGrowth += np.log(1 - slg)
                            simLogGrowthAlt += np.log(1 - slga)
                elif (betNames[i].split()[1].split(".")[1] == "25"):
                    if ("Over" in betNames[i]):
                        if (score[0] + score[1] == float(betNames[i].split()[1]) - 0.25):
                            simLogGrowth += np.log(1 - wager[i]/2)
                            simLogGrowthAlt += np.log(1 - altWager[i]/2)
                        elif (score[0] + score[1] > float(betNames[i].split()[1])):
                            simLogGrowth += np.log(1 + wager[i]*payout[i])
                            simLogGrowthAlt += np.log(1 + altWager[i]*payout[i])
                        else:
                            slg = min(wager[i], 0.9999999999)
                            slga = min(altWager[i], 0.9999999999)
                            simLogGrowth += np.log(1 - slg)
                            simLogGrowthAlt += np.log(1 - slga)
                    else:
                        if (score[0] + score[1] == float(betNames[i].split()[1]) - 0.25):
                            simLogGrowth += np.log(1 + wager[i]*payout[i]/2)
                            simLogGrowthAlt += np.log(1 + altWager[i]*payout[i]/2)
                        elif (score[0] + score[1] < float(betNames[i].split()[1])):
                            simLogGrowth += np.log(1 + wager[i]*payout[i])
                            simLogGrowthAlt += np.log(1 + altWager[i]*payout[i])
                        else:
                            slg = min(wager[i], 0.9999999999)
                            slga = min(altWager[i], 0.9999999999)
                            simLogGrowth += np.log(1 - slg)
                            simLogGrowthAlt += np.log(1 - slga)
                else:
                    if ("Over" in betNames[i]):
                        if (score[0] + score[1] == float(betNames[i].split()[1]) + 0.25):
                            simLogGrowth += np.log(1 + wager[i]*payout[i]/2)
                            simLogGrowthAlt += np.log(1 + altWager[i]*payout[i]/2)
                        elif (score[0] + score[1] > float(betNames[i].split()[1])):
                            simLogGrowth += np.log(1 + wager[i]*payout[i])
                            simLogGrowthAlt += np.log(1 + altWager[i]*payout[i])
                        else:
                            slg = min(wager[i], 0.9999999999)
                            slga = min(altWager[i], 0.9999999999)
                            simLogGrowth += np.log(1 - slg)
                            simLogGrowthAlt += np.log(1 - slga)
                    else:
                        if (score[0] + score[1] == float(betNames[i].split()[1]) + 0.25):
                            simLogGrowth += np.log(1 - wager[i]/2)
                            simLogGrowthAlt += np.log(1 - altWager[i]/2)
                        elif (score[0] + score[1] < float(betNames[i].split()[1])):
                            simLogGrowth += np.log(1 + wager[i]*payout[i])
                            simLogGrowthAlt += np.log(1 + altWager[i]*payout[i])
                        else:
                            slg = min(wager[i], 0.9999999999)
                            slga = min(altWager[i], 0.9999999999)
                            simLogGrowth += np.log(1 - slg)
                            simLogGrowthAlt += np.log(1 - slga)
        logGrowthCalculations.append(simLogGrowth)
        logGrowthCalculationsAlt.append(simLogGrowthAlt)
    return (np.average(logGrowthCalculationsAlt) - np.average(logGrowthCalculations), np.average(logGrowthCalculations))

#returns a list of the gradients for x given the actual probabilities, book probabilities, old wager list
def log_growth_gradients(betNames, pt, pb, wager):
    gradients = []
    growthRates = []
    for i in range(len(wager) - 1):
        toAvg = []
        toAvg2 = []
        for j in range(1):
            #epsilon = random.gauss(0, wager[i])
            epsilon = 0.0000000000001
            xNew = wager[i] + epsilon
            newWager = wager.copy()
            newWager[i] = xNew
            diff, calc = expected_log_growth(betNames, pt, pb, wager, newWager)
            toAvg.append(diff/epsilon)
            toAvg2.append(calc)
        gradients.append(np.average(toAvg))
        growthRates.append(np.average(toAvg2))
    return (gradients, growthRates)

def adjusted_constrain(betNames, pt):
    pass

def gradient_ascent(betNames, pt, pb, kellyWagers):
    bankrollConstraint = 0.1
    wager = kellyWagers.copy()
    wager.append(1 - bankrollConstraint)
    learningRates = []
    for i in range(len(pb)):
        learningRates.append([1, True])
    cReq = 0.005
    iterCount = 1
    diffAmounts = []
    while(iterCount < 5000):
        print ("Iteration: " + str(iterCount))
        iterCount += 1
        #rngIndex = random.randint(0, len(wager)-1)
        #eq 18
        t = np.log(wager)
        gradients, logGrowths = log_growth_gradients(betNames, pt, pb, wager)
        print ("Average learning rate:", np.average(learningRates)*2)
        weightedSumGradients = 0
        for i in range(len(gradients)):
            if (gradients[i] < 0):
                if (not learningRates[i][1]):
                    learningRates[i][0] = learningRates[i][0]*1.05
                else:
                    learningRates[i][0] = learningRates[i][0]*0.95
            else:
                if (learningRates[i][1]):
                    learningRates[i][0] = learningRates[i][0]*1.05
                else:
                    learningRates[i][0] = learningRates[i][0]*0.95
            weightedSumGradients += gradients[i]*wager[i]
        #eq 19
        dt = []
        for i in range(len(gradients)):
            dt.append(wager[i]*(gradients[i] - weightedSumGradients))
        #print (t)
        #print (dt)
        #print(learningRates)
        #adjustment to x
        for i in range(len(gradients)):
            t[i] = t[i] + dt[i]*learningRates[i][0]
        #eq 15
        diffAmount = 0
        print ("TTTTTTTTTTTTTTTTTTTTTTTTTTTT", t)
        print ("BRCCCCCCCCCCCCCCCCCCCCCCCCC", np.sum(np.exp(t)))
        for i in range(len(wager)):
            diffAmount += abs(wager[i] - (np.exp(t[i])/(np.sum(np.exp(t)))))
            wager[i] = np.exp(t[i])/(np.sum(np.exp(t)))

        print (wager)
        print ("TOTAL BANKROLL BET: " + str(np.sum(wager)))
        if (len(diffAmounts) == 10):
            diffAmounts.pop(0)
        diffAmounts.append(diffAmount)
        if (len(diffAmounts) == 30 and np.average(diffAmounts) < cReq):
            break
    return (wager)
