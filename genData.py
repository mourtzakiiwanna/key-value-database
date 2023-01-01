import string
import sys
import random
import getopt

def main(argv):
    
    opts, _ = getopt.getopt(argv, "hk:n:d:l:m:")

    # checking user input and throw error message if any argyment is missing 
    if len(opts) != 5:
        create_error_message()
        sys.exit()

    # initializing the variables with the values given from the user 
    for opt, arg in opts:
        if opt in ("-k"):
            key_file = arg
        elif opt in ("-n"):
            lines = int(arg)
        elif opt in ("-d"):
            nesting_level = int(arg)
        elif opt in ("-l"):
            max_string_length = int(arg)
        elif opt in ("-m"):
            max_keys = int(arg)

    # reading the 'keyFile.txt', parsing the key names/types and add them on 'keys' list 
    # 'keys' list stores the name and the type of each key [[name,string],[age,int]..]
    file = open(key_file, 'r')
    keys = []
    for i in file.readlines():
        keys.append(i.split())

    # generating random data and store them in 'payload' dict 
    # setting high-level keys as key1, key2..
    payload = {}
    for i in range(1,lines):
        payload['\'key' + str(i)+'\''] = create_payload(keys,nesting_level, max_keys, max_string_length)

    # writing generated data to 'dataToIndex' file
    outputFile = 'dataToIndex.txt'
    f = open(outputFile, "w")
    
    for key in payload:
        f.write(key + " : " + str(payload[key]) + "\n")

    print("\nData was successfully generated.")


# returns an error message when any argument is missing from user's input 
def create_error_message():
    print("\nSome arguments are missing. Please provide the required info in this order: genData.py -k -n -d -l -m , where : \n\n -k is a file containing a space-separated list of key names and their data types, \n -n indicates the number of lines that you would like to generate, \n -d is the maximum level of nesting, \n -m is the maximum number of keys inside each value, \n -l is the maximum length of a string value whenever you need to generate a string")

# returns a random value of specific length based on key type
# exaple: if max_string_length is 4 -> String 'Qvmq', int '6574', float '1202.93'
def create_random_value(max_string_length, type):

    max_length = int(max_string_length)
    min = pow(10, max_length-1)
    max = pow(10, max_length) - 1

    if type == "string":
        random_value = ''.join(random.choice(string.ascii_letters) for _ in range(max_string_length))
    elif type == "int":
        random_value = random.randint(min, max)
    elif type == "float":
        random_value = (round(random.uniform(min,max), 2))

    return str(random_value)

# returns the payload generated for every high-level key (key1,key2..)
def create_payload(keyTypes, nesting, max_keys, max_string_length):

    # this list will store the keys we have already used in order not to use them twice 
    keys_used = []
    
    # randomly choose the max key number for this high-level key 
    inside_keys = random.randint(0, max_keys)
    payload = {}

    # loop up to max key and create payload (using recursion)
    for i in range(0, inside_keys):

        key = random.randint(0, max_keys-1)

        # to be sure that the same key is not appeared twice in the same level 
        if (len(keys_used) != max_keys):
            if key not in keys_used:
                keys_used.append(key)
            else: 
                while key in keys_used:
                    key = random.randint(0, max_keys-1)
        else: 
            continue

        nesting_level = 0
        
        # if the nesting level is not 0, we randomly choose the nesting level we will apply 
        if nesting > 0:
            nesting_level = int(round(random.random()*nesting, 0))

        # if we will apply nest, we recursively call the 'create_payload' reducing every time the nesting level 
        if(nesting_level > 0):
            payload[keyTypes[key][0]] = create_payload(keyTypes, nesting_level - 1, max_keys, max_string_length)
        # else if we won't apply nesting, we just fill in with a random key value based on key type 
        else:
            type = keyTypes[key][1]
            value = create_random_value(max_string_length,type)
            payload[keyTypes[key][0]] = value

    return payload

if __name__ == "__main__":
    main(sys.argv[1:])
