#Setting up workspace
setwd("C:/Users/User/OneDrive/Desktop/Monash/FIT2086/Assignment3")

#Question 1
#1.
fuel_data = read.csv("fuel.ass3.2022.csv", header=TRUE, stringsAsFactors = TRUE)
mod = lm(Comb.FE ~ ., data=fuel_data)
summary(mod)

#2.
pvalues = coefficients(summary(mod))[,4]
(pvalues<0.05/17)

#3.
coefficients(summary(mod))[3,1] #Eng.Displacement
coefficients(summary(mod))[12,1] #Drive.SysF

#4.
step.fit.bic = step(mod, k=log(nrow(fuel_data)), direction="both", trace=0)
summary(step.fit.bic)

#5a.
predict(step.fit.bic, fuel_data[33,], interval="confidence", type="response", level=0.95)


#Question 2
#1.
heart.train = read.csv("heart.train.ass3.2022.csv", header=TRUE, stringsAsFactors = TRUE)
library(rpart)
source("Wrappers.R")
tree.heart = rpart(HD ~ ., heart.train)
tree.heart.cv = learn.tree.cv(HD ~ ., data=heart.train, nfolds = 10, m = 5000)

tree.heart.cv$best.tree

#2.
plot(tree.heart.cv$best.tree)
text(tree.heart.cv$best.tree, pretty=12)

#3.
plot(tree.heart)
text(tree.heart, pretty=12)
tree.heart

#5.
lgm = glm(HD ~ ., data=heart.train, family=binomial)
summary(lgm)
step.fit.kic = step(lgm, k=3, direction="both", trace=0)
summary(step.fit.kic)

#8.
heart.test = read.csv("heart.test.ass3.2022.csv", header=TRUE, stringsAsFactors = TRUE)
source("my.prediction.stats.R")
my.pred.stats(predict(tree.heart, heart.test)[,2], heart.test$HD)
my.pred.stats(predict(step.fit.kic, heart.test, type="response"), heart.test$HD)

#9.
odds_cv = predict(tree.heart.cv$best.tree, heart.test[10,])[,2]/(1-predict(tree.heart.cv$best.tree, heart.test[10,])[,2])
odds_stepwise = predict(step.fit.kic, heart.test[10,], type="response")/(1-predict(step.fit.kic, heart.test[10,], type="response"))

#10.
library(boot)
heart.train = read.csv("heart.train.ass3.2022.csv", header=TRUE, stringsAsFactors = TRUE)
heart.test = read.csv("heart.test.ass3.2022.csv", header=TRUE, stringsAsFactors = TRUE)
lgm = glm(HD ~., heart.train, family = binomial)
step.fit.kic = step(lgm, k=3, direction="both", trace=0)
boot.odds65 = function(formula, data, test, indices)
{
  #Create a bootstrapped version of the data
  d = data[indices,]
  
  #Fit a logistic regression to the bootstrapped data
  fit = glm(formula, d, family = binomial)
  
  prob = predict(fit,test[65,],type="response")
  #calculate odds for the 65th patient
  return (prob/(1-prob))
}
bs.odds65 = boot(data=heart.train, test = heart.test, statistic= boot.odds65, 5000, formula = step.fit.kic$formula)
bs.ci65 = boot.ci(bs.odds65, 0.95, type="bca")

boot.odds66 = function(formula, data, test, indices)
{
  #Create a bootstrapped version of the data
  d = data[indices,]
  
  #Fit a logistic regression to the bootstrapped data
  fit = glm(formula, d, family = binomial)
  
  prob = predict(fit,test[66,],type="response")
  #calculate odds for the 66th patient
  return (prob/(1-prob))
}
bs.odds66 = boot(data=heart.train, test=heart.test, statistic=boot.odds66, 5000, formula = step.fit.kic$formula)
bs.ci66 = boot.ci(bs.odds66, 0.95, type="bca")


#Question 3
#1.
library(kknn)
ms.measure = read.csv("ms.measured.2022.csv")
ms.truth = read.csv("ms.truth.2022.csv")
x = replicate(25,0)
y = (1:25)
for(i in 1:25){
  knn = train.kknn(intensity ~ MZ, ms.measure, kernel="optimal")
  est = fitted(kknn(intensity ~ MZ, ms.measure, ms.truth, kernel="optimal", k=i))
  x[i] = sqrt(mean((est - ms.truth$intensity)**2))
}
plot(y,x, main = "Plot of RMSE against various values of k", xlab = "k", ylab = "RMSE")

#2.
knn = train.kknn(intensity ~ MZ, ms.measure, kernel="optimal")
est2 = fitted(kknn(intensity ~ MZ, ms.measure, ms.truth, kernel="optimal", k=2))
est6 = fitted(kknn(intensity ~ MZ, ms.measure, ms.truth, kernel="optimal", k=6))
est12 = fitted(kknn(intensity ~ MZ, ms.measure, ms.truth, kernel="optimal", k=12))
est25 = fitted(kknn(intensity ~ MZ, ms.measure, ms.truth, kernel="optimal", k=25))
#k=2
plot(ms.truth$MZ, est2, main="Graph of k=2", xlab="MZ", ylab="Intensity")
lines(ms.measure, col="red")
lines(ms.truth, col="blue")
legend(x="topright", c("Estimated Spectrum", "Training Data", "True Spectrum"), fill=c("black","red","blue") )

#k=6
plot(ms.truth$MZ, est6, main="Graph of k=6", xlab="MZ", ylab="Intensity")
lines(ms.measure, col="red")
lines(ms.truth, col="blue")
legend(x="topright", c("Estimated Spectrum", "Training Data", "True Spectrum"), fill=c("black","red","blue") )

#k=12
plot(ms.truth$MZ, est12, main="Graph of k=12", xlab="MZ", ylab="Intensity")
lines(ms.measure, col="red")
lines(ms.truth, col="blue")
legend(x="topright", c("Estimated Spectrum", "Training Data", "True Spectrum"), fill=c("black","red","blue") )

#k=25
plot(ms.truth$MZ, est25, main="Graph of k=25", xlab="MZ", ylab="Intensity")
lines(ms.measure, col="red")
lines(ms.truth, col="blue")
legend(x="topright", c("Estimated Spectrum", "Training Data", "True Spectrum"), fill=c("black","red","blue") )

#5.
knn$best.parameters

#6.
est = fitted(kknn(intensity ~ MZ, ms.measure, ms.truth, kernel="optimal", k=5))
err = ms.measure$intensity - est
sd(err)

#7.
library(kknn)
ms.measure = read.csv("ms.measured.2022.csv")
ms.truth = read.csv("ms.truth.2022.csv")
est = fitted(kknn(intensity ~ MZ, ms.measure, ms.truth, kernel="optimal", k=5))
n = length(est)
for(i in 1:n){
  if( est[i] == max(est)){
    index = i
    break
  }
}
ms.truth[index,]$MZ

#8.
library(boot)
library(kknn)
ms.measure = read.csv("ms.measured.2022.csv")
ms.truth = read.csv("ms.truth.2022.csv")
boot.est5 = function(data, truth, indices, index)
{
  #Create a bootstrapped version of the data
  d = data[indices,]
  
  return (fitted(kknn(intensity ~ MZ, d, truth[index,], kernel="optimal", k=5)))
}
bs.est = boot(data=ms.measure, truth=ms.truth, statistic=boot.est5, index=160, 5000)
bs.ci = boot.ci(bs.est, 0.95, type="bca")

boot.est3 = function(data, truth, indices, index)
{
  #Create a bootstrapped version of the data
  d = data[indices,]
  
  return (fitted(kknn(intensity ~ MZ, d, truth[index,], kernel="optimal", k=3)))
}
bs.est2 = boot(data=ms.measure, truth=ms.truth, statistic=boot.est3, index=160, 5000)
bs.ci2 = boot.ci(bs.est2, 0.95, type="bca")

boot.est20 = function(data, truth, indices, index)
{
  #Create a bootstrapped version of the data
  d = data[indices,]
  
  return (fitted(kknn(intensity ~ MZ, d, truth[index,], kernel="optimal", k=20)))
}
bs.est3 = boot(data=ms.measure, truth=ms.truth, statistic=boot.est20, index=160, 5000)
bs.ci3 = boot.ci(bs.est3, 0.95, type="bca")
