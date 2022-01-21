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

def entropy_estimation(filename, k):
    cnt = 0       # total byte length
    H = 0         # entropy
    alphabet = {} # alphabet for symbols that will occurr
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
    cnt = 0
    alphabet = {}
    with open(filename, 'rb') as f:
        byte = [f.read(1) for i in range(k+1)]
        while byte[-1] != b"":
            key = "".join(str(_) for _ in byte)
            alphabet[key] = alphabet.get(key, 0) + 1
            cnt += 1
            byte.pop(0)
            byte.append(f.read(1))
            
    H = 0
    
    for key in alphabet:
        p = alphabet[key]
        if(p > 0):
            p /= cnt
            H += p * math.log2(p)
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
    if(len(sys.argv) > 1):
        filename = sys.argv[1] # use first command line argument as file
    
    print(f'File:\t{filename.split("/")[-1]}')
    L = file_length(filename)
    print(f'Length:\t{L:2}')
    
    print('Memory (k)\t\tEntropy H(Xn,...,Xn+k)\t\tEntropy H(Xn+k|Xn,...Xn+k-1)\tMax compression')
    
    for k in range(4):
        H1 = entropy_estimation(filename, k)
        H2 = conditional_entropy_estimation(filename, k, 1)
        R1 = H1/8
        R2 = H2/8
        R = min(R1, R2)
        print(f'{k}\t\t\t\t{H1:.5}\t\t\t\t\t\t{H2:.5}\t\t\t\t\t\t\t{R:.4}')
        # print(f'{k} \t\t {H:7.6}', end = '')

if __name__ == "__main__":
    main()



