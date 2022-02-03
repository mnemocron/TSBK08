#!/bin/bash

ORIGINAL="./infiles/cantrbry/alice29.txt"
ZIPPED="./tests/alice29.zop"
UNZIPPED="./tests/alice29.txt"

echo -e "\n---- COMPRESS ----"
time python3 encode_huffman.py $ORIGINAL $ZIPPED
echo -e "\n--- DECOMPRESS ---"
time python3 decode_huffman.py $ZIPPED $UNZIPPED
cmp --silent $ORIGINAL $UNZIPPED && echo '### SUCCESS: Files Are Identical! ###' || echo '### WARNING: Files Are Different! ###'

ORIGINAL="./infiles/cantrbry/ptt5"
ZIPPED="./tests/ptt5.zop"
UNZIPPED="./tests/ptt5"

echo -e "\n---- COMPRESS ----"
time python3 encode_huffman.py $ORIGINAL $ZIPPED
echo -e "\n--- DECOMPRESS ---"
time python3 decode_huffman.py $ZIPPED $UNZIPPED
cmp --silent $ORIGINAL $UNZIPPED && echo '### SUCCESS: Files Are Identical! ###' || echo '### WARNING: Files Are Different! ###'

rm ./tests/*

# python3 entropy.py ./infiles/cantrbry/alice29.txt
# python3 entropy.py ./infiles/cantrbry/asyoulik.txt
# python3 entropy.py ./infiles/cantrbry/cp.html
# python3 entropy.py ./infiles/cantrbry/fields.c
# python3 entropy.py ./infiles/cantrbry/grammar.lsp
# python3 entropy.py ./infiles/cantrbry/kennedy.xls
# python3 entropy.py ./infiles/cantrbry/lcet10.txt
# python3 entropy.py ./infiles/cantrbry/plrabn12.txt
# python3 entropy.py ./infiles/cantrbry/ptt5
# python3 entropy.py ./infiles/cantrbry/sum
# python3 entropy.py ./infiles/cantrbry/xargs.1
# 
# python3 entropy.py ./infiles/large/E.coli
# python3 entropy.py ./infiles/large/bible.txt
# python3 entropy.py ./infiles/large/world192.txt
