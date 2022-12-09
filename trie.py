import math

class Node:
    def __init__(self, payload=None):
        self.children = {}
        self.isFinal = False
        self.payload = payload

class Trie:
    def __init__(self):
        # root node
        self.root = Node()

    def insert(self, key, payload):
        curr_node = self.root

        for char in key:
            # If a character is not found, create a new node in the trie
            if char not in curr_node.children:
                curr_node.children[char] = Node()
            curr_node = curr_node.children[char]

        # Leaf node
        curr_node.payload = payload
        curr_node.isFinal = True
        return

    def delete(self, key):
        curr_node = self.root

        for char in key:
            # If a character is not found, create a new node in the trie
            if char not in curr_node.children:
                return False
            curr_node = curr_node.children[char]

        # Clear children of high-level key
        curr_node.children.clear()
        curr_node.payload = None
        curr_node.isFinal = False
        return True

    # Search key in the trie
    def search(self, key):
        curr_node = self.root

        for char in key:
            if char in curr_node.children:
                curr_node = curr_node.children[char]
            else:
                return [False, None]

        return [curr_node != None and curr_node.isFinal, curr_node.payload]


    # Query function
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


        
