
filename = ["cantrbry/test.txt"]

def read_file(filename):
    # Load bytes from file and count symbol occurances
    with open(filename, "rb") as f:  # 'rb' means read binary
        data = f.read()
        return data

data = read_file(filename[0])

list = [(None,0)]
index = 0
new_symbol = False
run = True

def get_symbol(tuple):
    return tuple[0]

while run:
    print(data[index])

    try:
        # look if symbol already exists until a symbol
        # that doesen't already exists is found
        for i in range(len(list)):
            if data[index] == list[i][1]: # byte in list == byte
                # symbol exists in list
                print("symbol exist in list")
                symbol_match_index = i

                index += 1
                newloop = True
                break
        
        if not newloop: # Symbol does not exist
            list.append((symbol_match_index, data[index]))
            newloop = False
    except:
        break

print(list)
