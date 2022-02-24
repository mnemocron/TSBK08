# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 16:22:35 2022

@author: simon
"""

import numpy as np

filename = ["cantrbry/alice29.txt"]

def read_file(filename):
    # Load bytes from file and count symbol occurances
    with open(filename, "rb") as f:  # 'rb' means read binary
        data = f.read()
        return data

data = read_file(filename[0])

data = [1,2,3,1,2,1,2,1,2]
datasize = len(data)

# The problem is here with multidimmensional arrays
# "dic" should be a dictionary e.g.
# dic = [[], [1], [2], [1,2], [1,2,3]]
# using numpy it will only ever append a single number but not the sym=[1,2] array
# so maybe use an acual dictionary
# but then the "sym in dic" search will fail with [1,2] symbol

dic = np.array([[]], dtype= np.uint8)  # 1. using numpy
# dic = [[]]  # 2. using dict

idx = 0
sym = np.array([], dtype=np.uint8)
k = 0
while(idx < datasize):
    # append new symbol to current symbol chain
    sym = np.append(sym, np.uint8(data[idx]) )
    print(f"new sym: {sym} --> {sym in dic}")
    
    if(sym in dic):
        # match!
        k = np.where(dic == sym)[0][0]
        # good! look further ahead until not a match anymore
        print(f"match {sym} at dic[ {k} ]")
    else:
        dic = np.append(dic, sym) # 1. using numpy
        #dic.append(sym) # 2. using dict
        
        print(f"new dict entry {sym} --> {dic[-1]}")
        code = [k, sym[-1] ]
        print(f"code: <{k}, {sym[-1]}>")
        sym = np.array([], dtype=np.uint8)    
    idx = idx+1





