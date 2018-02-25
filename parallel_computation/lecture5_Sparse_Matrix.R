library('Matrix') #M大写

m1 <- matrix(0, nrow = 1000, ncol = 1000)
m2 <- Matrix(0, nrow = 1000, ncol = 1000, sparse = TRUE)

object.size(m1)
# 8000200 bytes
object.size(m2)
# 5632 bytes


m1[500, 500] <- 1
m2[500, 500] <- 1

object.size(m1)
# 8000200 bytes
object.size(m2)
# 5648 bytes


# 基于稀疏矩阵的运算
m2 %*% rnorm(1000)
m2 + m2 #用点点表示
m2 - m2
t(m2)

m3 <- cBind(m2, m2) #B大写
nrow(m3)
ncol(m3)
m4 <- rBind(m2, m2)
nrow(m4)
ncol(m4)

summary(m2)


####################变量选择
library('Matrix')
library('glmnet')
n <- 10000
p <- 500

x <- matrix(rnorm(n * p), n, p)
iz <- sample(1:(n * p),
             size = n * p * 0.85,
             replace = FALSE)
x[iz] <- 0
object.size(x)

sx <- Matrix(x, sparse = TRUE) #Matrix作用在普通矩阵
object.size(sx)

beta <- rnorm(p)
y <- x %*% beta + rnorm(n)

#logistic建模
glmnet.fit <- glmnet(x, y)
summary(glmnet.fit)
glmnet.fit <- glmnet(sx, y)


#节省的时间
library(ggplot2)
set.seed(1)
performance <- data.frame()

for (sim in 1:10)
{
  n <- 10000
  p <- 500
  
  nzc <- trunc(p / 10)
  x <- matrix(rnorm(n * p), n, p)
  iz <- sample(1:(n * p),
               size = n * p * 0.85,
               replace = FALSE)
  x[iz] <- 0
  sx <- Matrix(x, sparse = TRUE)
  
  beta <- rnorm(nzc)
  fx <- x[, seq(nzc)] %*% beta
  
  eps <- rnorm(n)
  y <- fx + eps
  
  sparse.times <- system.time(fit1 <- glmnet(sx, y))
  full.times <- system.time(fit2 <- glmnet(x, y))
  sparse.size <- as.numeric(object.size(sx))
  full.size <- as.numeric(object.size(x))
  
  performance <- rbind(performance, data.frame(Format = 'Sparse',
                                               UserTime = sparse.times[1],
                                               SystemTime = sparse.times[2],
                                               ElapsedTime = sparse.times[3],
                                               Size = sparse.size))
  performance <- rbind(performance, data.frame(Format = 'Full',
                                               UserTime = full.times[1],
                                               SystemTime = full.times[2],
                                               ElapsedTime = full.times[3],
                                               Size = full.size))
}
performance
spar <- seq(1,20,2)
apply(performance[spar,2:5],2,mean)
apply(performance[-spar,2:5],2,mean)



##########################社交网络应用
#simple example
A <- rbind(c(0,1,0),c(0,0,1),c(1,0,0));A

#共同粉丝矩阵：矩阵相乘
struc1=t(A)%*%A;struc1 #在（1,2）位置元素为0，说明1 和 2的共同粉丝数为0
#共同关注数
struc2=A%*%t(A);struc2
#正向传递
struc3=A%*%A;struc3


# a real example
setwd("E:/graduate/class/分布式计算/lecture5/")
library(readr)
library(Matrix)
library(plyr)

dat=readLines("2014-03-07u_info.csv")

head(dat)
#UID，label，area，gender，follower，followee，tweets，
tmp=strsplit(dat,"\t")
uid=sapply(tmp,function(s){
  ifelse(nchar(s[1])==11,as.numeric(s[1]),NA) #uid刚好是11位的用户
})
flag=is.na(uid)==F
tmp=tmp[flag]
uid=uid[flag]
length(uid) #8424个用户


#整理邻接矩阵
dat1=read_csv("2014-03-07guanzhu.csv",col_names = F)
head(dat1)
dim(dat1)

tmp1=sapply(dat1,function(s){
  res=strsplit(s,"\t")
  return(res)})

rm(dat1)
tmp1=unlist(tmp1)
tmp1=as.numeric(tmp1)
rel=matrix(tmp1,byrow=T,ncol=2) 
#注意这个矩阵中包含的关系可能不全在uid之中，所以要去掉一部分的边.

flag=is.element(rel[,1],uid)*is.element(rel[,2],uid)
rel=rel[flag==1,]  #只取两个元素都在列表中的关系

N=length(uid)
adj=matrix(0,N,N)
for (i in 1:nrow(rel)){
  s1=which(uid==rel[i,1]) #找前面的人
  s2=which(uid==rel[i,2]) #找后面的人
  adj[s1,s2]=1}  #建立邻接矩阵，前面的人关注了后面的人


adj1=Matrix(adj,sparse=T)   #转化为稀疏矩阵存储

#共同粉丝矩阵
struc1=t(adj1)%*%adj1 #运行速度比普通矩阵相乘快
#共同关注数
struc2=adj1%*%t(adj1)
#正向传递
struc3=adj1%*%adj1




#for the small dataset
setwd("E:/graduate/class/分布式计算/lecture5/")
dat=read.csv("u_info_example.csv",header=F)
uid=dat[,1]
dat1=read.csv("guanzhu_example.csv",header=F)
head(dat1)
dim(dat1)
rel=dat1


flag=is.element(rel[,1],uid)*is.element(rel[,2],uid)
rel=rel[flag==1,]  #只取两个元素都在列表中的关系

N=length(uid)
adj=matrix(0,N,N)
for (i in 1:nrow(rel)){
  s1=which(uid==rel[i,1])
  s2=which(uid==rel[i,2])
  adj[s1,s2]=1}  #建立邻接矩阵


###################文本分析

ii <- c(1, 3:8)
jj <- c(2, 9, 6:10)
x <- 7 * (1:7)
(A <- sparseMatrix(ii, jj, x = x))  #从例子中可以看出，i，j是行列标号。x是取值

rm(list=ls())
##设置路径
setwd("C:/Users/ff/Desktop/")  
##加载R包                                                                                                          
library(jiebaRD)
library(jiebaR)                                                       


setwd("E://my workfiles//人民大学//教学//并行计算课件//我的课件//lecture5")
##读入comments数据
com_data=read.csv("./text.csv", header = T, stringsAsFactors = F)
head(com_data)


####提取评论所在的列
comments=com_data$评论内容
####统计词数
words=nchar(comments)
ratings=com_data$评论得分
phoneid=com_data$手机编号


##对全部评论进行分词
library(jiebaRD)
library(jiebaR) 
####初始化分词器
cutter = worker('tag',bylines = TRUE) 
####进行分词,这步会比较慢                                      
res = cutter[comments]      
res[1]

##对全部评论进行处理
####将text从list转换为matrix格式
text = lapply(res,as.matrix)
####将每行文本的分词结果逐一排列起来
text = as.data.frame(do.call(rbind, text), stringsAsFactors = F) 
##提取高频词作为关键词
####进行词频统计
freq = as.data.frame(table(text),stringsAsFactors = F) 
####按词频个数降序排列           
freq = freq[order(-freq[,2]),]  
####挑选前50个高频词                                
top50 = freq[1:50,];top50


#生成向量空间矩阵
N=length(comments)
D=dim(freq)[1] #D个词
Dic=freq[,1]
#for 循环
vsm=matrix(0,N,D) #向量空间矩阵？！......
for(i in 1:N)
{
  theres=res[[i]]
  index=apply(as.matrix(theres),1,function(x){which(Dic==x)})
  index2=unique(index)
  vsm[i,index2]=1
}
object.size((vsm))


ii=0
jj=0
for(i in 1:N) #稀疏矩阵的方式
{
  theres=res[[i]]
  index=apply(as.matrix(theres),1,function(x){which(Dic==x)})
  index2=unique(index)
  jj=c(jj,index2)
  ii=c(ii,rep(i,length(index2)))
}
ii=ii[-1]
jj=jj[-1]

A <- sparseMatrix(ii, jj, x = 1)
object.size(A)

summary(ratings)
hist(ratings)
y=rep(0,N)
y[ratings>3]=1 #把5级评分变成2分类


glm.fit=glmnet(A,y,family="binomial")
plot(glm.fit)
coefficients<-coef(glm.fit)
coeff1=coefficients[,50] #第50个lambda？
Active.Index<-which(coeff1!=0) 
length(Active.Index)
Dic[Active.Index[-1]] #有显著作用的词

#交叉验证选择最优lambda值
#cv.fit=cv.glmnet(A,y,family="binomial")
#cv.fit$lambda.min  #最佳lambda值
#glm.fit=glmnet(A,y,family="binomial")
#coefficients<-coef(glm.fit,s=cv.fit$lambda.min)
#Active.Index<-which(coefficients!=0) 
#length(Active.Index)
#Dic[Active.Index[-1]]

