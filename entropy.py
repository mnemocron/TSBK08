#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 17:38:19 2022

@author: simon burkhardt, github.com/mnemocron, simbu448@student.liu.se
@file:   entropy.py
#date:   2022-01-21
"""

import math
import sys
import time
import numpy as np
from scipy.stats import entropy

def get_entropy(filename, k):
    with open(filename, 'rb') as f:
        data = np.fromfile(f, np.dtype('B'))
    p = np.zeros([256, 1])
    for e in data:
        p[e] += 1
    p = p/len(data)
    H = 0
    for pp in p:
        if pp>0:
            H += pp * np.log2(pp)
    H = -H
    return H[0]

def entropy_estimation(filename, k):
    cnt = 0       # total byte length
    H = 0         # entropy
    alphabet = {} # alphabet for symbols that will occur
    with open(filename, 'rb') as f:
        byte = [f.read(1) for i in range(k+1)] # array of one or multiple bytes
        while byte[-1] != b"":
            key = "".join(str(_) for _ in byte) # treat multiple bytes as one symbol in alphabet
            alphabet[key] = alphabet.get(key, 0) + 1 # increment occurrence count
            cnt += 1
            byte.pop(0)            # trash last byte in memory
            byte.append(f.read(1)) # append newest byte to array
    
    # calculate probabilities
    for key in alphabet:
        p = alphabet[key]
        if(p > 0):
            p /= cnt
            H += p * math.log2(p) # sum up entropy
    H = -H
    return H

def conditional_entropy_estimation(filename, k, l):
    cnt = 0       # total byte length
    H = 0         # entropy
    
    # 3 different things must be counted in separate alphabets
    # - single symbols (x_n+1)
    # - previous k symbols (x_n, ... x_n-k)
    # - previous k+1 symbols (xn+1, x_n, ... x_n-k)
    
    alphabet = {} # alphabet for previous k+1 symbols (xn+1, x_n, ... x_n-k)
    alpha_single = {} # alphabet single symbols (x_n+1)
    alpha_minus = {}  # alphabet for previous k symbols (x_n, ... x_n-k)

    # count single characters and full sequence
    with open(filename, 'rb') as f:
        byte = [f.read(1) for i in range(k+1)]
        while byte[-1] != b"":
            key = "".join(str(_) for _ in byte)
            alphabet[key] = alphabet.get(key, 0) + 1
            cnt += 1
            b = byte.pop(0)
            alpha_single[b] = alpha_single.get(b, 0) + 1
            byte.append(f.read(1))
         
    k -=1
    if (k<0):
        k=0
    cnt = 0
    # run again but cound one less symbols
    with open(filename, 'rb') as f:
        byte = [f.read(1) for i in range(k+1)]
        while byte[-1] != b"":
            key = "".join(str(_) for _ in byte)
            alpha_minus[key] = alpha_minus.get(key, 0) + 1
            cnt += 1
            b = byte.pop(0)
            byte.append(f.read(1))   

    # for each predecessing combination of k symbols: yi = { x_n, x_n-1 ...}
    for tupl in alpha_minus: # for j=1 ... M
        # calculate pY(yi)
        py = alpha_minus[tupl] / sum(alpha_minus.values())
        #print(f'py ( {tupl} ) = {py}')
        ocr = 0
        # calculate H (X|Y=yi)
        for pair in alphabet:
            if pair.startswith(str(tupl)):
                ocr += alphabet[pair]
        # conditional probability, given condition: startswith()
        Hc = 0
        for sym in alpha_single:  # for i=1 ... L
            key = str(tupl) + str(sym)
            #key = str(sym) + str(tupl)
            if(key in alphabet): # not every combination may have occurred and is in the alphabet
                pcond = alphabet[key] / ocr
                # print(f'p(X|{key}) = {alphabet[key]} / {ocr}')
                Hc += pcond * math.log2(pcond)
        H += py * Hc
    H = -H
    return H
    
    
def file_length(filename):
    cnt = 0
    with open(filename, 'rb') as f:
        byte = f.read(1)
        while byte != b"":
            cnt += 1
            byte = f.read(1)
    return cnt
    
def main():
    filename = './infiles/cantrbry/xargs.1' # default for debuging
    # filename = './infiles/cantrbry/ptt5' # default for debuging
    # filename = './infiles/ab.txt'
    if(len(sys.argv) > 1):
        filename = sys.argv[1] # use first command line argument as file
    
    print(f'File:\t{filename.split("/")[-1]}')
    L = file_length(filename)
    print(f'Length:\t{L:2}')
    
    print('Memory (k)\t\tEntropy H(Xn,...,Xn+k)\t\tEntropy H(Xn+k|Xn,...Xn+k-1)\tMax compression')
    H = get_entropy(filename, 1)
    print(f'{H}')
    
    """
    for k in range(4):
        H1 = entropy_estimation(filename, k)
        H2 = conditional_entropy_estimation(filename, k, 1)
        if(H2 < 0.000001):
            H2 = H1
        R1 = H1/8
        R2 = H2/8
        R = min(R1, R2)
        print(f'{k}\t\t\t\t{H1:.6}\t\t\t\t\t\t{H2:.6}\t\t\t\t\t\t\t{R:.6}')
        # print(f'{k} \t\t {H:7.6}', end = '')
    """

if __name__ == "__main__":
    main()



