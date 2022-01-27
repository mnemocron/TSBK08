# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 13:02:23 2022

@author: simon
"""

import math
import sys
import time
import numpy as np

def build_tree(lengths, positions):
    pass


def compress(infile, outfile):
    # static huffman
    # 1. pass, get probabilities
    prb = get_probabilities(infile)
    prb = np.array( [[b,i] for i,b in enumerate(prb) if b > 0] , dtype=object)  # add indices which represent the byte value
    prb = prb[ np.argsort(prb[:,0]) ]  # sort by number of probabilities to build tree
    prb = prb[::-1] # reverse order to have max probability first
    # build tree
    N = len(prb)
    # what is lmin?
    for p in prb:
        pass
    
    # 2. pass, encode
    
    pass

def uncompress(infile, outfile):
    pass

def get_probabilities(filename):
    with open(filename, 'rb') as f:
        data = np.fromfile(f, np.dtype('B'))
    p = np.zeros([256, 1])
    for e in data:
        p[e] += 1
    p = p/len(data)
    return p


def main():
    filename = './infiles/cantrbry/xargs.1' # default for debuging
    # filename = './infiles/cantrbry/ptt5' # default for debuging
    # filename = './infiles/ab.txt'
    if(len(sys.argv) > 1):
        filename = sys.argv[1] # use first command line argument as file
        
    compress(filename, f'{filename}.pim')
    uncompress(f'{filename}.pin', f'{filename}.2')

if __name__ == "__main__":
    main()
