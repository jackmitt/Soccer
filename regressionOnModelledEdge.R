library(ggplot2)
library(sandwich)
library(msm)
library(glmnet)

data = read.csv("C:/Users/JackMitt/Documents/EPLBettingModel/EPL_Csvs/newvars_no_T/weibull_copula/mlResultsByEdge.csv")
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
write.csv(data, "C:/Users/JackMitt/Documents/EPLBettingModel/EPL_Csvs/newvars_no_T/weibull_copula/mlTruePredictedProbabilities.csv")

data = read.csv("C:/Users/JackMitt/Documents/EPLBettingModel/EPL_Csvs/newvars_no_T/weibull_copula/ahResultsByEdge.csv")
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
write.csv(data, "C:/Users/JackMitt/Documents/EPLBettingModel/EPL_Csvs/newvars_no_T/weibull_copula/ahTruePredictedProbabilities.csv")

data = read.csv("C:/Users/JackMitt/Documents/EPLBettingModel/EPL_Csvs/newvars_no_T/weibull_copula/ouResultsByEdge.csv")
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
write.csv(data, "C:/Users/JackMitt/Documents/EPLBettingModel/EPL_Csvs/newvars_no_T/weibull_copula/ouTruePredictedProbabilities.csv")