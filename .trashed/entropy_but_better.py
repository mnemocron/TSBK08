# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 14:32:35 2022

@author: simon
"""

import numpy as np

filename = './infiles/cantrbry/xargs.1' # default for debuging
filename = './infiles/large/bible.txt'
k = 0
with open(filename, 'rb') as f:
    data = np.fromfile(f, np.dtype('B'))
    
cnt = np.zeros([pow(256,k+1), 1])
for i in range(len(data)-k-1):
    dd = data[i+k]
    for kk in range(k):
        dd += data[i+k-kk-1] * pow(256,kk+1)
    cnt[dd] += 1
cnt /= len(data)
H = 0
for p in cnt:
    if p>0:
        H += p * np.log2(p)
print(-H)

#%%
data = [1,2,3,4,5,6,7,8,9]
k = 2
cnt = np.zeros([pow(256,k+1), 1])
for i in range(len(data)-k-1):
    dd = data[i+k]
    for kk in range(k):
        dd += data[i+k-kk-1] * pow(256,kk+1)
    cnt[dd] += 1
    

#%%
if(k==0):
    p = np.zeros([256, 1])
if(k==1):
    p = np.zeros([256, 256])
if(k==2):
    p = np.zeros([256, 256, 256])
for i in range(len(data)-k):
    if(k==0):
        p[data[i]] += 1
    if(k==1):
        p[data[i]][data[i+1]] += 1
    if(k==2):
        p[data[i]][data[i+1]][data[i+2]] += 1
    if(k==3):
        p[data[i]][data[i+1]][data[i+2]][data[i+4]] += 1

p = p/len(data)
H = 0

if(k==0):
    for pp in p:
        if pp>0:
            H += pp * np.log2(pp)
if(k==1):
    for pp in p:
        for ppp in pp:
            if ppp>0:
                H += pp * np.log2(pp)
if(k==2):
     for pp in p:
         for ppp in pp:
             for pppp in ppp:
                 if pppp>0:
                     H += pp * np.log2(pp)           
H = -H[0]
print(H)


    