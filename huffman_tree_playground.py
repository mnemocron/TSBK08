# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 13:43:17 2022

@author: simon
"""

import numpy as np

original = 'aabacabadabaabacacaba'
filename = './infiles/abcd.txt'
filename = './infiles/cantrbry/alice29.txt'
with open(filename, 'rb') as f:
    data = np.fromfile(f, np.dtype('B'))

p = np.zeros([256, 1])
for e in data:
    p[e] += 1
p = p/len(data) # probabilities

H = 0
for pp in p:
    if pp>0:
        H += pp * np.log2(pp)
H = -H
lmax = np.ceil(H+1)[0]
print(f'maximum codeword length: {lmax}')

syms = [i for i, x in enumerate(p) if x>0]
N = len(syms)

arr = np.array( [[b[0],i] for i,b in enumerate(p) if b>0])
arr = arr[ np.argsort(arr[:,0]) ]

#%% 
# todo: construct tree from probabilities

#%%
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



