from cgitb import small
import math
import time
import hashlib
import numpy as np
import os
import pickle

smallfilenames = ["cantrbry/alice29.txt", "cantrbry/asyoulik.txt", "cantrbry/cp.html", "cantrbry/fields.c", "cantrbry/grammar.lsp", "cantrbry/kennedy.xls", "cantrbry/lcet10.txt",
                  "cantrbry/plrabn12.txt", "cantrbry/ptt5", "cantrbry/sum", "cantrbry/xargs.1"]
bigfilenames = ["large/bible.txt", "large/E.coli", "large/world192.txt"]

def create_huffmantree(filename):
    global symbbollist
    # Load bytes from file and count symbol occurances
    with open(filename, "rb") as f:  # 'rb' = read binary
        while (byte := f.read(1)):
            # Append each byte to a list
            value = int.from_bytes(byte, "big")
            symbollist[value] += 1

    # Calculate probability for each symbol

    # Total symbols in file
    l = 0
    for i in symbollist:
        l += i

    # New list with only symbols that appear and their probability and change symbollist to Leaf class
    symbol_prob_list = []
    for i in range(len(symbollist)):
        if(symbollist[i] != 0):
            # symbol, probability, format converts int to binary with byte length
            symbol_prob_list.append(Leaf(format(i, "008b"), symbollist[i]/l))
            # replace symbol list with Leaf classes
            symbollist[i] = Leaf(format(i, "008b"), symbollist[i]/l)

    # Sort probability list

    def probability(node):
        return node.probability

    # Prepare to create huffman tree
    # Sort list of probabilities
    symbol_prob_list.sort(key=probability)

    # Create huffman tree

    while len(symbol_prob_list) > 1:

        # Take two symbols with least probability (beginning of list because sorted)
        symbol_low_prob = symbol_prob_list[0]
        del symbol_prob_list[0]
        # first element will be replaced to not have to delete and append new element
        symbol_high_prob = symbol_prob_list[0]

        # Add node to tree with combined probabilities of either node/leaf
        symbol_prob_list[0] = Node(symbol_high_prob, symbol_low_prob, symbol_high_prob.probability +
                                   symbol_low_prob.probability)  # create node with combined probabilities

        # Sort nodelist
        symbol_prob_list.sort(key=probability)

    root = symbol_prob_list[0]

    # Huffmantree, probability of root should be one
    # print("Probability of root: ", root.probability)

    # Save codewords in every leaf and in list of leaves
    root.set_leaf_code()

    return root, symbollist


class Node:
    # Does not need to know parent
    symbol = False

    def __init__(self, childLeft, childRight, probability):
        # Set children
        self.childLeft = childLeft
        self.childRight = childRight
        self.probability = probability

    def get_symbol(self):
        global code
        if code[0] == "0":
            code = code[1::]
            return self.childLeft.get_symbol()  # remove first 0 from code
        else:
            code = code[1::]
            return self.childRight.get_symbol()  # remove first 1 from code

    def set_leaf_code(self, code=""):
        self.childLeft.set_leaf_code(code + "0")
        self.childRight.set_leaf_code(code + "1")


class Leaf:
    # Does not need to know parent
    code = None

    def __init__(self, symbol, probability):
        self.symbol = symbol  # Binary string
        self.probability = probability  # Int

    def get_symbol(self):
        return self.symbol

    def set_leaf_code(self, code):
        global symbollist
        self.code = code  # Set code for Leaf
        # Set code in list with Leaves
        symbollist[int(self.symbol, 2)].code = self.code


def code_huffman(symbollist, filename):
    code = ""
    with open(filename, "rb") as f:  # 'rb' means read binary
        while (byte := f.read(1)):
            # Append each byte to code string
            i = int.from_bytes(byte, "big")
            code += symbollist[i].code
    return code


def decode_huffman(huffmantree):
    decoded = ""
    global code
    while code:
        symbol = huffmantree.get_symbol()
        decoded += symbol
    return decoded


def new_decode_huffman(huffmantree, code):
    decoded = np.array([], dtype=np.uint8)
    root = huffmantree
    for char in code:
        if root.symbol:
            decoded = np.append(decoded, np.uint8(int(root.symbol, 2)) )
            #decoded += chr(int(root.symbol, 2))
            #decoded = root.symbol
            root = huffmantree  # go back to root
        if char == "0":
            root = root.childLeft
        else:
            root = root.childRight

    decoded = np.append(decoded, np.uint8(root.symbol) )
    #decoded += chr(int(root.symbol, 2))
    #decoded = root.symbol
    return decoded


def decode_binary_string(s, amount):
    return ''.join(chr(int(s[i*8:i*8+8], 2)) for i in range(amount))

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

outfile = './temp.huf'
decompfile = './decomp.dat'
filename = smallfilenames[0]
filename = "cantrbry/ptt5"
print(f"Compress file: {filename.split('/')[1]} --> {outfile}", end='')

symbollist = [0]*256  # declare list with length 256 (2^8)

# print("Creating huffman tree!")
tic = time.time()
huffmantree, symbbollist = create_huffmantree(filename)
code = code_huffman(symbollist, filename)
# write to file
N = os.path.getsize(filename) # length of original data (bytes)
L = len(code)                 # length of encoded data (bits)

while len(code)%8 != 0:
    code += '0'  # padding with zeros to make the length a multiple of 8
# convert bits from string to bytes (uint8)
binar = np.zeros([np.ceil(L/8).astype(np.uint32), 1], dtype=np.uint8)
for i in range(len(binar)):
    ff = code[0+i*8 : 8+i*8]
    mybyte = 0
    for j in range(8):
        if ff[7-j] == '1':
            mybyte += pow(2,j)
    binar[i] = mybyte

dumpster = {} # create new object to then dump to a binary pickle file
dumpster['tree'] = huffmantree
dumpster['bin'] = binar
dumpster['L'] = L
dumpster['N'] = N
# pickle is easy and convenient but has some overhead
pickle.dump(dumpster, open( outfile, 'wb' ))

toc = time.time()
print(f" in {(toc-tic):.3} seconds!")
#print(f"Filesize {(len(code)/8)} bytes!")
print(f"Ratio: {os.path.getsize(outfile)/os.path.getsize(filename):.4}")

print(f"Decompress file: {outfile} --> {decompfile}", end= '')
tic = time.time()
dumpster = pickle.load(open( outfile, 'rb' ))
binar = dumpster["bin"]
# inflate binary back into string of 1 and 0
code = ''
for byte in binar:
    bb = np.unpackbits(byte)
    for b in bb:
        code += str(b)
huffmantree = dumpster["tree"]
L = dumpster["L"]
N = dumpster["N"]
code = code[0:L]
decoded = new_decode_huffman(huffmantree, code)
toc = time.time()
# there is some issue with the length when decoding binary files
# 1 byte too much is already wrong. truncate to the expected length N

decoded = decoded[0:N]  
with open(decompfile, 'wb') as f:
    f.write(decoded)
print(f" in {(toc-tic):.3} seconds!")

hash_original = md5(filename)
hash_decomp   = md5(decompfile)
if(hash_original == hash_decomp):
    print(f"md5 match: {hash_original}")
else:
    print(f"md5 hashes do not match: {hash_original} vs. {hash_decomp}")

#characters = 100
#print(f"First {characters} characters: "  + decoded[0:characters])
#print("\nFirst " + str(characters) + " characters: "  + decode_binary_string(decoded, 100))
