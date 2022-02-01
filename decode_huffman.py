# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 13:45:31 2022

@author: simon

Tree building and Hufman encoding is based on:
https://github.com/YCAyca/Data-Structures-and-Algorithms-with-Python/blob/main/Huffman_Encoding/huffman.py
"""

import os
import sys
import numpy as np
import pickle
from huffman import *


def decode_huffman(filename, outfile):
    dumpster = pickle.load(open( filename, 'rb' ))
    tree = dumpster['tree']
    binar = dumpster['bin']
    N = dumpster['N']
    L = dumpster['L']

    encode = ''
    for byte in binar:
        bb = np.unpackbits(byte)
        for b in bb:
            encode += str(b)

    decode = Huffman_Decoding(encode,tree)

    with open(outfile, 'w') as text_file:
        text_file.write(decode)

def main():
    filename = './out.bro' # default for debuging
    if(len(sys.argv) > 1):
        filename = sys.argv[1] # use first command line argument as file
    # outfile = filename.split('.')[0:-1] + '.bro'
    if(len(sys.argv) > 2):
        outfile = sys.argv[2]
    else:
        outfile = filename + '.txt'
    
    print(f'File:\t{filename.split("/")[-1]}')
    L = os.path.getsize(filename)
    print(f'Length:\t{L:2}')
    decode_huffman(filename, outfile)

if __name__ == "__main__":
    main()




