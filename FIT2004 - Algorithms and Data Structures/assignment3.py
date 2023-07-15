"""
S2 2022 FIT2004 Assignment 3
Python 3.9.6

Name: Diong Chen Xi
Student ID: 32722656
Email: cdio0004@student.monash.edu
"""

import math

class FlowNetwork:
    """
    Initialises the FlowNetwork.

    :Input: 
        availability: A list of lists containing the availability of the housemates for various days.

    :Postcondition: A flow network consisting of all the nodes, edges with flow/constraint/capacity is set up.

    :Time Complexity: O(N) where N is the length of availability. We need O(N) time to create the O(N) space
    for various nodes and edges.

    :Aux Space Complexity: O(N) where N is the length of availability. We have to create 10 nodes at minimum 
    (source, x, sink, z, 5 housemates, the restaurant), and at maximum (10 + 6N + 2N) nodes 
    ((5 people + 1 restaurant) to N-day pairs and 2N meals), which requires O(N) space. Adding on the O(N) 
    auxiliary space complexity from the function call to add_edges(), the overall auxiliary space complexity is
    O(N) + O(N) = O(N).
    """
    def __init__(self, availability):
        i = len(availability) # the number of days
        #1 vertex for x, 1 vertex for source
        #6 vertices for 5 housemates and the restaurant 
        #i vertices for breakfasts and i vertices for dinners
        #1 vertex z, 1 vertex for target
        self.vertices = [None] * (2 + 6)

        #setting up the vertices
        self.vertices[0] = Node("s", "Source")
        self.vertices[1] = Node("x", "Node", -2*i)
        
        id = 1
        #setting up nodes for people
        for k in range(2, 2+5):
            self.vertices[k] = Node(id, "Person")
            id += 1

        #setting up node for the restaurant
        self.vertices[7] = Node(6, "Restaurant")

        for j in range(len(availability)):
            for k in range(len(availability[j])):
                if availability[j][k] > 0:
                    self.vertices.append(Node(j+1, typeof="Person " + str(k+1) + " Day "))

        self.days = len(self.vertices) #an indicator of how many selector nodes are created
        
        
        id = 1
        #setting up nodes for breakfasts
        for k in range(self.days, self.days+i):
            self.vertices.append(Node(id, "Breakfast"))
            id += 1

        id = 1
        #setting up nodes for dinners
        for k in range(self.days+i, self.days+2*i):
            self.vertices.append(Node(id, "Dinner"))
            id += 1

        self.vertices.append(Node("z", "Node", 2*i))
        self.vertices.append(Node("t", "Target"))

        self.add_edges(availability)
    

    def __str__(self):
        retstr = ""
        for i in range(len(self.vertices)-1):
            retstr += str(self.vertices[i]) + "\n"
        retstr += str(self.vertices[-1]) 
        
        return retstr

    """
    Adding all edges with flow/constraint/capacity connecting the Nodes to one another.

    :Input: 
        availability: A list of lists containing the availability of the housemates for various days.

    :Postcondition: The Nodes are connected to one another by flow edges.

    :Time Complexity: O(N) where N is the number of Nodes in the FlowNetwork. The worst case is when the availability list consists of all 3s
    (i.e. every person has availability on every meal), we would have a maximum number of nodes, and every selector node is connected to the
    breakfast and dinner nodes, which the number of edges is still close to N. The number of edges would never exceed a linear growth of N, 
    therefore the overall time complexity is O(N).

    :Aux Space Complexity: O(N) where N is the number of Nodes in the FlowNetwork. At worst case we would have to create O(N) edges connecting
    the Nodes to represent the network.
    """
    def add_edges(self, availability):
        i = len(availability)

        #flow from x to all the people
        for k in range(2, 2+5):
            self.vertices[1].edges.append(Edge(self.vertices[1], self.vertices[k], flow=0, constraint=math.floor(0.36*i), capacity=math.ceil(0.44*i)))

        #flow from x to the restaurant
        self.vertices[1].edges.append(Edge(self.vertices[1], self.vertices[7], flow=0, capacity=math.floor(0.1*i)))


        #flow from people to days
        #housemates are self.vertices[2...6], restaurant is self.vertices[7]
        #days are self.vertices [8...self.days]
        #breakfasts are self.vertices [self.days...self.days+i]
        #dinners are self.vertices [self.days+i...self.days+2i]
        #availability: 0(not available), 1(only breakfast), 2(only dinner), 3(both available)
        index = 0
        for j in range(len(availability)):
            for k in range(len(availability[j])):
                if availability[j][k] > 0: 
                    self.vertices[k+2].edges.append(Edge(self.vertices[k+2], self.vertices[index+8], capacity=1))
                    index += 1


        #flow from days to breakfasts and dinners
        index = 0
        for j in range(len(availability)):
            for k in range(len(availability[j])):
                if availability[j][k] > 0:
                    if availability[j][k] == 1:
                        self.vertices[index+8].edges.append(Edge(self.vertices[index+8], self.vertices[self.days+j], capacity=1))
                    elif availability[j][k] == 2:
                        self.vertices[index+8].edges.append(Edge(self.vertices[index+8], self.vertices[self.days+j+i], capacity=1))
                    elif availability[j][k] == 3:
                        self.vertices[index+8].edges.append(Edge(self.vertices[index+8], self.vertices[self.days+j], capacity=1))
                        self.vertices[index+8].edges.append(Edge(self.vertices[index+8], self.vertices[self.days+j+i], capacity=1))
                    index += 1
            #flow from restaurants to breakfasts and dinners
            self.vertices[7].edges.append(Edge(self.vertices[7], self.vertices[self.days+j], capacity=1))
            self.vertices[7].edges.append(Edge(self.vertices[7], self.vertices[self.days+j+i], capacity=1))

        #flow from breakfasts and dinners to z
        for i in range(self.days, len(self.vertices)-2):
            self.vertices[i].edges.append(Edge(self.vertices[i], self.vertices[-2], constraint=1, capacity=1))
            
    """
    Removes the lower bounds from the edges of the flow network by converting them into demands and decreasing 
    capacities.

    :Postcondition: The lower bounds (constraints) are removed from the network (i.e. set to 0) 

    :Time complexity: O(V+E) where V is the number of Nodes in the FlowNetwork, and E is the number of Edges 
    in the FlowNetwork. The function loops through the whole FlowNetwork and performs an update on the 
    edge if required.

    :Aux Space Complexity: O(E) where E is the number of Edges in the FlowNetwork. There are temporary lists
    created to store the edges with capacity > 0 and then reassigned back to a Node's edges attribute. The worst 
    case is when there are no edges to be removed, therefore we need to store E edges back into the lists.
    """
    def remove_lowerbound(self):
        for vertex in self.vertices:
            for edge in vertex.edges:
                edge.u.demand += edge.constraint # + outgoing
                edge.v.demand -= edge.constraint # - incoming
                edge.capacity -= edge.constraint
                edge.constraint = 0
            

    """
    Removes the demands from the Nodes in the FlowNetwork by setting up a source Node that links to Nodes with 
    negative demand and a sink Node that links to Nodes with positive demand.

    :Postcondition: The demands are removed from the Nodes (i.e. set to 0).

    :Time Complexity: O(V) where V is the number of Nodes in the FlowNetwork. The worst case is when all Nodes 
    have a demand, so we have to create O(V) Edges to be linked to either the source or the sink.

    :Aux Space Complexity: O(V) where V is the number of Nodes in the FlowNetwork. We have to create O(V) new 
    edges and store them in the list of edges of the Nodes.
    """
    def remove_demand(self):
        for vertex in self.vertices:
            if vertex.demand < 0: #link -ve demands to source
                self.vertices[0].edges.append(Edge(self.vertices[0], vertex, flow=0, constraint=0, capacity=-vertex.demand))
                vertex.demand = 0
            elif vertex.demand > 0: #link +ve demands to sink
                vertex.edges.append(Edge(vertex, self.vertices[-1], flow=0, constraint=0, capacity=vertex.demand))
                vertex.demand = 0

    """
    Resets the .visited attribute of all the Nodes in the FlowNetwork for dfs.

    :Postcondition: All the .visited attributes of the Nodes of the FlowNetwork are reset back to False.

    :Time Complexity: O(V) where V is the number of Nodes in the FlowNetwork. We have to loop through every node in the network.

    :Aux Space Complexity: O(1) as no extra space is created.
    """
    def reset(self):
        for vertex in self.vertices:
            vertex.visited = False

    """
    Performs dfs to find if there's an augmenting path and performs augmentation at the same time. 
    Referenced from FIT2004 course notes page 125 pseudocode.

    :Input:
        source: The Node to start the dfs from.
        target: The target Node that we want to reach.
        bottleneck: the minimum flow of all the Edges of the augmenting path.

    :Return: An integer indicating the minimum flow that is augmented from the dfs.

    :Time Complexity: O(N) where N is the number of Nodes in the FlowNetwork. The worst case is 
    when we can't hit the target Node, where we have to traverse at most N-1 Nodes of the network.

    :Space Complexity: O(1) as there is only constant space created for each recursion.
    """
    def dfs(self, source, target, bottleneck):
        #base case : reached target, there is an augmenting path
        if source == target:
            return bottleneck
        source.visited = True
        for edge in source.edges:
            residual = edge.capacity - edge.flow
            if residual > 0 and not edge.v.visited:
                edge.v.previous = edge.u
                augment = self.dfs(edge.v, target, min(bottleneck, residual))
                if augment > 0:
                    edge.flow += augment
                    edge.reverse.flow -= augment
                    return augment
        return 0 

    """
    Runs dfs and augments the flow network until there are no more augmenting paths in the FlowNetwork.
    Referenced from FIT2004 course notes page 125 pseudocode.

    :Input:
        source: The Node to start the dfs from. Expected to be the source Node.
        target: The target Node that we want to reach. Expected to be the sink Node.

    :Return: The maximum flow in the network obtained by Ford Fulkerson method.

    :Time Complexity: O(N^2), where N is the number of Nodes in the FlowNetwork. The worst case time 
    complexity for the dfs() function call is O(N), and for each iteration of the while loop we only augment 
    1 flow, up until the maximum flow, therefore the total time complexity is max_flow * O(N) = O(max_flow * N).
    The maximum flow is always the number of meals specified, which is 2N, thus the overall time complexity is 
    O(2N * N) = O(N^2).

    :Aux Space Complexity: O(1) as only constant space is created for the recursive dfs.
    """
    def mincut(self, source, target):
        flow = 0
        while True:
            self.reset()
            augment = self.dfs(source, target, math.inf)
            flow += augment 
            if augment == 0:
                break
        return flow      
        

class Node:
    def __init__(self, id, typeof, demand=0):
        self.demand = demand
        self.id = id
        self.typeof = typeof
        self.edges = []
        self.previous = None
        self.visited = False

    def __str__(self):
        retstr = self.typeof + ": " + str(self.id)
        if self.demand != 0:
            retstr += " with demand " + str(self.demand)
        retstr += "\n"
        for edge in self.edges:
            retstr += str(edge)
        return retstr


class Edge:
    def __init__(self, u, v, flow=0, constraint=0, capacity=0, is_reverse=False) -> None:
        self.u = u
        self.v = v
        self.flow = flow
        self.constraint = constraint
        self.capacity = capacity
        self.flow = 0
        self.is_reverse=is_reverse
        if not is_reverse:
            self.reverse = Edge(v, u, -flow, is_reverse=True)
            self.reverse.reverse = self
            v.edges.append(self.reverse)

    def __str__(self):
        return "Flow from " + self.u.typeof + ": " + str(self.u.id) + " to " + self.v.typeof + ": " + str(self.v.id) + " " + str(self.flow) + "/" + str(self.constraint) + "/" + str(self.capacity) + "\n"
        

"""
Given an availability table, performs allocation of meal preparation of the housemates.

:Input: A list of lists containing the availability of the housemates for various days.

:Return: A tuple of lists (breakfast, dinner) where lists breakfast and dinner specify a
valid allocation. breakfast[i] = j if person numbered j is allocated to prepare breakfast
on day i, otherwise breakfast[i] = 5 to denote that the breakfast will be ordered from
a restaurant on that day. Similarly, dinner[i] = j if person numbered j is allocated to
prepare dinner on day i, otherwise dinner[i] = 5 to denote that the dinner will be ordered
from a restaurant on that day. None otherwise if there is no possible allocation.

:Time complexity: 
FlowNetwork initialisation = O(N) 
remove_lowerbound() = O(V+E) 
remove_demand() = O(V)
mincut() = O(N^2)
Where N is the length of availability, V is the number of Nodes in the FlowNetwork, E is the 
number of Edges in the FlowNetwork.
The dominant function is the mincut() function, therefore the overall time complexity is O(N^2).

:Aux Space Complexity: 
FlowNetwork initialisation = O(V) 
remove_lowerbound() = O(E) 
remove_demand() = O(V)
mincut() = O(1)
Where V is the number of Nodes in the FlowNetwork, E is the number of Edges in the FlowNetwork.
The total auxiliary space complexity is O(V + E + V) = O(2V + E) = O(V+E).
"""
def allocate(availability):
    network = FlowNetwork(availability)
    network.remove_lowerbound()
    network.remove_demand()
    maxflow = network.mincut(network.vertices[0], network.vertices[-1])
    #no max flow can be achieved, it is not feasible
    if maxflow != 2*len(availability):
        return None

    breakfasts = [None] * len(availability)
    dinners = [None] * len(availability)
    for i in range(2,7):
        for edge in network.vertices[i].edges:
            if edge.is_reverse == False:
                for edgeb in edge.v.edges:
                    if edgeb.flow > 0:
                        if edgeb.v.typeof == "Breakfast":
                            breakfasts[edgeb.v.id-1] = network.vertices[i].id-1
                        else:
                            dinners[edgeb.v.id-1] = network.vertices[i].id-1

    for edge in network.vertices[7].edges:
        if edge.is_reverse == False:
            if edge.flow > 0:
                if edge.v.typeof == "Breakfast":
                    breakfasts[edge.v.id-1] = 5
                else:
                    dinners[edge.v.id-1] = 5

    return (breakfasts,dinners)
    

#===================================== Question 2 ================================================
#%% Node data structure
class TrieNode:
    """
    Initialises a Node of a Trie.

    :Input:
        size: An integer indicating the size of the maximum number of children a Node can have.
        data: The data to be stored on the node.

    :Postcondition: A Node containing a list of its children is created, and a payload is stored within it.
    
    :Time complexity: O(N) where N is the size provided via input. We always create a list within the node, whereby its size depends on the input given.

    :Aux sspace complexity: O(N) where N is the size provided via input. 
    """
    def __init__(self, size=28, data=None):
        self.data = data
        self.first_str = False
        #all 26 characters, plus a terminal '$' at index 0, and a space character ' ' at index 27
        self.link = [None] * size 

#%% Trie data structure
class Trie:
    """
    Initialises the Trie data structure.

    :Postcondition: A Trie with a root node is created, and an attribute corresponding to the longest common substring is stored.

    :Time complexity: O(1). Since we do not supply any input to the creation of a TrieNode, it is always created in O(28) = O(1) time.
    
    :Aux space complexity: O(1) since we are creating a TrieNode with constant size children array.
    """
    def __init__(self):
        self.root = TrieNode()
        self.longest_common_substring = ""

    """
    Inserts a key into the TrieNode recursively.

    :Input:
        key: A string of the key to be inserted.
        is_first: An indication of whether the key is the first string to be inserted into the Trie.
        i: The current pointer towards the character of the key we are inserting.
        data: The longest substring we can find for inserting the current key.

    :Postcondition: The key is inserted into the Trie.

    :Time complexity: O(N) where N is the length of the key. The worst case complexity of the auxiliary function is
    O(N).

    :Aux Space complexity: O(N) where N is the length of the key. There is no extra space created in this function,
    but its call to the auxiliary function has an auxiliary space complexity of O(N).
    """
    def recursive_insert(self, key, is_first, i=0, data=""):
        current = self.root
        self.recursive_insert_aux(current, i, is_first, key, data)


    """
    The auxiliary function for recursive insert into the Trie.

    :Input: 
        current: The current Node that is visited.
        i: The current pointer towards the character of the key we are inserting.
        is_first: An indication of whether the key is the first string to be inserted into the Trie.
        key: A string of the key to be inserted.
        data: The longest substring we can find for inserting the current character.

    :Time compleity: O(N) where N is the length of the key. The worst case is when the key has no common characters with those
    in the Trie, so we have to create N new nodes, each in O(1) time.

    :Aux space complexity: O(N) where N is the length of the key. The worst case is when the key has no common characters with those
    in the Trie, so we have to create N new nodes, each with a children array of O(28) size, totalling up to a auxiliary space
    complexity of O(28*N) = O(N).
    """
    def recursive_insert_aux(self, current, i, is_first, key, data=""):
        #base case : reached $
        if i == len(key):
            index = 0
            if current.link[index] is not None:
                current = current.link[index]
                if is_first:
                    current.first_str = True
            
            else:
                current.link[index] = TrieNode()
                current = current.link[index]
                if is_first:
                    current.first_str = True
            
            if len(data) > len(self.longest_common_substring):
                self.longest_common_substring = data
            return
        #recursive step
        else:
            if key[i] == ' ':
                index = 27
            else:
                index = ord(key[i]) - 97 + 1
            #if path: move current
            if current.link[index] is not None:
                current = current.link[index]
                if is_first:
                    current.first_str = True
                else:
                    if current.first_str == True:
                        data += key[i]
                
            #otherwise: create path, move current
            else:
                current.link[index] = TrieNode()
                current.link[index].previous = current
                current = current.link[index]
                if is_first:
                    current.first_str = True
                 
            self.recursive_insert_aux(current, i+1, is_first, key, data)

"""
The function to round a floating point correctly.

:Input:
    n: A floating point to be rounded.

:Return: An integer after rounding the given input.

:Time Complexity: O(1) as it is only performing number comparison and arithmetic operations.

:Aux Space Complexity: O(1) as no extra space is created.
"""
def safeRound(n):
    if n % 1 >= 0.5:
        n = n//1 + 1
    else:
        n = n//1
    return int(n)

"""
Builds a suffix tree from the given inputs and returns their longest common substring, along with the similarity scores of the two.

:Input:
    submission1: The first string.
    submission2: The second string.

:Return: [longest_common_substring, percentage1, percentage2]
    longest_common_substring: The longest common substring of the two inputs.
    percentage1: An integer denoting the similarity score of the first input.
    percentage2: An integer denoting the similarity score of the second input.

:Time complexity: O(N^2 + M^2) where N is the length of the first input, and M is the length of the second input. Generating the substrings
of the first input is in O(N) time, and each insertion is in O(N) time, adding up to O(N)*O(N) = O(N^2) time. Similarly for the second input, 
generating the substrings is in O(M) time, and each insertion is in O(M) time, adding up to O(M)*O(M) = O(M^2) time. Totalling up both we get
an overall time complexity of O(N^2 + M^2) time. 
Since we are already keeping track of the longest common substring during each insert, we 
can search for the result in O(1) time. 
Calculating the similarity score requires O(N+M) time, since we have to obtain the length of both strings and perform calculation.

:Aux space complexity: O(N^2 + M^2) where N is the length of the first input, and M is the length of the second input. Since each call to
insert a suffix requires an auxiliary space complexity of O(N)/O(M), and N suffixes are generated for the first input, M suffixes are 
generated for the second input, a total of O(N^2 + M^2) auxiliary space is needed at worst case.
"""
def compare_subs(submission1, submission2):
    t = Trie()

    for i in range(len(submission1)):
        substr = submission1[i:]
        t.recursive_insert(key=substr, is_first = True)

    for i in range(len(submission2)):
        substr = submission2[i:]
        t.recursive_insert(key=substr, is_first = False)

    percentage1 = safeRound(len(t.longest_common_substring)/len(submission1) * 100)
    percentage2 = safeRound(len(t.longest_common_substring)/len(submission2) * 100)

    return [t.longest_common_substring, percentage1, percentage2]



