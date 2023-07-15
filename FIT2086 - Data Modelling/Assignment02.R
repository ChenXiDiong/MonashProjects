setwd("C:/Users/User/OneDrive/Desktop/Monash/FIT2086/Assignment 2")

#Q1.1
covidcases <- read.csv("daily.covid.aug1to7.csv")
mean_hat <- mean(covidcases$daily.covid.cases)
var_hat <- var(covidcases$daily.covid.cases)
size <- length(covidcases$daily.covid.cases)
t_value <- qt(p = 1-0.05/2, df=size-1)

mean_hat - t_value*sqrt(var_hat/size)
mean_hat + t_value*sqrt(var_hat/size)

#Q1.2
covidcases2 <- read.csv("daily.covid.aug8to14.csv")
mean_hat2 <- mean(covidcases2$daily.covid.cases)
var_hat2 <- var(covidcases2$daily.covid.cases)
size2 <- length(covidcases2$daily.covid.cases)

mean_diff <- mean_hat - mean_hat2
mean_diff - 1.96*sqrt(var_hat/size+var_hat2/size2)
mean_diff + 1.96*sqrt(var_hat/size+var_hat2/size2)

#Q1.3
z <- (mean_hat - mean_hat2)/sqrt(var_hat/size + var_hat2/size2)
p <- 2*pnorm(-abs(z))
p

#Q2.1
y = (0:25)
v1 = 0
r1 = 1
p1 = choose(y+r1-1,y)*(r1^r1)*((exp(v1)+r1)^(-r1-y))*exp(y*v1)
plot(y,p1, xlab="y Value", ylab="Negative Binomial PMF", main="Graph of y Against Negative Binomial PMF", type="l")
v2 = 1
r2 = 2
p2 = choose(y+r2-1,y)*(r2^r2)*((exp(v2)+r2)^(-r2-y))*exp(y*v2)
lines(y,p2, col="red")
v3 = 1.5
r3 = 2
p3 = choose(y+r3-1,y)*(r3^r3)*((exp(v3)+r3)^(-r3-y))*exp(y*v3)
lines(y,p3, col="blue")
legend(x = "topright", c("v=0, r=1", "v=1,r=2", "v=1.5, r=2"), fill=c("black","blue","red"))


#Q3.1
data = c(rep(1, 176),rep(0,64))
n = length(data)
mu = mean(data)
var = var(data)
student_t = qt(p= 1-0.05/2, df=n)
CI_min = mu-student_t*sqrt(var/n)
CI_max = mu+student_t*sqrt(var/n)

#Q3.2
mu0 = 0.5
z = (mu-mu0)/sqrt(mu0*(1-mu0)/n)
p = 2*pnorm(-abs(z))

#Q3.3
res = binom.test(x=176, n=240)
?binom.test
res$p.value

#Q3.4
mu_diff = (176/240) - (210/240)
thetap = (210+176)/480
z = mu_diff/sqrt(thetap*(1-thetap)*120)
p = 2*pnorm(-abs(-3.911))
p
