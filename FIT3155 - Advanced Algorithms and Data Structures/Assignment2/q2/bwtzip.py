"""
Name: Chen Xi Diong
Student ID: 32722656

Encoder File for FIT3155 S1 2023 Assignment 2 - Question 2
"""
import heapq, sys


class GlobalEnd:
    """
    Creating a reference object Global End used for rapid leaf extension.

    Referenced from week 5 tutorial ukkonen_incomplete.py.
    """
    def __init__(self):
        self.val = -1

    def increment(self):
        self.val += 1

class Node:
    """
    The Node class used for branching and creating a leaf.
    """
    def __init__(self, link=None, start=None, end=None, is_root = False, is_leaf = False):
        self.is_root = is_root
        self.is_leaf = is_leaf
        self.suffix_id = None
        #Edge representation trick
        self.start = start
        self.end = end
        #We need to account for ASCII characters ranging from 36 - 127, and the '$' character.
        self.children = [None] * 91
        #Suffix link
        self.link = link
        

    def get_edge(self, char):
        """
        Getting the edge of the current node that starts with the character char.
        """
        index = ord(char) - 36
        return self.children[index]
    
    def add_edge(self, char, node):
        """
        Adding an edge to the current node that starts with the character char.
        """
        index = ord(char) - 36
        self.children[index] = node

    def get_start(self):
        """
        Getter for start value.
        """
        return self.start
    
    def get_end(self):
        """
        Getter for end value.
        """
        #If it is a leaf node, return global end value
        if self.is_leaf:
            return self.end.val
        else:
            return self.end

class SuffixTree:
    def __init__(self, s):
        #Adding the terminal character
        self.text = s + '$'
        #Creating the root node
        self.root = Node(is_root=True)
        self.root.link = self.root
        #Creating the global end object
        self.ge = GlobalEnd()
        #Creating the previous node for suffix link
        self.prev_node = None

        self.active_node = self.root
        self.active_length = 0
        self.active_edge = None

        self.ukkonnen()
        
    def traverse(self, i, active_node, active_len):
        """
        Traversing the tree to obtain the active node and active length.
        """
        
        def traverse_aux(curr_node, curr_len):
            """
            Recursive auxiliary function for traversing the tree.
            """
            #Base case: Current node is a leaf or there is no more length to traverse
            if curr_node.is_leaf or curr_len == 0:
                return curr_node, curr_len
        
            #Getting the active edge
            AE = curr_node.get_edge(self.text[i-curr_len])

            #if the active edge doesn't exist, terminate
            if AE is None:
                return curr_node, curr_len
            
            else:
                #Calculating the active edge length
                ae_length = AE.get_end() - AE.get_start() + 1

                #if length of the edge is greater than length of substring, terminate
                if ae_length > curr_len:
                    return curr_node, curr_len
                
                #Otherwise update the current node and current length and continue searching
                curr_node = AE
                curr_len = curr_len - ae_length
                
                return traverse_aux(curr_node, curr_len)
                
        return traverse_aux(active_node, active_len)



    def makeExtension(self, i, j, active_node, active_length, active_edge):
        """
        Perform extension j of phase i on the suffix tree.
        """
        char = self.text[i-active_length]
        #Flag for rule 3
        do_nothing = False

        #Rule 2 Reg: We hang leaf on an existing node
        if active_edge is None:
            leaf = Node(start=i-active_length, end=self.ge, is_leaf=True)
            leaf.suffix_id = j
            active_node.add_edge(char, leaf)

            if self.active_length > 0:
                self.active_length -= 1
            self.active_node = self.active_node.link

        #Rule 2 Alt: Substring does not exist in tree, split edge
        elif self.text[i] != self.text[active_edge.get_start() + active_length]:
            #Create one node for the branching, one leaf to hang at the new node
            node = Node(link = self.root, start=active_edge.get_start(), end=active_edge.get_start() + active_length - 1)
            leaf = Node(link = self.root, start=i, end=self.ge, is_leaf=True)
            leaf.suffix_id = j
            #Update parent-children relations
            active_node.add_edge(char, node)
            node.add_edge(self.text[active_edge.get_start() + active_length], active_edge)
            active_edge.start = active_edge.get_start() + active_length
            node.add_edge(self.text[i], leaf)

            #Update suffix link
            if self.prev_node is not None:
                self.prev_node.link = node
            self.prev_node = node
            
            #Skip count trick 
            if self.active_node is self.root:
                self.active_length -= 1
            self.active_node = self.active_node.link
            
        #Rule 3: Do nothing
        else:
            do_nothing = True
            
        return do_nothing


    def ukkonnen(self):
        """
        Building a Suffix Tree using Ukkonen's Algorithm
        """
        #Variable initialisation
        i = 0
        j = 0
        n = len(self.text)
        
        while i < n:
            #Incrementing global end to perform rapid leaf extension
            self.ge.increment()

            #Resetting the previous node for suffix link
            self.prev_node = None

            self.active_node = self.root
            self.active_length = i - j

            while j <= i:
                #Traversing the tree to obtain active node and active length
                self.active_node, self.active_length = self.traverse(i, self.active_node, self.active_length)

                #Finding the active edge
                self.active_edge = self.active_node.get_edge(self.text[i-self.active_length])

                #With information from active node, active length and active edge, we perform an extension 
                if(self.makeExtension(i, j, self.active_node, self.active_length, self.active_edge)):
                    #IF we meet a rule 3, freeze j, increment i
                    break

                #Move to next extension
                j += 1

            
            #Move to next phase
            i += 1
            


    def inorder(self, res):
        """
        Inorder traversal of the suffix tree to obtain the values of the suffix array.
        """
        def inorder_aux(node, res):
            """
            Recursive auxiliary function for inorder traversal.
            """
            if node.is_leaf:
                res.append(node.suffix_id)
                  
            else:
                for child in node.children:
                    if child is not None:
                        inorder_aux(child, res)

            return res

        return inorder_aux(self.root, res)


class BytePacker:
    """
    BytePacker Class to pack bits into bytes and write to a binary file.    
    """
    def __init__(self):
        self.bitstring = ""
        self.file = open("bwtencoded.bin", "wb")

    def append(self, bitstring):
        """
        Appends a bitstring to the current bitstring
        """
        self.bitstring += bitstring

    def write_to_file(self):
        """
        Writes the current bitstring to byte (8-bit) chunks and stores in the file
        """
        while len(self.bitstring) >= 8:
            to_write = self.bitstring[:8]
            self.bitstring = self.bitstring [8:]
            int_to_pack = int(to_write, 2)
            byte_to_pack = int_to_pack.to_bytes(1, byteorder='big')

            self.file.write(byte_to_pack)

    def close(self):
        """
        Closes the file.
        """
        self.file.close()

    def getbitstring(self):
        """
        Getter of the current bitstring.
        """
        return self.bitstring

def bwt(s):
    """
    Generates the Burrows-Wheeler Transform of a string s from a suffix array, using the Suffix Tree from q1.
    """
    suffix_tree = SuffixTree(s)
    suffix_array = suffix_tree.inorder([])
    n = len(s)
    res = ""

    for i in range(n):
        res += s[suffix_array[i] - 1]
        
    return res

def elias_code(n):
    """
    Generates the Elias code of a number n.
    """
    if n == 1:
        return "1"
    res = int_to_bin(n)
    L = len(res) - 1

    while L > 1:
        temp = int_to_bin(L)
        temp = "0" + temp[1:]
        L = len(temp) - 1
        res = temp + res


    res = "0" + res

    return res

def int_to_bin(n):
    """
    Integer to Binary converter.
    """
    if n == 0 or n == 1:
        return str(n)
    res = ""
    while n != 1:
        res = str(n%2) + res
        n >>= 1 #n = n // 2
    res = str(n) + res
    return res

def huffman(s):
    """
    The Huffman Encoding Algorithm
    """
    #Counting the frequencies of each character, while also keeping track of the number of unique characters
    uniq = 0
    count_arr = [0] * 91 #accounting for ASCII 36-126
    for char in s:
        if count_arr[ord(char)-36] == 0:
            uniq += 1
        count_arr[ord(char)-36] += 1


    #Setting up the heap
    h = []
    for i in range(0, len(count_arr)):
        if count_arr[i] > 0:
            heapq.heappush(h, (count_arr[i], chr(i+36)))
            
    #Generating the Huffman Encoding
    res = [None] * 91
    while len(h) > 1:
        freq1, str1 = heapq.heappop(h)
        for char in str1:
            if res[ord(char)-36] is None:
                res[ord(char)-36] = "0"
            else:
                res[ord(char)-36] += "0"

        freq2, str2 = heapq.heappop(h)
        for char in str2:
            if res[ord(char)-36] is None:
                res[ord(char)-36] = "1"
            else:
                res[ord(char)-36] += "1"

        heapq.heappush(h, (freq1+freq2, str1+str2))

    for i in range(len(res)):
        if res[i]:
            res[i] = ''.join(reversed(res[i]))

    return res, uniq

def encoding(s):
    """
    Zips a string s using Burrows-Wheeler Transform and Runlength Encoding.
    """
    #Setting up the byte packer
    byte_packer = BytePacker()
    
    #Appending terminal '$' character and generating the BWT string
    s += "$"
    s = bwt(s)
    #============================================Header part=================================================
    #Encoding the length
    res = elias_code(len(s))
    

    huffman_code, n_unique = huffman(s)
    #Encoding the number of unique characters
    res += elias_code(n_unique)


    #packing 8 bis into 1 byte
    byte_packer.append(res)
    byte_packer.write_to_file()
    res = ""
    
    for i in range(len(huffman_code)):
        if huffman_code[i] is not None:
            ascii_bin = int_to_bin(i+36)
            #pad zeroes + ASCII(char) + elias_codeCode(codelen) + HuffmanCode(char)
            res += ("0" * (7-len(ascii_bin))) + ascii_bin + elias_code(len(huffman_code[i])) + huffman_code[i]
            #since each ASCII code is 7 bits, res is guaranteed to have more than 8 bits in each encoding
            byte_packer.append(res)
            byte_packer.write_to_file()
            res = ""

    #=============================================Data part=================================================
    #runlength encoding
    count = 1
    encoded = 0
    for i in range(0,len(s)-1):

        #if the next char is different from the current
        if s[i] != s[i+1]:
            #save the current result and reset count
            res += huffman_code[ord(s[i])-36] + elias_code(count)
            count = 1
            #if the next character is the last character, we save it with count 1
            if i+1 == len(s)-1:
                res += huffman_code[ord(s[i+1])-36] + elias_code(count)
                encoded += 1
        
        #if the next char is same as the current
        elif s[i] == s[i+1]:
            count += 1
            #if the next character is the last character, we save it with the already incremented count
            if i+1 == len(s)-1:
                res += huffman_code[ord(s[i])-36] + elias_code(count)
                encoded += 1

        #approximately every 2 runlength encodings will make res longer than 8 bits
        if encoded%2 == 1:
            byte_packer.append(res)
            byte_packer.write_to_file()
            res = ""
    
    res = byte_packer.getbitstring()
    res += "0" * (8 - len(res))
    byte_packer.append(res)
    byte_packer.write_to_file()
    
    byte_packer.close()

    return res

if __name__ == "__main__":
    _, filename = sys.argv

    f = open(filename, "r")
    s = f.read()

    encoding(s)

    f.close()


