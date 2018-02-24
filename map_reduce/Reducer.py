#!/usr/bin/env python 
#coding=utf-8 
import sys 
def read_input(file): 
    for line in file: 
        yield line.rstrip() 
        
input = read_input(sys.stdin) 
#读取map端的输出，共有三个字段，按照'\t'分隔开来 
mapperOut = [line.split('\t') for line in input] 
cumVal=0.0 
cumSumSq=0.0 
cumN=0.0

for instance in mapperOut: 
    nj = float(instance[0])#第一个字段是数据个数 
    cumN += nj 
    cumVal += nj*float(instance[1])
    #第二个字段是一个map输出的均值，均值乘以数据个数就是数据总和 
    cumSumSq += nj*float(instance[2])
    #第三个字段是一个map输出的平方和的均值，乘以元素个数就是所有元素的平方和 
mean = cumVal/cumN#得到所有元素的均值 
var = (cumSumSq/cumN-mean*mean)#得到所有元素的方差 
print "%d\t%f\t%f" % (cumN, mean, var)
