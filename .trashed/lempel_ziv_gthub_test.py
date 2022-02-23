# -*- coding: utf-8 -*-

import lzw

filename = './infiles/cantrbry/alice29.txt'
outfile = 'test.lzw'
decompfile = './alice29.txt'

# Compresses "example file.txt" into "example file.txt.lzw".
with open(filename) as input_file:
    with open(outfile, 'wb') as compressed_file:
        compressed_file.write(lzw.compress(input_file.read()))

# Decompresses and prints "example file.txt.lzw" content.
with open(outfile, 'rb') as compressed_file:
    with open(decompfile, 'wb') as decompressed_file:
        decompressed_file.write(lzw.decompress(compressed_file.read()))
        
    # print(lzw.decompress(compressed_file.read()))
    
#%%
with open(filename) as input_file:
    print(input_file.read())
    