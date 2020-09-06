library(ggplot2)
library(sandwich)
library(msm)
library(glmnet)

data = read.csv("C:/Users/JackMitt/Documents/EPLBettingModel/EPL_Csvs/only_T_E_Vars/mlResultsByEdge.csv")
predictions = c()
for (i in 1:nrow(data)){
  print (i)
  tempTest = data[FALSE,]
  vals = c()
  for (j in c(1:5)){
    vals = c(vals, data[i, j])
  }
  tempTest[1,] = vals
  tempTrain = data[-c(i),]
  model1 = glm(Result ~ P, family = binomial, data = tempTrain)
  predictions = c(predictions, predict(model1, newdata = tempTest, type = "response"))
}

data["True Prediction"] = predictions
#write.csv(data, "C:/Users/JackMitt/Documents/EPLBettingModel/EPL_Csvs/only_T_E_Vars/mlTruePredictedProbabilities.csv")

data = read.csv("C:/Users/JackMitt/Documents/EPLBettingModel/EPL_Csvs/only_T_E_Vars/ahResultsByEdge.csv")
predictions = c()
for (i in 1:nrow(data)){
  print (i)
  tempTest = data[FALSE,]
  vals = c()
  for (j in c(1:5)){
    vals = c(vals, data[i, j])
  }
  tempTest[1,] = vals
  tempTrain = data[-c(i),]
  model2 = glm(Result ~ P, family = binomial, data = tempTrain)
  predictions = c(predictions, predict(model2, newdata = tempTest, type = "response"))
}

data["True Prediction"] = predictions
#write.csv(data, "C:/Users/JackMitt/Documents/EPLBettingModel/EPL_Csvs/only_T_E_Vars/ahTruePredictedProbabilities.csv")

data = read.csv("C:/Users/JackMitt/Documents/EPLBettingModel/EPL_Csvs/only_T_E_Vars/ouResultsByEdge.csv")
predictions = c()
for (i in 1:nrow(data)){
  print (i)
  tempTest = data[FALSE,]
  vals = c()
  for (j in c(1:5)){
    vals = c(vals, data[i, j])
  }
  tempTest[1,] = vals
  tempTrain = data[-c(i),]
  model3 = glm(Result ~ P, family = binomial, data = tempTrain)
  predictions = c(predictions, predict(model3, newdata = tempTest, type = "response"))
}

data["True Prediction"] = predictions
#write.csv(data, "C:/Users/JackMitt/Documents/EPLBettingModel/EPL_Csvs/only_T_E_Vars/ouTruePredictedProbabilities.csv")