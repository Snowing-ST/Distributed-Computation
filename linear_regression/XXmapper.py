#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
XXmapper

Created on Fri Dec 15 23:11:30 2017

@author: situ
"""

import sys
import numpy as np

def read_input(file): 
    for line in file:
        yield line.strip()
        #rstrip()去除字符串右边的空格 
input = read_input(sys.stdin)#依次读取每行的数据 
#input = [line for line in input]
def XXmul(datairow):
    datairow = datairow.split(",")
    datairow = np.matrix(datairow,float)
    x =  datairow[0,:(datairow.shape[1]-1)]
    return np.dot(x.T,x)

mul = np.array(map(XXmul,input))
mulsum = np.sum(mul,axis = 0)


mulsum2 = mulsum.reshape(1,len(mulsum)**2) #matrix to vector
mulsum2 = list(mulsum2[0])
print("\t".join(str(i) for i in mulsum2))