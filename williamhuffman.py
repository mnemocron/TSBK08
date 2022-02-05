from cgitb import small
import math
import time

smallfilenames = ["cantrbry/test.txt", "cantrbry/alice29.txt", "cantrbry/asyoulik.txt", "cantrbry/cp.html", "cantrbry/fields.c", "cantrbry/grammar.lsp", "cantrbry/kennedy.xls", "cantrbry/lcet10.txt",
                  "cantrbry/plrabn12.txt", "cantrbry/ptt5", "cantrbry/sum", "cantrbry/xargs.1"]
bigfilenames = ["large/bible.txt", "large/E.coli", "large/world192.txt"]


def create_huffmantree(filename):
    global symbbollist
    # Load bytes from file and count symbol occurances
    with open(filename, "rb") as f:  # 'rb' means read binary
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
    print("Probability of root: ", root.probability)

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
    decoded = ""
    root = huffmantree
    for char in code:
        if root.symbol:
            decoded += chr(int(root.symbol, 2))
            #decoded = root.symbol
            root = huffmantree  # go back to root
        if char == "0":
            root = root.childLeft
        else:
            root = root.childRight

    decoded += chr(int(root.symbol, 2))
    #decoded = root.symbol
    return decoded


def decode_binary_string(s, amount):
    return ''.join(chr(int(s[i*8:i*8+8], 2)) for i in range(amount))


starttime = time.time()

filename = bigfilenames[0]

print("Coding " + filename.split("/")[1] + "!\n")

symbollist = [0]*256  # declare list with length 256 (2^8)

print("Creating huffman tree!")
start = time.time()
huffmantree, symbbollist = create_huffmantree(filename)
end = time.time()
print("\nCreating huffman tree took " + str(end-start) + " seconds!\n")


print("Coding file!")
start = time.time()
code = code_huffman(symbollist, filename)
end = time.time()
print("Coding file took " + str(end-start) + " seconds!\n")
print("Filesize " + str(len(code)/8) + " byte!")


print("Decoding file!")
start = time.time()
decoded = new_decode_huffman(huffmantree, code)
end = time.time()
print("Decoding file took " + str(end-start) + " seconds!\n")

endtime = time.time()
print("Decode and code" + str(filename) + " took: ", end - start, " seconds!")

characters = 100
print("\nFirst " + str(characters) + " characters: "  + decoded[0:characters])
#print("\nFirst " + str(characters) + " characters: "  + decode_binary_string(decoded, 100))
