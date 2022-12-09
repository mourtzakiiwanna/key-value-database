import math

class TrieNode:
    def __init__(self, payload=None):
        # the payload stored in this node
        self.payload = payload
        # whether this is the end of a word
        self.isEndOfWord = False
        # a dictionary of child nodes
        self.children = {}

class Trie:
    def __init__(self):
        self.root = TrieNode()

    # INSERT function 
    def insert(self, key, payload):
        node = self.root

        # Loop through each character in the key
        for char in key:
            # If a char is not found, create a new node in the trie
            if char not in node.children:
                node.children[char] = TrieNode()
            
            # moving to the next node (the next character)
            node = node.children[char]

        node.payload = payload
        # Mark the end of a word
        node.isEndOfWord = True
        return

    # DELETE function 
    def delete(self, key):
        node = self.root

        # Loop through each character in the key
        for char in key:
            if char not in node.children:
                return False

            # Moving to the next node (the next character)
            node = node.children[char]
        
        node.payload = None
        node.isEndOfWord = False
        # Delete the children of high-level key
        node.children.clear()
        return True

    # SEARCH function (also used in QUERY)
    def search(self, key):
        node = self.root

        for char in key:
            if char in node.children:
                node = node.children[char]
            else:
                # key is not present 
                return [False, None]

        # Returns true/false if the key was found and a payload with its payload (if found)
        return [node != None and node.isEndOfWord, node.payload]


    # COMPUTE function 
    def compute(self, math_formula,query):
        if "cos" in math_formula:
            math_formula = math_formula.replace("cos","math.cos")
        if "tan" in math_formula:
            math_formula = math_formula.replace("tan","math.tan")
        if "sin" in math_formula:
            math_formula = math_formula.replace("sin","math.sin")   
        if "log" in math_formula:
            math_formula = math_formula.replace("log","math.log10")    

        query_str = ''.join(query)
        var_count = query_str.count('=')
        if var_count == 1:
            query_result = self.search(query[3])
            query_number_result = query_result[1]
            # Check if X is int , or float
            if query_number_result.isdigit():
                X = int(query_number_result)
                x = int(query_number_result)
            else: 
                X = float(query_number_result)
                x = float(query_number_result)

            exists = query_number_result != None

        elif var_count == 2:
            query_result_x = self.search(query[3])
            query_number_result_x = query_result_x[1]
            # Check if X is int , or float
            if query_number_result_x.isdigit():
                X = int(query_number_result_x)
                x = int(query_number_result_x)
            else: 
                X = float(query_number_result_x)
                x = float(query_number_result_x)    

            query_result_y = self.search(query[8])
            query_number_result_y = query_result_y[1]
            # Check if X is int , or float
            if query_number_result_y.isdigit():
                Y = int(query_number_result_y)
                Y = int(query_number_result_y)
            else: 
                Y = float(query_number_result_y)
                Y = float(query_number_result_y)   

            exists = query_number_result_x != None and query_number_result_y != None
           
            
        elif var_count == 3:
            query_result_x = self.search(query[3])
            query_number_result_x = query_result_x[1]
            # Check if X is int , or float
            if query_number_result_x.isdigit():
                X = int(query_number_result_x)
                x = int(query_number_result_x)
            else: 
                X = float(query_number_result_x)
                x = float(query_number_result_x)    

            query_result_y = self.search(query[8])
            query_number_result_y = query_result_y[1]
            # Check if Y is int , or float
            if query_number_result_y.isdigit():
                Y = int(query_number_result_y)
                Y = int(query_number_result_y)
            else: 
                Y = float(query_number_result_y)
                Y = float(query_number_result_y)    

            query_result_z = self.search(query[13])
            query_number_result_z = query_result_z[1]
            # Check if Z is int , or float
            if query_number_result_z.isdigit():
                Z = int(query_number_result_z)
                Z = int(query_number_result_z)
            else: 
                Z = float(query_number_result_z)
                Z = float(query_number_result_z)    

            exists = query_number_result_x != None and query_number_result_y != None and query_number_result_z != None
        
        result = eval(math_formula)
        return [exists, str(result)] 


        
