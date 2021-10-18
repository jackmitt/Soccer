library(dplyr)
library(tidyr)
library(ggplot2)

data = read.csv("C:/Users/JackMitt/Documents/EPLBettingModel/tempNaiveEval.csv")

KellyDiv = 1

ml = data %>% select(ML.Result, ML.Book.Prob, ML.Edge) %>% drop_na() %>% mutate(ML.P = (ML.Edge/KellyDiv) + ML.Book.Prob) %>% arrange(ML.P)
ah = data %>% select(AH.Result, AH.Book.Prob, AH.Edge) %>% drop_na() %>% mutate(AH.P = (AH.Edge/KellyDiv) + AH.Book.Prob) %>% arrange(AH.P)
ou = data %>% select(OU.Result, OU.Book.Prob, OU.Edge) %>% drop_na() %>% mutate(OU.P = (OU.Edge/KellyDiv) + OU.Book.Prob)%>% arrange(OU.P)

index = seq(1, nrow(ml))

l = index[0+1:trunc(nrow(ml)/2)]
ll = l[0+1:trunc(length(l)/2)]
six = l[(trunc(length(l)/2)+1):trunc(length(l))]
lll = ll[0+1:trunc(length(ll)/2)]
five = ll[(trunc(length(ll)/2)+1):trunc(length(ll))]
llll = lll[0+1:trunc(length(lll)/2)]
four = lll[(trunc(length(lll)/2)+1):trunc(length(lll))]
lllll = llll[0+1:trunc(length(llll)/2)]
three = llll[(trunc(length(llll)/2)+1):trunc(length(llll))]
llllll = lllll[0+1:trunc(length(lllll)/2)]
two = lllll[(trunc(length(lllll)/2)+1):trunc(length(lllll))]
one = lllll[0+1:trunc(length(lllll)/2)]

r = index[(trunc(nrow(ml)/2)+1):nrow(ml)]
rr = r[(trunc(length(r)/2)+1):length(r)]
seven = r[0+1:trunc(length(r)/2)]
rrr = rr[(trunc(length(rr)/2)+1):length(rr)]
eight = rr[0+1:trunc(length(rr)/2)]
rrrr = rrr[(trunc(length(rrr)/2)+1):length(rrr)]
nine = rrr[0+1:trunc(length(rrr)/2)]
rrrrr = rrrr[(trunc(length(rrrr)/2)+1):length(rrrr)]
ten = rrrr[0+1:trunc(length(rrrr)/2)]
rrrrrr = rrrrr[(trunc(length(rrrrr)/2)+1):length(rrrrr)]
eleven = rrrrr[0+1:trunc(length(rrrrr)/2)]
twelve = rrrrr[(trunc(length(rrrrr)/2)+1):trunc(length(rrrrr))]

predictedRate = c(mean(ml$ML.P[one]),mean(ml$ML.P[two]),mean(ml$ML.P[three]),mean(ml$ML.P[four]),mean(ml$ML.P[five]),mean(ml$ML.P[six]),mean(ml$ML.P[seven]),mean(ml$ML.P[eight]),mean(ml$ML.P[nine]),mean(ml$ML.P[ten]),mean(ml$ML.P[eleven]),mean(ml$ML.P[twelve]))
actualRate = c(mean(ml$ML.Result[one]),mean(ml$ML.Result[two]),mean(ml$ML.Result[three]),mean(ml$ML.Result[four]),mean(ml$ML.Result[five]),mean(ml$ML.Result[six]),mean(ml$ML.Result[seven]),mean(ml$ML.Result[eight]),mean(ml$ML.Result[nine]),mean(ml$ML.Result[ten]),mean(ml$ML.Result[eleven]),mean(ml$ML.Result[twelve]))
n = c(length(ml$ML.Result[one]),length(ml$ML.Result[two]),length(ml$ML.Result[three]),length(ml$ML.Result[four]),length(ml$ML.Result[five]),length(ml$ML.Result[six]),length(ml$ML.Result[seven]),length(ml$ML.Result[eight]),length(ml$ML.Result[nine]),length(ml$ML.Result[ten]),length(ml$ML.Result[eleven]),length(ml$ML.Result[twelve]))
mldf = data.frame(predictedRate,actualRate,n)





l = index[0+1:trunc(nrow(ou)/2)]
ll = l[0+1:trunc(length(l)/2)]
six = l[(trunc(length(l)/2)+1):trunc(length(l))]
lll = ll[0+1:trunc(length(ll)/2)]
five = ll[(trunc(length(ll)/2)+1):trunc(length(ll))]
llll = lll[0+1:trunc(length(lll)/2)]
four = lll[(trunc(length(lll)/2)+1):trunc(length(lll))]
lllll = llll[0+1:trunc(length(llll)/2)]
three = llll[(trunc(length(llll)/2)+1):trunc(length(llll))]
llllll = lllll[0+1:trunc(length(lllll)/2)]
two = lllll[(trunc(length(lllll)/2)+1):trunc(length(lllll))]
one = lllll[0+1:trunc(length(lllll)/2)]

r = index[(trunc(nrow(ou)/2)+1):nrow(ou)]
rr = r[(trunc(length(r)/2)+1):length(r)]
seven = r[0+1:trunc(length(r)/2)]
rrr = rr[(trunc(length(rr)/2)+1):length(rr)]
eight = rr[0+1:trunc(length(rr)/2)]
rrrr = rrr[(trunc(length(rrr)/2)+1):length(rrr)]
nine = rrr[0+1:trunc(length(rrr)/2)]
rrrrr = rrrr[(trunc(length(rrrr)/2)+1):length(rrrr)]
ten = rrrr[0+1:trunc(length(rrrr)/2)]
rrrrrr = rrrrr[(trunc(length(rrrrr)/2)+1):length(rrrrr)]
eleven = rrrrr[0+1:trunc(length(rrrrr)/2)]
twelve = rrrrr[(trunc(length(rrrrr)/2)+1):trunc(length(rrrrr))]

predictedRate = c(mean(ou$OU.P[one]),mean(ou$OU.P[two]),mean(ou$OU.P[three]),mean(ou$OU.P[four]),mean(ou$OU.P[five]),mean(ou$OU.P[six]),mean(ou$OU.P[seven]),mean(ou$OU.P[eight]),mean(ou$OU.P[nine]),mean(ou$OU.P[ten]),mean(ou$OU.P[eleven]),mean(ou$OU.P[twelve]))
actualRate = c(mean(ou$OU.Result[one]),mean(ou$OU.Result[two]),mean(ou$OU.Result[three]),mean(ou$OU.Result[four]),mean(ou$OU.Result[five]),mean(ou$OU.Result[six]),mean(ou$OU.Result[seven]),mean(ou$OU.Result[eight]),mean(ou$OU.Result[nine]),mean(ou$OU.Result[ten]),mean(ou$OU.Result[eleven]),mean(ou$OU.Result[twelve]))
n = c(length(ou$OU.Result[one]),length(ou$OU.Result[two]),length(ou$OU.Result[three]),length(ou$OU.Result[four]),length(ou$OU.Result[five]),length(ou$OU.Result[six]),length(ou$OU.Result[seven]),length(ou$OU.Result[eight]),length(ou$OU.Result[nine]),length(ou$OU.Result[ten]),length(ou$OU.Result[eleven]),length(ou$OU.Result[twelve]))
oudf = data.frame(predictedRate,actualRate,n)




l = index[0+1:trunc(nrow(ah)/2)]
ll = l[0+1:trunc(length(l)/2)]
six = l[(trunc(length(l)/2)+1):trunc(length(l))]
lll = ll[0+1:trunc(length(ll)/2)]
five = ll[(trunc(length(ll)/2)+1):trunc(length(ll))]
llll = lll[0+1:trunc(length(lll)/2)]
four = lll[(trunc(length(lll)/2)+1):trunc(length(lll))]
lllll = llll[0+1:trunc(length(llll)/2)]
three = llll[(trunc(length(llll)/2)+1):trunc(length(llll))]
llllll = lllll[0+1:trunc(length(lllll)/2)]
two = lllll[(trunc(length(lllll)/2)+1):trunc(length(lllll))]
one = lllll[0+1:trunc(length(lllll)/2)]

r = index[(trunc(nrow(ah)/2)+1):nrow(ah)]
rr = r[(trunc(length(r)/2)+1):length(r)]
seven = r[0+1:trunc(length(r)/2)]
rrr = rr[(trunc(length(rr)/2)+1):length(rr)]
eight = rr[0+1:trunc(length(rr)/2)]
rrrr = rrr[(trunc(length(rrr)/2)+1):length(rrr)]
nine = rrr[0+1:trunc(length(rrr)/2)]
rrrrr = rrrr[(trunc(length(rrrr)/2)+1):length(rrrr)]
ten = rrrr[0+1:trunc(length(rrrr)/2)]
rrrrrr = rrrrr[(trunc(length(rrrrr)/2)+1):length(rrrrr)]
eleven = rrrrr[0+1:trunc(length(rrrrr)/2)]
twelve = rrrrr[(trunc(length(rrrrr)/2)+1):trunc(length(rrrrr))]

predictedRate = c(mean(ah$AH.P[one]),mean(ah$AH.P[two]),mean(ah$AH.P[three]),mean(ah$AH.P[four]),mean(ah$AH.P[five]),mean(ah$AH.P[six]),mean(ah$AH.P[seven]),mean(ah$AH.P[eight]),mean(ah$AH.P[nine]),mean(ah$AH.P[ten]),mean(ah$AH.P[eleven]),mean(ah$AH.P[twelve]))
actualRate = c(mean(ah$AH.Result[one]),mean(ah$AH.Result[two]),mean(ah$AH.Result[three]),mean(ah$AH.Result[four]),mean(ah$AH.Result[five]),mean(ah$AH.Result[six]),mean(ah$AH.Result[seven]),mean(ah$AH.Result[eight]),mean(ah$AH.Result[nine]),mean(ah$AH.Result[ten]),mean(ah$AH.Result[eleven]),mean(ah$AH.Result[twelve]))
n = c(length(ah$AH.Result[one]),length(ah$AH.Result[two]),length(ah$AH.Result[three]),length(ah$AH.Result[four]),length(ah$AH.Result[five]),length(ah$AH.Result[six]),length(ah$AH.Result[seven]),length(ah$AH.Result[eight]),length(ah$AH.Result[nine]),length(ah$AH.Result[ten]),length(ah$AH.Result[eleven]),length(ah$AH.Result[twelve]))
ahdf = data.frame(predictedRate,actualRate,n)







ggplot(mldf, aes(y=actualRate, x=predictedRate, color = n, size = n)) + geom_point() + geom_abline(slope=1, intercept=0) + xlim(0,1) + ylim(0,1)

ggplot(ahdf, aes(y=actualRate, x=predictedRate, color = n, size = n)) + geom_point() + geom_abline(slope=1, intercept=0) + xlim(0,1) + ylim(0,1)

ggplot(oudf, aes(y=actualRate, x=predictedRate, color = n, size = n)) + geom_point() + geom_abline(slope=1, intercept=0) + xlim(0,1) + ylim(0,1)
