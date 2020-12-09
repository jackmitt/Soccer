library(ggplot2)
library(sandwich)
library(msm)
library(glmnetUtils)
library(sigmoid)
library(My.stepwise)
library(MASS)

train = read.csv("C:/Users/JackMitt/Documents/EPLBettingModel/EPL_Csvs/currentModelTrain/temptrainx.csv")
pred = read.csv("C:/Users/JackMitt/Documents/EPLBettingModel/EPL_Csvs/2020-21_Season/intermediate.csv")
numDataTrain = train[-c(1,2,3,4)]
trainScaled = as.data.frame(scale(numDataTrain))
trainScaled["Home Field"] = train["Home.Field"]
trainScaled["Score"] = train["Score"]
numDataPred = pred[-c(1,2)]
colMeans = c()
colSds = c()
for (i in colnames(numDataTrain)){
  colMeans = c(colMeans, mean(numDataTrain[[i]]))
  colSds = c(colSds, sd(numDataTrain[[i]]))
}
predScaled = as.data.frame(scale(numDataPred, center=colMeans, scale=colSds))
predScaled["Home Field"] = pred["Home.Field"]


model = glm(Score ~ ., family = poisson, data = trainScaled)
predictions = predict(model, newdata = predScaled, type = "response")

pred["Poisson Mean Prediction"] = predictions

write.csv(pred, "C:/Users/JackMitt/Documents/EPLBettingModel/EPL_Csvs/2020-21_Season/intermediate.csv", row.names=FALSE)