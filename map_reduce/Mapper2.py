#!/usr/bin/env python 
#coding=utf-8 
import sys 
def read_input(file): 
    for line in file:
        line = line.rstrip()
        yield line.split(",")[2]
        #rstrip()去除字符串右边的空格 
input = read_input(sys.stdin)#依次读取每行的数据 

input = [line for line in input]
del input[0]
#print(input[:5])
input = [float(line) for line in input]#将每行转换成float型 
numInputs = len(input) 
meanInput = sum(input)/numInputs
sqInput = sum([x**2 for x in input])/numInputs
#输出数据个数，均值，以及平方和的均值，以'\t'隔开 
print "%d\t%f\t%f" % (numInputs, meanInput, sqInput)
