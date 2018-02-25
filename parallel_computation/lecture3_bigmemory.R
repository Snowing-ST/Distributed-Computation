#初始化
library(bigmemory)
#nrow:行数
#ncol:列数
#type:数据类型（矩阵所有数据类型必须是一样的）
#init:初始化取值      
#dinnames:list对象（两列），第一列表述行标识，第二列表示列标识
#backingfile:备份数据
#descriptorfile:描述文件
setwd("E:/graduate/class/分布式计算/lecture3")
bigData <- big.matrix(nrow=10, ncol=4, type='integer', init=2, 
                      dimnames=list(1:10,c('c1','c2', 'c3', 'c4')),   
                      backingfile='bigData.bin', descriptorfile='bigData.desc',
                      backingpath = "E:/graduate/class/分布式计算/lecture3")  
bigData
bigData[1:10,]


#加载存储的大数据对象  
loadBigData <- attach.big.matrix('bigData.desc')  
loadBigData[1:10,] 

#修改bigdata的数据  
loadBigData[,1] <- sample(1:10)  
flush(loadBigData)  
loadBigData[1:10] 

###############################

library(bigmemory)
library(biganalytics)
#try a small dataset in 2008, 600M
x <- read.csv("2008.csv",header=TRUE)
object.size(x)
rm(x)
gc()

xx <- read.big.matrix("2008.csv", type="integer", header=TRUE, #描述文件？？？
                     backingfile="airline2.bin",
                     backingpath = "E:/graduate/class/分布式计算/lecture3", 
                     descriptorfile="airline2.desc")
object.size(xx)
dim(xx)

#对矩阵进行操作
xx <- attach.big.matrix("airline2.desc")
summary(xx[,"ArrDelay"])
summary(xx[,15])
hist(xx[,"ArrDelay"])
ArrDelay <- xx[,"ArrDelay"]

#mwhich 操作
x <- as.big.matrix(matrix(1:30, 10, 3)) 
x
x[,]
#第一列中大于等于2小于等于3的行
#即x[2<=x[,1]<=3,]
x[mwhich(x, 1, list(c(2,3)), list(c('ge','le')),),]  
#第二列中小于17大于14的行
x[mwhich(x, 2, list(c(14,17)), list(c('gt','lt')),),]  
#前两个筛选条件用or合并
x[mwhich(x, 1:2, list(c(2,3), c(14,17)), list(c('ge','le'), c('gt', 'lt')), 'OR'),]  
sub.big.matrix(x, 2, 9, 2, 3)[,]
#第一个参数不用多说，第二个参数是起始行  第三个参数是结束行  第四个参数是开始列  第五个参数是结束列  


#计算飞机的月龄
birthmonth <- function(y) {
  minYear <- min(y[,'Year'], na.rm=TRUE)
  these <- which(y[,'Year']==minYear)
  minMonth <- min(y[these,'Month'], na.rm=TRUE) #最小年份中找最小月份
  return(12*minYear + minMonth - 1)
}

##对所有飞机进行操作
allplanes <- unique(xx[,'TailNum'])
length(allplanes)

planeStart <- rep(0, length(allplanes))
j=1
for (i in allplanes) {
  planeStart[j] <- birthmonth( xx[mwhich(xx, 'TailNum', i, 'eq'),#tailnum 机尾唯一编号
                                 c('Year', 'Month'), drop=FALSE] )
  j=j+1
}

#用foreach
#参考课件R中的内存管理


#the final age
xx$age <- xx[,"Year"]*as.integer(12)+xx[,"Month"]-as.integer(planeStart[xx[,"TailNum"]])


#big regression
blm <- biglm.big.matrix(ArrDelay ~ Distance + Month + DayOfWeek, data=xx)
summary(blm)

