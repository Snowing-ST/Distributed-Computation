#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 03:59:20 2017

@author: situ
"""

import sys 
import numpy as np

def read_input(file):
    for line in file:
        yield line.strip()
      
input = read_input(sys.stdin) 
length = 0
for line in input:
    fields = line.split("\t")
    if length == 0:
        length = len(fields) #p dim
        data = np.array([0.0 for _ in range(length)])
    fields = np.array(fields,dtype = float)
    data += fields
print data