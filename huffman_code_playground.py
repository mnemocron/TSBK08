# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 08:30:20 2022

@author: simon



a = 0    0
b = 10   2
c = 110  6
d = 111  7

"""

import numpy as np

original = 'aabacabadabaabacacaba'
filename = './infiles/abcd.txt'
with open(filename, 'rb') as f:
    data = np.fromfile(f, np.dtype('B'))

tree_enc = np.zeros([256], dtype=np.uint8) * np.NaN
tree_dec = np.zeros([256], dtype=np.uint8) * np.NaN

tree_enc[ord('a')] = 0
tree_enc[ord('b')] = 2
tree_enc[ord('c')] = 6
tree_enc[ord('d')] = 7

tree_dec[0] = ord('a')
tree_dec[2] = ord('b')
tree_dec[6] = ord('c')
tree_dec[7] = ord('d')

# COMPRESS
compressed = np.array([], dtype=np.uint8)
for sym in data:
    cw = np.unpackbits(tree_enc[sym].astype(np.uint8))
    cw_short = np.array([], dtype=np.uint8)
    for bit in cw:
        if bit == 1:
            cw_short = np.append(cw_short,1)
    if(len(cw_short) < 3):
        cw_short = np.append(cw_short,0)
    compressed = np.append(compressed, cw_short)

# DECOMPRESS
decompressed = ''
tmp = np.array([],dtype=np.uint8)
for bit in compressed:
    tmp = np.append(tmp, bit)
    if (bit == 0) or (len(tmp) == 3):
        # decode
        tmp = np.pad(tmp, (8-len(tmp), 0))
        sym =  chr( tree_dec[ np.packbits(tmp, bitorder='big') ][0].astype(np.uint8) )
        decompressed = decompressed + sym
        tmp = np.array([],dtype=np.uint8) # clear

print(original)
print(decompressed)



