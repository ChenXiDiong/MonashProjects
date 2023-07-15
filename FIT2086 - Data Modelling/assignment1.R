setwd("C:/Users/User/OneDrive/Desktop/Monash/FIT2086")

my_estimate <- function(X){
  n = length(X)
  
  return (sum(X)/n)
}
dogbites <- read.csv("dogbites.1997.csv")
lambda_est <- my_estimate(dogbites$daily.dogbites)

ppois(2, lambda_est)
ppois(32, lambda_est*7)

mean(dogbites$daily.dogbites == 1)
dpois(1, lambda_est)
for(i in 0:22){
  s = paste("Probability of ", toString(i), " dogbites, observed: ", toString(mean(dogbites$daily.dogbites == i)), ", prediction model: ", toString(dpois(i, lambda_est)))
  print(s)
}

x <- 0:22
y_pred <- dpois(x, lambda_est)
y_obsv = rep(0, 23)
n = length(dogbites$daily.dogbites)
for(i in dogbites$daily.dogbites){
  y_obsv[i] = y_obsv[i] + (y_obsv[i] + 1)/n
}
plot(x,y_pred, "l", col = "red", xlab = "Number of dogbites in a day", ylab = "Probability")
lines(x, y_obsv, col = "blue")
legend(x = "topright", c("Observations", "Predictions"), fill=c("blue","red"))
