"""
Name: Chen Xi Diong
Student ID: 32722656

FIT3155 S1 2023 Assignment 2 - Question 1
"""
import sys

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
            


    def inorder(self, f):
        """
        Inorder traversal of the suffix tree to obtain the values of the suffix array.
        """
        def inorder_aux(node, f):
            """
            Recursive auxiliary function for inorder traversal.
            """
            if node.is_leaf:
                f.write(str(node.suffix_id + 1) + "\n")
                  
            else:
                for child in node.children:
                    if child is not None:
                        inorder_aux(child, res)

        inorder_aux(self.root, f)

if __name__ == "__main__":
    _, filename = sys.argv

    f = open(filename, "r")
    txt = f.read()

    res = open("output_sa.txt", "w")

    st = SuffixTree(txt)
    st.inorder(res)

    f.close()







