# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 17:38:19 2022

@author: simon
"""

import os
import math

filename = './infiles/cantrbry/alice29.txt'
cnt = 0
alphabet = {}
k = 2

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

print(cnt)
print(H)

