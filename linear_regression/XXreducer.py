#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
XXreducer

Created on Fri Dec 15 23:44:27 2017

@author: situ
"""

import sys 
import numpy as np

def read_input(file):
    for line in file:
        yield line.strip()
input = read_input(sys.stdin) 

#loop to sum up
#length = 0
#
#for line in input:
#    fields = line.split("\t")
#    if length == 0:
#        length = len(fields) #p*p dim
#        sumup = np.array([0.0 for _ in range(length)])
#    fields = np.array(fields,dtype = float)
#    sumup += fields


#map to sum up
def forsumup(datairow):
    datairow = datairow.split("\t")
    datairow = np.array(datairow,float)
    return datairow
vecsumup = np.array(map(forsumup,input))
sumup = np.sum(vecsumup,axis = 0)

p = int(np.sqrt(len(sumup)))
print np.matrix(sumup.reshape(p,p)) #vector to matrix

