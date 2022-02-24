
filename = ["cantrbry/test.txt"]


def read_file(filename):
    # Load bytes from file and count symbol occurances
    with open(filename, "rb") as f:  # 'rb' means read binary
        data = f.read()
        return data


data = read_file(filename[0])

datasize = len(data)

list = [(None, 0)]
index = 0   # index for data
nextsymbol = False
symbol_match_index = 0 #empty symbol
run = True

number_of_bytes_in_data_to_compare_with = 1 # symbol chain from data
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

    print("byte to code: ", data[index])

    # look if symbol already exists until a symbol
    # that doesen't already exists is found
    for i in range(len(list)): # look through whole lists

        # How many bytes to compare with
        j = i
        compare_byte = list[j][1]
        for nr_bytes in range(number_of_bytes_in_data_to_compare_with):
            if(data[index+nr_bytes] != compare_byte):
                # no match => next step in list
                break

            # match => look deeper
            j = list[j][0] # index of byte in list

            # if j is 0 or None then that is the end of symbol chain
            if j == 0 or j == None:
                list.append()

            compare_byte = list[j][1] # iterate deeper in element in list
            print("look depper")
        
    # Symbol does not exist in list => add new symbol
    list.append((0, data[index]))
    index += 1 # code next byte in data

print("Code:\n", list)
