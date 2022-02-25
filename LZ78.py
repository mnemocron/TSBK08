
filename = ["cantrbry/test.txt"]


def read_file(filename):
    # Load bytes from file and count symbol occurances
    with open(filename, "rb") as f:  # 'rb' means read binary
        data = f.read()
        return data


data = read_file(filename[0])

datasize = len(data)

list = [(0, None)]
index = 0   # index for data
nextsymbol = False
symbol_match_index = 0 #empty symbol
run = True

match_length = 1 # symbol chain from data
data_to_compare_with = 0 # how many bytes in data to compare with list


print("Coding: ", filename, " with ", datasize, " bytes!\n")

# Example:
# a b a d a b a c b a c b a c
# (0, None), (0,a), (0,b), (1,d), (1,b), (1,c), (2,a), (0,c), (6,c)

# It is easy when implementing to code one symbol at a time
# harder when you need to compare multiple symbols in data with multiple symbols in list
# because every element in the list only contains one symbol and a reference to another one.
# That is what I try to do down here

while run:
    if(index +1 > datasize): # done?
        # code the last symbol
        list.append((symbol_match_index, data[index-1]))
        print("added new symbol: ", (symbol_match_index, data[index-1]), "\n")
        break
    print("Coding byte ", index, " , with data: ", data[index], "\n")


    ### Actual coding and looking for symbols in list starts here

    # look if symbol already exists until the longest match_length + new symbol is found
    for i in range(len(list)): # look through whole lists

        # What bytes to compare with and how many symbols the match should be (first time match_length=1)
        # match_lenth gets longer as longer matches are found
        list_byte = list[i][1]
        for nr_bytes in range(match_length):
            
            data_byte = data[index+nr_bytes] # step through data to find longer matches

            if(list_byte != data_byte):
                # no match => compare with next symbol in list
                break

            # match found => look deeper
            while list_byte != None:
                # match found => look deeper, need to look for longer matches
                j = list[i][0] # index the mathed byte's pointed byte
                list_byte = list[j][1] # set list_byte to byte pointed to

                # Now we need to see if list_byte match with the next byte in data
            
            
            match_length += 1

            if(list_byte == None): # there is nothing deeper down
                # Here! One match has been found but that match has nothing deeper down
                # Some other elements in list might get more matches
                # But if this is the best longest match then add a new symbol with latest byte
                # and add reference to the longest match and update index accordingly.

                # write that code

                break

            # Here one match is found but we need to look if there are longer matches
            match_length += 1
            print("look depper")
            
    # Symbol does not exist in list => add new symbol
    list.append((0, data[index]))
    match_length = 1 # restore match_length
    index += 1 # code next byte in data

print("Code:\n", list)
