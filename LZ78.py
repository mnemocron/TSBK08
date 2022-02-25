
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

    data_byte = data[index] # current byte from data to code

    longest_match = 0 # variable to remember the longest match
    longest_match_index = 0 # variable to remember the index of longest match

    # look if data_byta already exists in list
    for i in range(len(list)):

        # list_byte must be the deepest down in the list when comparing
        # Ex: (0,a),(0,b),(1,a) which is abba
        # but when reading list[2][1] is will give "a" but list[2][1] is actually ba
        list_byte = None
        j = i
        while(list[j][1] != None):
            j = list[j][0]
        
        list_byte = list[j][1] # first byte of byte chain in list

        if(list_byte == data_byte):
            ### Match!!!

            # Need to look at the deepest byte ex: (1,b) need to look at byte at 1 before b and so on until None is the byte

            # add first match to start of byte_chain
            byte_chain = []
            byte_chain.insert(0,(i,data_byte))

            # gets the whole byte chain from the element in list
            k = list[i][0]
            deeper_byte = list[k][1]

            current_longest_match_index = 0 # reference to (0, None)

            while deeper_byte != None:
                byte_chain.insert(0,(k,deeper_byte)) # need to store index for later use
                k = list[k][0]
                deeper_byte = list[k][1]
            
            # byte_chain is now a list with the whole byte chain stored in list ex: [a,b,b,a,a]
            print("Byte chain: ", byte_chain)

            # Now we need to calculate how long the match is for this element in the list with the data
            currentmatch = 0
            for i in range(len(byte_chain)):
                if byte_chain[i][1] == data[index+i]:
                    currentmatch += 1
                    longest_match_index = byte_chain[i][0]

            if currentmatch > longest_match:
                longest_match = currentmatch
            
            print("Byte chain from list: ", byte_chain)

        # no match => compare with next symbol in list
    
    # More than one symbol already exists in list
    if longest_match > 0:
        list.append((longest_match_index, data[index + longest_match]))
        index += 1 + longest_match
    else:
        # Symbol does not exist in list => add new symbol
        list.append((0, data[index]))
        match_length = 1 # restore match_length
        index += 1 # code next byte in data

print("Code:\n", list)
