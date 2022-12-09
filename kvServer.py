import sys
import getopt
import socket
import trie
import json
import math

# Returns the error message
def create_error_message():
    print("\nSome arguments are missing. Please provide the required info in this order: kvServer.py -a -p , where : \n\n -a is the IP address of the server, \n -p is the PORT of the server")

# Returns a dictionary with all the key-values (recursively concatenate the keys of the dictionary)
def dict_flatten(kvDict, prefix = None, result={}):

    for key in kvDict:
        if prefix is None:
            prefix_str = (str(key))
        else:
            prefix_str = (prefix, str(key))
            prefix_str = '.'.join(prefix_str)

        if isinstance(kvDict[key],dict):
            dict_flatten(kvDict[key], prefix_str, result)

        if prefix_str not in result:
            result[prefix_str] = kvDict[key]

    return result


def main(argv):
    
    opts, _ = getopt.getopt(argv, "hk:a:p:")

    if len(opts) != 2:
        create_error_message()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-a"):
            ip_address = arg
        elif opt in ("-p"):
            port = int(arg)

    trie_structure = trie.Trie()
    s = socket.socket()
    s.bind((ip_address, port))
    s.listen(5)
    print("The socket is ready..")

    while (True):
        # connection with client socket 
        c, addr = s.accept()
        print('Got connection from: ', addr)

        data_from_client = c.recv(4098)

        if(len(data_from_client) <= 0):
            continue

        data_from_client = data_from_client.decode().split()
        # command can be PUT,GET,QUERY,DELETE,COMPUTE
        command = data_from_client[0]
        # request is the whole part after the command 
        request = data_from_client[1]

        # PUT request
        if command == "PUT":
            # parsing 
            parsing_var = "{" + request + "}"
            parsing_var = parsing_var.replace("'", "\"")
            parsing_var = json.loads(parsing_var)

            print(f"Adding data to the trie_structure:\n{request}\n")

            # in case the high-level key already exists
            temp = str(list(parsing_var.keys())[0])
            if not trie_structure.search(temp)[0]:
                kvDict = dict_flatten(parsing_var)
                for key in kvDict:
                    trie_structure.insert(key, kvDict[key])
                response = "OK"
            else:
                response = "High-level key already exists."

        # GET request
        elif command == "GET":
            if "." in request:
                response = "ERROR - No high-level key specified"
            else:
                result = trie_structure.search(request)
                # if key found
                if result[0]: 
                    response = request + ": " + str(result[1])
                else:
                    response = "Key " + str(request) + " was not found - is not a high-level key.\n"

        # QUERY request
        elif command == "QUERY":
            result = trie_structure.search(request)
            # if key found
            if result[0]:  
                response = request + ": " + str(result[1])
            else:
                response = "Key " + str(request) + " was not found - is not a high-level key.\n"

        # COMPUTE request
        elif command == "COMPUTE":
            result = trie_structure.compute(data_from_client[1],data_from_client[3:])
            # if key/keys found
            if result[0]:
                response = request + ": " + str(result[1])
            else:
                response = "Key " + str(request) + " was not found - is not a key.\n"

        # DELETE request
        elif command == "DELETE":
            result = trie_structure.delete(request)
            if "." in request:
                response = "ERROR - No high-level key specified"
            else:
                # id key is deleted
                if result:  
                    response = request + " has been successfully deleted."
                else:
                    response = "Key " + str(request) + " was not found - is not a key.\n"

        # ELSE
        else:
            response = "ERROR - This command is not available."

        c.send(response.encode())


if __name__ == "__main__":
    main(sys.argv[1:])
