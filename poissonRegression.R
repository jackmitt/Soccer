library(ggplot2)
library(sandwich)
library(msm)
library(glmnet)

data = read.csv("C:/Users/JackMitt/Documents/EPLBettingModel/poissonFormattedData.csv")
predictions = c()
for (i in 1:nrow(data)){
  print (i)
  tempTest = data[FALSE,]
  vals = c()
  for (j in c(1:98)){
    vals = c(vals, data[i, j])
  }
  tempTest[1,] = vals
  tempTrain = data[-c(i),]
  model = glm(Score ~ . - Date - Team - Score, family = poisson, data = tempTrain)
  predictions = c(predictions, predict(model, newdata = tempTest, type = "response"))
}

data["Poisson Mean Prediction"] = predictions
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
data["0 Goal Prob"] = prob_0_goal
data["1 Goal Prob"] = prob_1_goal
data["2 Goal Prob"] = prob_2_goal
data["3 Goal Prob"] = prob_3_goal
data["4 Goal Prob"] = prob_4_goal
data["5 Goal Prob"] = prob_5_goal
data["6 Goal Prob"] = prob_6_goal
data["7 Goal Prob"] = prob_7_goal
data["8 Goal Prob"] = prob_8_goal
data["9 Goal Prob"] = prob_9_goal
data["10 Goal Prob"] = prob_10_goal

write.csv(data, "C:/Users/JackMitt/Documents/EPLBettingModel/poissonPredictionMeans.csv")

