#!/usr/bin/anaconda2/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 07:56:09 2017

@author: situ
"""
from pyspark.mllib.linalg import Matrix, Matrices
from pyspark import SparkContext
import numpy as np

f=open('/home/lifeng/pc2017fall/000lifeng/stocks.csv','r')
#f=open('/home/situ/Documents/lifeng/stocks.csv','r')

data=[]
i = 0
for line in f:    
    line=line.split(',')[3:7]
    if line!=['stock_price_open','stock_price_high',
              'stock_price_low','stock_price_close']:

        data.extend(map(float,line))
       
p = 4    
n = len(data)/p;n


mat=Matrices.dense(n,p,data)
print mat

