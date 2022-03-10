import time


filenames = ["compressed.txt"]

def read_file(filename):
    # Load bytes from file and count symbol occurances
    with open(filename, "rb") as f:  # 'rb' means read binary
        data = f.read()
        return data

def LZ78_decoder(filename):

    #code = read_file(filename)
    code = [(0,None),(0,"a"),(0,"b"),(1,"b"),(3,"c"),(4,"d")]
    decoded = []

    for index_symbol in code:
        if index_symbol[0] == 0:
            if index_symbol[1]: # not False or None
                decoded.append(index_symbol[1])
        else:
            index = 0
            symbols = [index_symbol[1]]
            next_index_symbol = code[index_symbol[0]]
            while next_index_symbol[0] != 0:
                symbols.insert(0, next_index_symbol[1])
                next_index_symbol = code[next_index_symbol[0]]
            symbols.insert(0, next_index_symbol[1])

            # add symbols to decoded
            for symbol in symbols:
                decoded.append(symbol)
    
    print("decoded: ", decoded)


tic = time.time()
LZ78_decoder("filename")
tec = time.time()

print("Decoding took ", tec-tic, " seconds")
