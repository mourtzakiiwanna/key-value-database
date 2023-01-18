import sys
import getopt
import socket
import errno
import random

def main(argv):
  
    # checking user input and throw error message if any argyment is missing 
    try:
        opts, _ = getopt.getopt(argv, "hk:s:i:k:")
    except getopt.GetoptError:
        create_error_message()
        sys.exit(2)

    if len(opts) != 3:
        create_error_message()
        sys.exit(2)

    # initializing the variables with the values given from the user 
    for opt, arg in opts:
        if opt in ("-s"):
            serverfile = arg
        elif opt in ("-i"):
            dataToIndex = arg
        elif opt in ("-k"):
            k = int(arg)

    # reading the file with the servers' info 
    servers = []
    with open(serverfile) as f:
        for line in f:
            servers.append(line.split())
    
    # checking if the servers provided are less than the 'k' number. If so, the program must exit.
    if(len(servers) < k):
        print("\nThe 'k' number (replication factor) must be bigger or equal to the amount of servers provided in the file.")
        sys.exit()

    # reading the ouput file from the first part of the project 
    with open(dataToIndex) as f:
        output_data = [line.rstrip(" \\\n").replace(" ", "") for line in f]

    print("\nIndexing of servers has just started...\n")
    print("====================================")

    # looping through every line of the file with the output data 
    for i in output_data:
        
        # choosing randomly k servers to send the data, "server_indexes" holds these servers 
        server_indexes = []
        for _ in range(k):
            r = random.randint(0, len(servers)-1)
            # we don't want to have duplicated servers 
            while(r in server_indexes):
                r = random.randint(0, len(servers)-1)
            server_indexes.append(r)
        
        # indexing every server that has been choosen above (server_indexes)
        for j in server_indexes:
            
            s = socket.socket()
            ip_address = servers[j][0]
            port = int(servers[j][1])

            try:
                # socket connection 
                s.connect((ip_address, port))
                sending_data = "PUT " + i
                s.send(sending_data.encode())
                data_from_server = s.recv(4098)
                print(f"Response from {ip_address}:{port}: {data_from_server.decode()}")

            except socket.error as e:
                if e.errno == errno.ECONNREFUSED:
                    print(f"Response from {ip_address}:{port} : ERROR")
                else:
                    print("Caught an exception : %s" % e)
            s.close()
        print("====================================")
    print("\nIndexing of servers is finished!\n")

    # checking if all servers (k) are down
    if check_servers(servers, k) == 0:
        print("\nThe program is exitting...")
        return

    print("- Please provide a query:\n")

    # reading user input 
    for line in sys.stdin:

        # check if all servers are down
        if (check_servers(servers, k)) == 0:
            break

        # the user exits the program
        if (line.rstrip() == "EXIT" or line.rstrip() == "exit"):
            s.close()
            break

        # the user input is empty 
        if (line.rstrip() == ""):
            print("\n- Please provide a non-empty query:")
            continue

        command = line.split()

        # if user input is only the command (GET, QUERY etc. without key provided)
        if (len(command) == 1):
            print("\nNo key specified.")
            print("\n- Please provide a well-specified query:\n")
            continue

        # not letting the user to perform 'DELETE' requests when at least one server is down 
        if (command[0] == "DELETE" or command[0] == "delete"):
            if (check_servers(servers, k)) == 1:
                print("\nDELETE request cannot be executed because at least one server is down.")
                print("\nPlease provide a query:\n")
                continue

        # not letting the user to perform other 'PUT' requests 
        if (command[0] == "PUT" or command[0] == "put"):
            print("\n> PUT requests are not supported after server indexing.")
            continue

        # send request to all servers 
        for server in servers:
            s = socket.socket()
            ip_address = server[0]
            port = int(server[1])

            try:
                # connect to socket 
                s.connect((ip_address, port))
                # line is the user input 
                sending_data = line
                # send the data to the server 
                s.send(sending_data.encode())

                data_from_server = s.recv(4098)
                print("====================================")
                print(f"Response from {ip_address}:{port} :\n\n{data_from_server.decode()}")
                if ":" in data_from_server.decode():
                    break
                #print("====================================")
                
            except socket.error as e:
                if e.errno == errno.ECONNREFUSED:
                    print(f"Response from{ip_address}:{port} : ERROR")
                else:
                    print("> Caught an exception: %s" % e)
            
            # the socket is closed 
            s.close()
        print("====================================")
        print("\n- Please provide a query:\n")

    print("\nThe program is exiting...\n")

# returns the error message
def create_error_message():
    print("\nSome arguments are missing. Please provide the required info in this order: kvClient.py -s -i -k, where : \n\n -s is a file with a space separated list of server IPs and their respective ports, \n -i is a file containing data that was output from the previous part of the project, \n -k is the replication factor, i.e. how many different servers will have the same replicated data")

# returns 0 if k servers are down and 1 if at least one server is down
def check_servers(servers, k):
 
    down = 0
    for server in servers:
        s = socket.socket()
        ip_address = server[0]
        port = int(server[1])
        
        try:
            s.connect((ip_address, port))
        except Exception:
            down += 1
        s.close()

    # for DELETE function, it will not be done correctly if at least one server is down 
    if down >= 2:
        print("\nTwo or more servers are down.\n")

    if down == k:
        print("\nAll servers are down, and the operation cannot be correctly executed.")
        return 0

    if down >= 1:
        return 1

    return 2

if __name__ == "__main__":
    main(sys.argv[1:])