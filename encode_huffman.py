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

def encode_huffman(filename, outfile):    
    f = open(filename, "rb")
    data = f.read()
    f.close()
    # print(data)
    encoding, tree = Huffman_Encoding(data)
    
    # next step: encode into binary file
    # preamble: number of bits in file OOOORRR number of bytes to recover from file (and ignore trailing bits)
    # tree information
    N = len(data)     # length of original data (bytes)
    L = len(encoding) # length of encoded data (bits)
    
    # padding with zeros to make the length a multiple of 8
    while len(encoding)%8 != 0:
        encoding += '0'  
    
    # write to file
    binar = np.zeros([np.ceil(L/8).astype(np.uint32), 1], dtype=np.uint8)
    for i in range(len(binar)):
        ff = encoding[0+i*8 : 8+i*8]
        mybyte = 0
        for j in range(8):
            if ff[7-j] == '1':
                mybyte += pow(2,j)
        binar[i] = mybyte
    
    dumpster = {}
    dumpster['tree'] = tree
    dumpster['bin'] = binar
    dumpster['N'] = N
    dumpster['L'] = L
    
    pickle.dump(dumpster, open( outfile, 'wb' ))
    
    siz1 = os.path.getsize(outfile)
    siz2 = os.path.getsize(filename)
    print(f'Actual file compression ratio: {siz1/siz2:.7}')

def main():
    # filename = './infiles/cantrbry/alice29.txt' # default for debuging (text file)
    filename = './infiles/cantrbry/ptt5' # default for debuging (binary file)
    if(len(sys.argv) > 1):
        filename = sys.argv[1] # use first command line argument as file
    # outfile = filename.split('.')[0:-1] + '.bro'
    if(len(sys.argv) > 2):
        outfile = sys.argv[2]
    else:
        outfile = './out.bro'
    
    print(f'File:\t{filename.split("/")[-1]}')
    print(f'Out:\t{outfile.split("/")[-1]}')
    L = os.path.getsize(filename)
    print(f'Length:\t{L:2}')
    encode_huffman(filename, outfile)
    
if __name__ == "__main__":
    main()


