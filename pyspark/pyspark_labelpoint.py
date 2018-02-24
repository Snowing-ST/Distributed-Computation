#!/usr/bin/anaconda2/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 16:37:30 2017

@author: situ
"""

from pyspark import SparkContext
from pyspark.mllib.regression import LabeledPoint

f=open('/home/lifeng/pc2017fall/000lifeng/stocks.csv','r')
#f=open('/home/situ/Documents/lifeng/stocks.csv','r')

data=[]
i = 0
for line in f:    
    line=line.strip().split(',')
    if line!=['exchange','stock_symbol','date','stock_price_open',
              'stock_price_high','stock_price_low','stock_price_close',
              'stock_volume','stock_price_adj_close\n']:
        del line[1:3]
        data.append(line)
len(data)

def toLabel(datairow):
    if datairow[0]=='NASDAQ':
        label = 0
    else: label=1
    pos = LabeledPoint(label,map(float, datairow[1:5]))
    return pos



data_label = map(toLabel,data)
print data_label[1]
