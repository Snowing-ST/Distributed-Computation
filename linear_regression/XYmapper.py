#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import sys
import numpy as np

def read_input(file): 
    for line in file:
        yield line.strip()
        #rstrip()去除字符串右边的空格 
input = read_input(sys.stdin)#依次读取每行的数据 

def XYmul(datairow):
    datairow = datairow.split(",")
    datairow = np.array(datairow,float)
    y = datairow[len(datairow)-1]
    x =  datairow[:(len(datairow)-1)]
    return x*y

mul =map(XYmul,input)
mulsum = np.sum(mul,axis = 0)
print("\t".join(str(i) for i in mulsum))



