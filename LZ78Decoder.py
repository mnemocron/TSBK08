from base64 import decode
from symtable import Symbol
import time

from LZ78Coder import LZ78_file


def read_file(filename):
    # Load bytes from file and count symbol occurances
    with open(filename, "rb") as f:  # 'rb' means read binary
        data = f.read()
        return data


def LZ78_decoder(filename):

    #code = read_file(filename)
    code = [(0, None), (0, "a"), (0, "b"), (1, "b"), (3, "c"), (4, "d"),
            (0, False), (0, None), (0, "a"), (0, "b"), (1, "b"), (3, "c"), (4, "d")]
    decoded = []

    code = filename

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
            else:
                raise Exception("Should not be able to be here!")

        else:
            symbols = [index_symbol[1]]
            next_index_symbol = code[index_symbol[0]]
            while next_index_symbol[0] != 0:
                symbols.insert(0, next_index_symbol[1])
                next_index_symbol = code[next_index_symbol[0]]
            symbols.insert(0, next_index_symbol[1])

            # add symbols to decoded
            for symbol in symbols:
                decoded.append(symbol)

            i += 1

    return decoded


filename = "cantrbry/alice29.txt" #"cantrbry/test.txt"
#filename = "test.txt"

start = time.time()

list = [(0, None)]
code = LZ78_file(filename, list)

end = time.time()


print(code[15:25], "\n")
print("Coding ", filename, " took ", end-start, " seconds!\n")

tic = time.time()
decoded = LZ78_decoder(code)
tec = time.time()

decoded = bytes(decoded)
orig = read_file(filename)

#%%
for i in range(0,200):
    print(chr(decoded[i]), end="")

print("\nDecoding took ", tec-tic, " seconds")
