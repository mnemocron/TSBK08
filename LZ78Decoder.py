from doctest import FAIL_FAST
from logging import raiseExceptions
import time


filenames = ["compressed.txt"]


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

    print("decoded: ", decoded)


tic = time.time()
LZ78_decoder("filename")
tec = time.time()

print("Decoding took ", tec-tic, " seconds")
