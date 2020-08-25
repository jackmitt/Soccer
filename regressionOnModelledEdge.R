library(ggplot2)
library(sandwich)
library(msm)
library(glmnet)

data = read.csv("C:/Users/JackMitt/Documents/EPLBettingModel/SerieA_Csvs/mlResultsByEdge.csv")
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
  model = glm(Result ~ P, family = binomial, data = tempTrain)
  predictions = c(predictions, predict(model, newdata = tempTest, type = "response"))
}

data["True Prediction"] = predictions
write.csv(data, "C:/Users/JackMitt/Documents/EPLBettingModel/SerieA_Csvs/mlTruePredictedProbabilities.csv")

data = read.csv("C:/Users/JackMitt/Documents/EPLBettingModel/SerieA_Csvs/ahResultsByEdge.csv")
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
  model = glm(Result ~ P, family = binomial, data = tempTrain)
  predictions = c(predictions, predict(model, newdata = tempTest, type = "response"))
}

data["True Prediction"] = predictions
write.csv(data, "C:/Users/JackMitt/Documents/EPLBettingModel/SerieA_Csvs/ahTruePredictedProbabilities.csv")

data = read.csv("C:/Users/JackMitt/Documents/EPLBettingModel/SerieA_Csvs/ouResultsByEdge.csv")
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
  model = glm(Result ~ P, family = binomial, data = tempTrain)
  predictions = c(predictions, predict(model, newdata = tempTest, type = "response"))
}

data["True Prediction"] = predictions
write.csv(data, "C:/Users/JackMitt/Documents/EPLBettingModel/SerieA_Csvs/ouTruePredictedProbabilities.csv")