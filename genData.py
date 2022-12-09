import string
import sys
import random
import getopt

# Returns the error message
def createErrorMessage():
    print("\nSome arguments are missing. Please provide the required info in this order: genData.py -k keyFile.txt -n -d -l -m , where : \n\n -k keyFile.txt is a file containing a space-separated list of key names and their data types \n -n indicates the number of lines that you would like to generate \n -d is the maximum level of nesting \n -m is the maximum number of keys inside each value \n -l is the maximum length of a string value whenever you need to generate a string")

# Returns a random value of specific length based on key type
def createRandomValue(max_string_length,type):

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

# Returns the payload generated for every high-level key (key0,key1..)
def createPayload(keyTypes, nesting, max_keys, max_string_length):

    indexes = []
    # randomly choose the max key number for this high-level key 
    rand_max_key = random.randint(0, max_keys)
    payload = {}

    # loop up to max key and create payload 
    for _ in range(0, rand_max_key):

        index = random.randint(0, max_keys-1)

        if index not in indexes:
            indexes.append(index)
        elif (len(indexes) != max_keys):
            while index in indexes:
                index = random.randint(0, max_keys-1)
        else:
            continue

        # if the nesting level is not 0, we randomly choose if we will apply the nest or not 
        if nesting > 0:
            isNesting = random.choice([True, False])

        # if we will apply nest, we recursively call the 'createPayload' reducing every time the nesting level 
        if(nesting > 0 and isNesting):
            payload[keyTypes[index][0]] = createPayload(keyTypes, nesting - 1, max_keys, max_string_length)
        # else if we won't apply nesting, we just fill in with a random key value based on key type 
        else:
            type = keyTypes[index][1]
            value = createRandomValue(max_string_length,type)
            payload[keyTypes[index][0]] = value

    return payload


def main(argv):
    
    opts, _ = getopt.getopt(argv, "hk:n:d:l:m:")

    if len(opts) != 5:
        createErrorMessage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-k"):
            key_file = arg
        elif opt in ("-n"):
            lines = int(arg)
        elif opt in ("-d"):
            nesting_level = int(arg)
        elif opt in ("-m"):
            max_keys = int(arg)
        elif opt in ("-l"):
            max_string_length = int(arg)

    # 'keys' list have the name and the type of each key [[name,string],[age,int]]
    file = open(key_file, 'r')
    keys = []
    for i in file.readlines():
        keys.append(i.split())

    # payload generation
    payload = {}
    for j in range(lines):
        payload['\'key' + str(j)+'\''] = createPayload(keys,nesting_level, max_keys, max_string_length)

    # write generated data to file
    with open("dataToIndex.txt", 'w') as f:
        for d in payload:
            f.write(d + "-> " + str(payload[d]))
            f.write('\n')
    
    """

    with open("dataToIndex.txt", 'r') as f:
        
        filedata = f.read()

    filedata = filedata.replace(':','->')
    filedata = filedata.replace(',','|')

    with open("dataToIndex.txt", 'w') as f:
        f.write(filedata)

    """

if __name__ == "__main__":
    main(sys.argv[1:])