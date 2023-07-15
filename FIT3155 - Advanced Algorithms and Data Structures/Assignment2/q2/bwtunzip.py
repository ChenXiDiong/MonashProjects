"""
Name: Chen Xi Diong
Student ID: 32722656

Decoder File for FIT3155 S1 2023 Assignment 2 - Question 2
"""
import sys

class HuffmanTree:
    """
    The Huffman Tree Class to store the huffman tree and decode the huffman code.
    """
    def __init__(self):
        self.root = Node()

    def insert(self, code, char):
        """
        Inserts a character into the huffman tree based on the huffman code.
        """
        curr = self.root
        for c in code:
            if c == '0':
                if curr.left is None:
                    curr.left = Node()
                curr = curr.left
            elif c == '1':
                if curr.right is None:
                    curr.right = Node()
                curr = curr.right

        curr.data = char

    def traverse(self, code, curr):
        """
        Traverses the huffman tree based on the huffman code.
        """
        if code == '0':
            return curr.left
        elif code == '1':
            return curr.right

class Node:
    """
    The Node of a Huffman Tree.
    """
    def __init__(self):
        self.data = None
        self.left = None
        self.right = None

    def isleaf(self):
        """
        An indication of whether the node is a leaf node.
        """
        return self.left is None and self.right is None

class ByteUnpacker:
    """
    ByteUnpacker Class to read from a binary file and unpack bytes into bits.   
    """
    def __init__(self, filename):
        self.file = open(filename, "rb")
        self.bytestring = self.file.read()
        self.buffer = ""
        self.counter = 0

        self.file.close()
        
    def unpack_byte(self):
        """
        Writes the current bitstring to byte (8-bit) chunks and stores in the file
        """
        if self.counter >= len(self.bytestring):
            return 
        s = int.from_bytes(self.bytestring[self.counter:self.counter+1], byteorder='big')
        self.counter += 1
        for i in range(8):
            #Saves the i-th bit using bitwise operations
            self.buffer += str((s >> (7-i)) & 1) 
        return 

class Decoder:
    def __init__(self, filename):
        self.unpacker = ByteUnpacker(filename)
        self.huffman_tree = HuffmanTree()

    def elias_decode(self, length):
        """
        Decodes the elias code from the string s starting from index i.
        """
        res = ""
        while len(self.unpacker.buffer) < length:
            self.unpacker.unpack_byte()

        #If current component is a length:
        if self.unpacker.buffer[0] == "0":
            res += "1"

            for i in range(1,length):
                res += self.unpacker.buffer[i]

            length = self.bin_to_int(res) + 1
            return None, length

        elif self.unpacker.buffer[0] == "1":
            for i in range(length):
                res += self.unpacker.buffer[i]

            return self.bin_to_int(res), 1

    def bin_to_int(self, s):
        i = 0
        n = len(s)
        res = 0
        while i < n:
            if s[i] == '1':
                res += 2**(n-i-1)
            i += 1

        return res

    def preprocess(self, s):
        """
        Preprocesses the string to obtain nOccurrences matrix and rank array.
        
        """
        #init
        nOccurences = []
        memo = [0] * 91 #Accounting for 36-126 in ASCII
        rank_array = [None] * len(memo)
        rank_array[0] = 1
        rank = 1
        
        for i in range(len(s)):
            index = ord(s[i]) - 36
            memo[index] += 1
            temp = [i for i in memo]
            nOccurences.append(temp)

        prev = memo[0]
        for i in range(1,len(memo)):
            if memo[i] != 0:
                rank += prev
                prev = memo[i]
                rank_array[i] = rank

        return nOccurences, rank_array
    
    def invert_bwt(self, s):
        """
        Inverts the BWT string into the original message.
        """
        res = ""
        nOccurences, rank_array = self.preprocess(s)
        i = 1
        while True:
            char = s[i-1]
            if char == '$':
                res += '$'
                break
            res = char + res
            
            r = rank_array[ord(char)-36]
            n = nOccurences[i-1][ord(char)-36] - 1
            i = n + r

        return res

    def decoding(self):
        #Obtaining the length of the original message
        L = None
        length = 1
        while L is None:
            #A copy of the previous length for string slicing
            ori_length = length
            L, length = self.elias_decode(length)
            self.unpacker.buffer = self.unpacker.buffer[ori_length:]
        
        #Obtaining the number of unique characters in the BWT string
        n_unique = None
        while n_unique is None:
            ori_length = length
            n_unique, length = self.elias_decode(length)
            self.unpacker.buffer = self.unpacker.buffer[ori_length:]

        #Building the huffman tree
        while n_unique > 0:
            #decoding the character
            if len(self.unpacker.buffer) < 7:
                self.unpacker.unpack_byte()
            ascii_bin = self.bin_to_int(self.unpacker.buffer[:7])
            self.unpacker.buffer = self.unpacker.buffer[7:]
            
            char = chr(ascii_bin)

            #decoding the length of the huffman code
            huffman_codelen = None
            while huffman_codelen is None:
                ori_length = length
                huffman_codelen, length = self.elias_decode(length)
                self.unpacker.buffer = self.unpacker.buffer[ori_length:]

            while len(self.unpacker.buffer) < huffman_codelen:
                self.unpacker.unpack_byte()

            huffman_code = self.unpacker.buffer[:huffman_codelen]
            self.unpacker.buffer = self.unpacker.buffer[huffman_codelen:]
            

            #Inserting into the Huffman Tree
            self.huffman_tree.insert(huffman_code, char)

            n_unique -= 1

        
        #Runlength decoding
        res = ""
        while len(res) < L:
            curr = self.huffman_tree.root
            while not curr.isleaf():
                if len(self.unpacker.buffer)<=1:
                    self.unpacker.unpack_byte()
                curr = self.huffman_tree.traverse(self.unpacker.buffer[0], curr)
                self.unpacker.buffer = self.unpacker.buffer[1:]
                
            char = curr.data
            runlength = None
            while runlength is None:
                ori_length = length
                runlength, length = self.elias_decode(length)
                self.unpacker.buffer = self.unpacker.buffer[ori_length:]
            

            for _ in range(runlength):
                res += char
        
        res = self.invert_bwt(res)

        return res

if __name__ == "__main__":
    _, filename = sys.argv

    dc = Decoder(filename)
    res = dc.decoding()
    res = res[:len(res)-1]

    #write result to a file
    f = open("recovered.txt", "w")
    f.write(res)







