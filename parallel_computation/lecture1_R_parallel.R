
#lapply
doit <- function(x)(x)^2 + 2*x
system.time(res <- lapply(1:5000000,  doit))



#use parallel
library(parallel)  #加载包
cl.cores <- detectCores()  #检查当前电脑可用核数
cl <- makeCluster(cl.cores)  #使用刚才检测的核并行运算

system.time({
 res <- parLapply(cl, 1:5000000,  doit)
})


#another example
nSims <- 100
input <- seq_len(nSims) # same as 1:nSims but more robust

testFun <- function(i)
{
 mn <- mean(rnorm(1000000))
 return(mn)
}

system.time(
res <- lapply(input, testFun)
)


system.time(
res <- parLapply(cl, input, testFun)
)

summary(unlist(res))
hist(unlist(res))

############################一元二次方程求解
# Author: Peng Zhao, 8/30/2016

solve.equation <- function(a, b, c) 
{
  # Not validate eqution: a and b are almost ZERO
  if(abs(a) < 1e-8 && abs(b) < 1e-8) return(c(NA, NA) )

  # Not validate eqution: a,b and c are almost ZERO
  if(abs(a) < 1e-8 && abs(b) < 1e-8) return(c(NA, NA) )
  
  # Not quad equation
  if(abs(a) < 1e-8 && abs(b) > 1e-8) return(c(-c/b, NA))
  
  # No Solution
  if(b*b - 4*a*c < 0) return(c(NA,NA))
  
  # Return solutions
  x.delta <- sqrt(b*b - 4*a*c)
  x1 <- (-b + x.delta)/(2*a)
  x2 <- (-b - x.delta)/(2*a)
  
  return(c(x1, x2))
}

# Generate data    
len <- 1e7
a <- runif(len, -10, 10)
a[sample(len, 100,replace=TRUE)] <- 0

b <- runif(len, -10, 10)
c <- runif(len, -10, 10)


# serial code
system.time(
    res1.s <- lapply(1:len, FUN = function(x) { solve.equation(a[x], b[x], c[x])})
)


# parallel
cores <- detectCores(logical = FALSE)
cl <- makeCluster(cores)
clusterExport(cl, c('solve.equation', 'a', 'b', 'c'))
system.time(
   res1.p <- parLapply(cl, 1:len, function(x) { solve.equation(a[x], b[x], c[x]) })
)

stopCluster(cl)


##########################################################################################
#foreach
library(foreach)
#利用foreach重复运行sqrt函数
foreach(i=1:3) %do% sqrt(i)

foreach(a=1:3, b=rep(10, 3))%do% {
  a + b
}

foreach(a=1:1000, b=rep(10, 2)) %do% (a + b)

foreach(a=1:3, b=rep(10, 3), .combine="c") %do%
{
 x1<-(a + b);
 x2<-a*b;
 c(x1,x2);  
}

foreach(a=1:3, b=rep(10, 3), .combine="cbind") %do%
{
 x1<-(a + b);
 x2<-a*b;
 c(x1,x2);  
}
#also try cbind

#try to use another function
foreach(a=1:3, b=rep(10, 3), .combine="+") %do%
{
 x1<-(a + b);
 x2<-a*b;
 c(x1,x2);  
}

foreach(a=1:3, b=rep(10, 3), .combine="*") %do%
{
 x1<-(a + b);
 x2<-a*b;
 c(x1,x2);  
}

#.combine还可以自己编写函数来实现，如下例：

cfun <- function(a, b) a+b
foreach(a=1:3, b=rep(10, 3), .combine="cfun") %do%
{
 x1<-(a + b);
 x2<-a*b;
 c(x1,x2);  
}

#when
library(iterators)
foreach(a=irnorm(1, count=10), .combine='c') %do% a
foreach(a=irnorm(2, count=10), .combine='cbind') %do% a
foreach(a=irnorm(1, count=10), .combine='c') %:% when(a >= 0) %do% sqrt(a)


#并行运算other tasks
#begin
library(doParallel)
cl <- makeCluster(2)
registerDoParallel(cl)

taskFun <- function(i){
  set.seed(i)
  mn <- mean(rnorm(1000000))
  return(mn)
}

out=rep(0,40)
system.time(
for(i in 1:40) {
    out[i] <- taskFun(i)
  }
)


system.time(
  out1 <- foreach(i = 1:40) %do% {
    outSub <- taskFun(i)
  }
)

system.time(
  out1 <- foreach(i = 1:40) %dopar% {
    outSub <- taskFun(i)
  }
)

hist(out1)
stopCluster(cl)


# Boostrap Example
library(doParallel)
cl <- makeCluster(2)
registerDoParallel(cl)


# Parallel by dopar
x <- iris[which(iris[,5] != "setosa"), c(1,5)]
trials <- 10000
ptime <- system.time({
 r <- foreach(icount(trials), .combine=cbind) %dopar% {
 ind <- sample(100, 100, replace=TRUE)
 result1 <- glm(x[ind,2]~x[ind,1], family=binomial(logit))
 coefficients(result1)
 }
})
ptime

#Sequential by do
stime <- system.time({
 r <- foreach(icount(trials), .combine=cbind) %do% {
 ind <- sample(100, 100, replace=TRUE)
 result1 <- glm(x[ind,2]~x[ind,1], family=binomial(logit))
 coefficients(result1)
 }
 })
stime

stopCluster(cl)

#random forests
library(doParallel)
cl <- makeCluster(2)
registerDoParallel(cl)
library(randomForest)

#生成矩阵x作为输入值，y作为目标因子
x <- matrix(runif(500), 100)
y <- gl(2, 50)  #Generate factors by specifying the pattern of their levels. 

#按顺序执行
system.time(
rf <- foreach(ntree=rep(200, 6), .combine=combine) %do% 
 randomForest(x, y, ntree=ntree)
)

system.time(
rf <- foreach(ntree=rep(200,6), .combine=combine, .packages="randomForest") %dopar%   
  randomForest(x, y, ntree=ntree)  
)


############################内存管理
ls()
object.size("a1")
memory.size()
memory.limit()


