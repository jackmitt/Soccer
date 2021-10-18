library(ggplot2)
library(sandwich)
library(msm)
library(glmnetUtils)
library(sigmoid)
library(My.stepwise)
library(MASS)
library(dplyr)
library(caret)

#plot1 = histogram(predictions, xlim = c(0,10), breaks = 15)


train = read.csv("C:/Users/JackMitt/Documents/EPLBettingModel/EPL_Csvs/currentModelTrain/temptrainx.csv")
test = read.csv("C:/Users/JackMitt/Documents/EPLBettingModel/EPL_Csvs/currentModelTrain/temptestx.csv")
trainNum = train[-c(1,2,3,4)]
testNum = test[-c(1,2,3,4)]
trainS = as.data.frame(scale(trainNum))
colMeans = c()
colSds = c()
for (i in colnames(trainNum)){
  colMeans = c(colMeans, mean(trainNum[[i]]))
  colSds = c(colSds, sd(trainNum[[i]]))
}
testS =as.data.frame(scale(testNum, center=colMeans, scale=colSds))
trainS["Home Field"] = train["Home.Field"]
trainS["Score"] = train["Score"]
testS["Home Field"] = test["Home.Field"]
testS["Score"] = test["Score"]

predictions = c()
model = glm(Score ~ ., family = "poisson", data = trainS)
predictions = c(predictions, predict(model, newdata = testS, type = "response"))

test["Poisson Mean Prediction"] = predictions
prob_0_goal = c()
prob_1_goal = c()
prob_2_goal = c()
prob_3_goal = c()
prob_4_goal = c()
prob_5_goal = c()
prob_6_goal = c()
prob_7_goal = c()
prob_8_goal = c()
prob_9_goal = c()
prob_10_goal = c()
for (i in predictions){
  prob_0_goal = c(prob_0_goal, dpois(0, i))
  prob_1_goal = c(prob_1_goal, dpois(1, i))
  prob_2_goal = c(prob_2_goal, dpois(2, i))
  prob_3_goal = c(prob_3_goal, dpois(3, i))
  prob_4_goal = c(prob_4_goal, dpois(4, i))
  prob_5_goal = c(prob_5_goal, dpois(5, i))
  prob_6_goal = c(prob_6_goal, dpois(6, i))
  prob_7_goal = c(prob_7_goal, dpois(7, i))
  prob_8_goal = c(prob_8_goal, dpois(8, i))
  prob_9_goal = c(prob_9_goal, dpois(9, i))
  prob_10_goal = c(prob_10_goal, dpois(10, i))
}
test["0 Goal Prob"] = prob_0_goal
test["1 Goal Prob"] = prob_1_goal
test["2 Goal Prob"] = prob_2_goal
test["3 Goal Prob"] = prob_3_goal
test["4 Goal Prob"] = prob_4_goal
test["5 Goal Prob"] = prob_5_goal
test["6 Goal Prob"] = prob_6_goal
test["7 Goal Prob"] = prob_7_goal
test["8 Goal Prob"] = prob_8_goal
test["9 Goal Prob"] = prob_9_goal
test["10 Goal Prob"] = prob_10_goal

write.csv(test, "C:/Users/JackMitt/Documents/EPLBettingModel/testPredictions.csv")

#cross validation for predictions for train data
foldBreaks = c(0, trunc(nrow(train)/5), trunc(2*nrow(train)/5), trunc(3*nrow(train)/5), trunc(4*nrow(train)/5), trunc(5*nrow(train)/5))
predictions = c()

for (i in 1:5){
  testIndex = seq(foldBreaks[i] + 1, foldBreaks[i+1])
  tempTrain = train[-testIndex, ]
  tempTest = train[testIndex, ]

  trainNum = tempTrain[-c(1,2,3,4)]
  testNum = tempTest[-c(1,2,3,4)]
  trainS = as.data.frame(scale(trainNum))
  colMeans = c()
  colSds = c()
  for (i in colnames(trainNum)){
    colMeans = c(colMeans, mean(trainNum[[i]]))
    colSds = c(colSds, sd(trainNum[[i]]))
  }
  testS =as.data.frame(scale(testNum, center=colMeans, scale=colSds))
  trainS["Home Field"] = tempTrain["Home.Field"]
  trainS["Score"] = tempTrain["Score"]
  testS["Home Field"] = tempTest["Home.Field"]
  testS["Score"] = tempTest["Score"]
  
  model = glm(Score ~ ., family = "poisson", data = trainS)
  predictions = c(predictions, predict(model, newdata = testS, type = "response"))
}
train["Poisson Mean Prediction"] = predictions
write.csv(test, "C:/Users/JackMitt/Documents/EPLBettingModel/trainPredictions.csv")