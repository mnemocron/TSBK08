# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 16:03:08 2022

@author: simon
"""

import os
import sys
import numpy as np
import pickle
from huffman import *


filename = './infiles/cantrbry/alice29.txt' # default for debuging (binary file)

if(len(sys.argv) > 1):
    filename = sys.argv[1] # use first command line argument as file
# outfile = filename.split('.')[0:-1] + '.bro'
if(len(sys.argv) > 2):
    outfile = sys.argv[2]
else:
    outfile = './out.bro'
    
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

filename = outfile

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

decode = ( Huffman_Decoding(encode,tree) )

# todo: use length to write correct amount of bytes to output
outfile = 'thing.bin'
with open(outfile, 'wb') as text_file:
    text_file.write(decode)

#%%
asdf = bytes(decode)
for k in range(len(data)):
    if(asdf[k] != data[k]):
        print(adsf[k])

