import time

from numpy import short

filenames = ["cantrbry/test.txt"] #, "cantrbry/fields.c", "cantrbry/sum"]

shortfilenames = ["cantrbry/alice29.txt", "cantrbry/asyoulik.txt", "cantrbry/cp.html", "cantrbry/fields.c", "cantrbry/grammar.lsp", "cantrbry/kennedy.xls", "cantrbry/lcet10.txt",
                  "cantrbry/plrabn12.txt", "cantrbry/ptt5", "cantrbry/sum", "cantrbry/xargs.1"]
bigfilenames = ["large/bible.txt", "large/E.coli", "large/world192.txt"]

def read_file(filename):
    # Load bytes from file and count symbol occurances
    with open(filename, "rb") as f:  # 'rb' means read binary
        data = f.read()
        return data

def get_byte_sequence_from_element_in_list(i, list):
    # returns a list of the sequence that an index in list refers to
    byte_chain = []
    while list[list[i][0]][1] != None:
        byte_chain.insert(0,(i,list[i][1]))
        i = list[i][0]
    
    byte_chain.insert(0,(i,list[i][1]))
    
    #print("byte_chain: ", byte_chain)
    return byte_chain



def get_first_symbol_from_element_in_list(i, list):
    # returns the first symbol that an element in list refers to
    while(list[i][1] != None):
        if list[list[i][0]][1] == None: # get byte before None byte
            return list[i][1] # first byte of byte chain in list
        i = list[i][0]
    
    return list[i][1]


def LZ78_file(filename, list):
    # Example:
    # a b a d a b a c b a c b a c
    # (0, None), (0,a), (0,b), (1,d), (1,b), (1,c), (2,a), (0,c), (6,c)

    # It is easy when implementing to code one symbol at a time
    # harder when you need to compare multiple symbols in data with multiple symbols in list
    # because every element in the list only contains one symbol and a reference to another one.
    # That is what I try to do down here

    data = read_file(filename)
    datasize = len(data)
    index = 0   # indexing for bytes in data
    code = []
    print("Coding: ", filename, " with ", datasize, " bytes!\n")

    while True:

        if index > datasize-1:
            break

        data_byte = data[index] # current byte from data to code

        longest_match = 0 # variable to remember the longest match
        longest_match_index = 0 # variable to remember the index of longest match

        # look if data_byta already exists in list and find the longest match
        for i in range(len(list)):

            # list_byte must be the deepest down in the list when comparing
            # Ex: (0,a),(0,b),(1,a) which is abba
            # but when reading list[2][1] is will give "a" but list[2][1] is actually ba
            
            list_byte = get_first_symbol_from_element_in_list(i, list)

            if(list_byte == data_byte):
                ### Match!!!

                # Need to look at the deepest byte ex: (1,b) need to look at byte at 1 before b and so on until None is the byte

                # add first match to start of byte_chain
                byte_chain = get_byte_sequence_from_element_in_list(i, list)

                # Calculate how many bytes in data that match with list
                currentmatch_length = 0
                currentmatch_index = 0

                for j in range(len(byte_chain)):
                    if index + j < datasize - 1:
                        if byte_chain[j][1] == data[index+j]:
                            currentmatch_length += 1
                            currentmatch_index = byte_chain[j][0]
                        else:
                            break
                    else:
                        break # do not code more bytes than in data
                
                #print("matchlength: ", currentmatch_length, " index: ", currentmatch_index)

                if currentmatch_length > longest_match:
                    longest_match = currentmatch_length
                    longest_match_index = currentmatch_index
                
            # no match => compare with next symbol in list
        
        # More than one symbol already exists in list
        if longest_match > 0:
            list.append((longest_match_index, data[index + longest_match]))
            index += longest_match + 1
            
            #print("list: ", list)
        else:
            # Symbol does not exist in list => add new symbol
            list.append((0, data[index]))
            index += 1 # code next byte in data
        
        # check if list is too long then start over
        
        if len(list) > 1000:
            code += list
            code += [(0,False)]
            list = [(0,None)]
    
    code += list
    return code


if __name__ == "__main__":

    tic = time.time()
    filenames = ["test.txt"]

    for filename in filenames:
        list = [(0, None)]
        start = time.time()
        code = LZ78_file(filename, list)
        #print("Code", code, "length: ",len(code))
        end = time.time()
        print("Coding ", filename, " took ", end-start, " seconds!\n")
        print("Code: ", code)

    tac = time.time()

    print("Total time: ", tac-tic, " seconds!")