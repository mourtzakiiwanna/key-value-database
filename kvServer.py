import sys
import getopt
import socket
import trie
import json

def main(argv):

    # checking user input and throw error message if any argyment is missing 
    try:
        opts, _ = getopt.getopt(argv, "hk:a:p:")
    except getopt.GetoptError:
        create_error_message()
        sys.exit(2)

    if len(opts) != 2:
        create_error_message()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-a"):
            ip_address = arg
        elif opt in ("-p"):
            port = int(arg)

    # creating a Trie object 
    trie_structure = trie.Trie()
    s = socket.socket()
    print("\nSocket successfully created!")
    s.bind((ip_address, port))
    # allowing oup to 5 connections 
    s.listen(5)
    print("The socket is waiting..\n")

    while (True):
        
        # connecting with the client
        c, addr = s.accept()

        data_from_client = c.recv(4098)

        # if the data sent from the client is empty 
        if(len(data_from_client) <= 0):
            continue

        print('Got connection from: ', addr)
        data_from_client = data_from_client.decode().split()
        # command can be PUT,GET,QUERY,DELETE,COMPUTE
        command = data_from_client[0]

        # if user input is just command (e.g. GET) without key specified 
        if (len(data_from_client) > 1):
            # request is the whole part after the command 
            request = data_from_client[1]
        else: 
            response = "This command is not available."

        # PUT request
        if command == "PUT":
            # parsing 
            parsing_var = "{" + request + "}"
            parsing_var = parsing_var.replace("'", "\"")
            parsing_var = json.loads(parsing_var)

            print(f"Adding data to the Trie:\n{request}\n")

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
        elif (command == "GET" or command == "get"):
            if "." in request:
                response = "No high-level key specified."
            else:
                result = trie_structure.search(request)
                # if key found
                if result[0]: 
                    response = request + ": " + str(result[1])
                else:
                    response = "Key '" + str(request) + "' was not found - is not a high-level key.\n"

        # QUERY request
        elif (command == "QUERY" or command == "query"):
            result = trie_structure.search(request)
            # if key found
            if result[0]:  
                response = request + ": " + str(result[1])
            else:
                response = "Key '" + str(request) + "' was not found - is not a key.\n"

        # COMPUTE request
        elif (command == "COMPUTE" or command == "compute"):
            result = trie_structure.compute(data_from_client[1],data_from_client[3:])
            # if key/keys found
            if result[0]:
                response = request + ": " + str(result[1])
            else:
                response = "Key '" + str(request) + "' was not found - is not a key.\n"

        # DELETE request
        elif (command == "DELETE" or command == "delete"):
            if "." in request:
                response = "No high-level key specified."
            else:
                result = trie_structure.delete(request)
                # id key is deleted
                if result:  
                    response = request + " has been successfully deleted."
                else:
                    response = "Key '" + str(request) + "' was not found - is not a key.\n"
        # ELSE
        else:
            response = "This request is not available.\n Supported requests: GET, QUERY, COMPUTE, DELETE, EXIT."

        # sending the response to the client
        c.send(response.encode())

# returning the error message
def create_error_message():
    print("\nSome arguments are missing. Please provide the required info in this order: kvServer.py -a -p , where : \n\n -a is the IP address of the server, \n -p is the PORT of the server")

# returning a dictionary with all the key-values (recursively concatenate the keys of the dictionary)
def dict_flatten(initialDict, prefix = None, finalDict={}):

    for key in initialDict:
        if prefix is None:
            prefix_str = (str(key))
        else:
            prefix_str = (prefix, str(key))
            prefix_str = '.'.join(prefix_str)

        if isinstance(initialDict[key],dict):
            dict_flatten(initialDict[key], prefix_str, finalDict)

        if prefix_str not in finalDict:
            finalDict[prefix_str] = initialDict[key]

    return finalDict

if __name__ == "__main__":
    main(sys.argv[1:])


