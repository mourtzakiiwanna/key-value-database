import math

class TrieNode:
    def __init__(self, payload=None):
        # the payload stored in this node
        self.payload = payload
        # whether this is the end of a word
        self.isEndOfWord = False
        # a dictionary of children nodes
        self.children = {}

class Trie:
    def __init__(self):
        self.root = TrieNode()

    # INSERT function 
    def insert(self, key, payload):
        node = self.root

        # looping through each character in the key
        for char in key:
            # if a char is not found, create a new node in the trie
            if char not in node.children:
                node.children[char] = TrieNode()
            # moving to the next node (the next character)
            node = node.children[char]

        node.payload = payload
        # marking the end of a word
        node.isEndOfWord = True
        return

    # DELETE function 
    def delete(self, key):
        node = self.root

        # looping through each character in the key
        for char in key:
            if char not in node.children:
                return False
            # moving to the next node (the next character)
            node = node.children[char]
        
        node.payload = None
        node.isEndOfWord = False
        # deleting the children of high-level key
        node.children.clear()
        return True

    # SEARCH function (also used in QUERY)
    def search(self, key):
        node = self.root

        # loop through each character in the key
        for char in key:
            if char in node.children:
                node = node.children[char]
            else:
                # key is not present 
                return [False, None]

        # returning true/false if the key was found and a payload with its payload (if found)
        return [node != None and node.isEndOfWord, node.payload]


    # COMPUTE function 
    # math_formula is the math expression (e.g. X+2) and query is the value of X (e.g. X = QUERY key0.age)
    def compute(self, math_formula,query):

        # try:
            # checks if the math formula contains trigonometric/logarithmic functions and replaces it with the actual math function 
            if "cos" in math_formula:
                math_formula = math_formula.replace("cos","math.cos")
            if "tan" in math_formula:
                math_formula = math_formula.replace("tan","math.tan")
            if "sin" in math_formula:
                math_formula = math_formula.replace("sin","math.sin")   
            if "log" in math_formula:
                math_formula = math_formula.replace("log","math.log10")    

            # checking if the math formula contains power function [we will replace the x^y with math.pow(x,y)]
            power_symbol = math_formula.find('^')  
            # if power function exists 
            if (power_symbol != -1):
                base = math_formula[power_symbol-1]
                exponent = math_formula[power_symbol+1]
                
                # if exponent is for example (Y+2), we want to include all the parenthesis index
                if (exponent == "("):
                    res = math_formula.split("^", 1)
                    temp = res[1]
                    end_of_exponent_index = temp.find(")")
                    exponent = temp[0:end_of_exponent_index+1] 
                # if base is for example (Y+2), we want to include all the parenthesis index
                if (base == ")"):
                    res = math_formula.split("^", 1)
                    temp = res[0]
                    start_of_base_index = temp.find("(")
                    base = temp[start_of_base_index:power_symbol]
                 
            math_formula = math_formula.replace(f"{base}^{exponent}",f"math.pow({base},{exponent})")
           
            query_str = ''.join(query)
            var_count = query_str.count('=')

            # first case: query with only one variable (X)
            if var_count == 1:
                query_result = self.search(query[3])
                query_number_result = query_result[1]
                
                # if x is string, we cannot operate the function 
                if (isinstance(query_number_result, str)):
                    result = "This operation cannot be performed because one or many variables are strings."
                    return [True,result]

                # check if X is int , or float
                if query_number_result.isdigit():
                    X = int(query_number_result)
                    x = int(query_number_result)
                else: 
                    X = float(query_number_result)
                    x = float(query_number_result)

                exists = query_number_result != None
            
            # second case: query with two variables (X,Y)
            elif var_count == 2:
                query_result_x = self.search(query[3])
                query_number_result_x = query_result_x[1]

                query_result_y = self.search(query[8])
                query_number_result_y = query_result_y[1]

                # if x or y is string, we cannot operate the function 
                if (isinstance(query_number_result_x, str) or isinstance(query_number_result_y, str)):
                    result = "This operation cannot be performed because one or many variables are strings."
                    return [True,result]
                
                # check if X is int , or float
                if query_number_result_x.isdigit():
                    X = int(query_number_result_x)
                    x = int(query_number_result_x)
                else: 
                    X = float(query_number_result_x)
                    x = float(query_number_result_x)    

                # check if Y is int , or float
                if query_number_result_y.isdigit():
                    Y = int(query_number_result_y)
                    y = int(query_number_result_y)
                else: 
                    Y = float(query_number_result_y)
                    y = float(query_number_result_y)   

                exists = query_number_result_x != None and query_number_result_y != None
            
            # third case: query with three variables (X,Y,Z)
            elif var_count == 3:
                query_result_x = self.search(query[3])
                query_number_result_x = query_result_x[1]

                query_result_y = self.search(query[8])
                query_number_result_y = query_result_y[1]

                query_result_z = self.search(query[13])
                query_number_result_z = query_result_z[1]

                # if x or y or z is string, we cannot operate the function 
                if (isinstance(query_number_result_x, str) or isinstance(query_number_result_y, str) or isinstance(query_number_result_z, str)):
                    result = "This operation cannot be performed because one or many variables are strings."
                    return [True,result]
                    
                # check if X is int , or float
                if query_number_result_x.isdigit():
                    X = int(query_number_result_x)
                    x = int(query_number_result_x)
                else: 
                    X = float(query_number_result_x)
                    x = float(query_number_result_x)    

                # check if Y is int , or float
                if query_number_result_y.isdigit():
                    Y = int(query_number_result_y)
                    y = int(query_number_result_y)
                else: 
                    Y = float(query_number_result_y)
                    y = float(query_number_result_y)    
               
                # check if Z is int , or float
                if query_number_result_z.isdigit():
                    Z = int(query_number_result_z)
                    z = int(query_number_result_z)
                else: 
                    Z = float(query_number_result_z)
                    z = float(query_number_result_z)    

                exists = query_number_result_x != None and query_number_result_y != None and query_number_result_z != None
            
            # evaluating the created math formula 
            result = eval(math_formula)
            return [exists, str(result)] 

        # handling possible errors occured in the COMPUTE function 
        # except Exception: 
        #     return (True,"An error occured with this operation.\n")


        


        
