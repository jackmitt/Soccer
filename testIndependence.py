import pandas as pd
import numpy as np

data = pd.read_csv('./SerieA_Csvs/no_T_Vars/poissonPredictionMeans.csv', encoding = "ISO-8859-1")
pred = []
act = []
diff = []
for i in range(11):
    pred.append([])
    act.append([])
    diff.append([])
    for j in range(11):
        pred[i].append([])
        act[i].append([])
        diff[i].append([])

curIndex = 0
while (curIndex < len(data.index)):
    for col in data.columns:
        if ("Goal Prob" in col):
            for col2 in data.columns:
                if ("Goal Prob" in col2):
                    pred[int(col.split(" Goal Prob")[0])][int(col2.split(" Goal Prob")[0])].append(float(data.at[curIndex, col]) * float(data.at[curIndex + 1, col2]))
    for i in range(11):
        for j in range(11):
            if (int(data.at[curIndex, "Score"]) == i and int(data.at[curIndex+1, "Score"]) == j):
                act[i][j].append(1)
            else:
                act[i][j].append(0)
    curIndex += 2

for i in range(11):
    for j in range(11):
        diff[i][j].append(np.average(act[i][j]) - np.average(pred[i][j]))
for i in range(11):
    for j in range(11):
        print (i, "-", j, diff[i][j])
