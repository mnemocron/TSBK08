# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 11:32:29 2022

@author: simon
"""

from base64 import decode
from symtable import Symbol
import time
import hashlib
from operator import itemgetter
import os
import math

from LZ78Coder import LZ78_file


smallfilenames = ["cantrbry/alice29.txt", "cantrbry/asyoulik.txt", "cantrbry/cp.html", "cantrbry/fields.c", "cantrbry/grammar.lsp", "cantrbry/kennedy.xls", "cantrbry/lcet10.txt",
                  "cantrbry/plrabn12.txt", "cantrbry/ptt5", "cantrbry/sum", "cantrbry/xargs.1"]
bigfilenames = ["large/bible.txt", "large/E.coli", "large/world192.txt"]

def read_file(filename):
    # Load bytes from file and count symbol occurances
    with open(filename, "rb") as f:  # 'rb' means read binary
        data = f.read()
        return data

def LZ78_decoder(filename, code):
    decoded = []
    i = 0
    while i <= len(code)-1:
        index_symbol = code[i]
        if index_symbol[0] == 0:
            if index_symbol[1]:  # not False or None
                decoded.append(index_symbol[1])
                i += 1
            elif index_symbol[1] == None:  
                i += 1
            elif index_symbol[1] == False:   # clear code and start over
                code = code[i+1:]
                i = 0
                print(f'dec {filename} @ {len(decoded)}')

        else:
            symbols = [index_symbol[1]]
            next_index_symbol = code[index_symbol[0]]
            while next_index_symbol[0] != 0:
                #symbols.insert(0, next_index_symbol[1])
                symbols.append(next_index_symbol[1])
                next_index_symbol = code[next_index_symbol[0]]
            #symbols.insert(0, next_index_symbol[1])
            symbols.append(next_index_symbol[1])

            symbols.reverse()   # more efficient than repeatedly using symbols.insert()
            # add symbols to decoded
            #for symbol in symbols:
            #    decoded.append(symbol)
            decoded.extend(symbols)

            i += 1

    return decoded

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

### COMPRESS USING LZ78 #######################################################
outfile = './temp.lz78'
decompfile = './decomp.dat'

files = smallfilenames + bigfilenames
# files = smallfilenames[0:1]
# files = smallfilenames[0:1]

for filename in files:
    #filename = smallfilenames[1]
    #filename = "cantrbry/ptt5"
    # print(f"Compress file: {filename.split('/')[1]} --> {outfile}", end='')
    metric_file = filename.split('/')[1]
    tic = time.time()
    list = [(0, None)]
    code = LZ78_file(filename, list)
    toc = time.time()
    metric_time_encode = toc-tic
    ### DECOMPRESS THE FILE #######################################################
    tic = time.time()
    decoded = LZ78_decoder(filename, code)
    decoded = bytes(decoded)
    with open(decompfile, 'wb') as f:
        f.write(decoded)
    toc = time.time()
    metric_time_decode = toc-tic
    
    # theoretical output file size 
    # = 6 bits for match length + 8 bits for next symbol
    maxdepth = max(code,key=itemgetter(0))[0]
    dict_bits = math.ceil(math.log2(maxdepth))
    outfilesize = (dict_bits + 8) * len(code) / 8
    metric_ratio = outfilesize/os.path.getsize(filename)
    print(dict_bits)
        
    metric_md5ok = 0
    hash_original = md5(filename)
    hash_decomp   = md5(decompfile)
    if(hash_original == hash_decomp):
        #print(f"md5 match: {hash_original}")
        metric_md5ok = 1
    print(f'{metric_file}\t{metric_ratio:.2}\t{metric_time_encode:.3}\t{metric_time_decode:.3}\t{metric_md5ok}')




