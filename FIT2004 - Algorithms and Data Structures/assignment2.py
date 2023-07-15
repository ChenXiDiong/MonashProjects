import math

class RoadGraph:
    def __init__(self, roads, cafes):
        """
        Initialises the RoadGraph with the given locations and roads using an adjacency list.

        :Input:
            roads: A list of possible roads (u,v,w), where u = start location, v = end location, w = time taken to travel.
            cafes: A list of cafes (c, w), where c = location of cafe, w = waiting time for a coffee.

        :Postcondition: A list of vertices each containing their respective list of edges is stored in the 'vertices' attribute.

        :Time complexity: O(V+E) where V is the number of unique locations, E is the number of roads given. We need to set up every vertex which is in O(V), and add_edges() appends all edges 
        to their respective vertices which is in O(E), totalling up to a complexity of O(V) + O(E) = O(V+E). Setting up the reversed graph is running the same algorithm, therefore the overall
        complexity is O(2(V+E)) which is still O(V+E).

        :Aux space complexity: O(V+E) where V is the number of unique locations, E is the number of roads given. Two lists of the vertices is created with size V, each containing an adjacency list
        storing the outgoing edges. Totalling up to a space complexity of 2 * O(V) + O(E) = O(2(V+E)) = O(V+E).
        """
        #locations = vertices
        n_locations = roads[0][0]
        for road in roads:
            if road[0] > n_locations:
                n_locations = road[0]
            if road[1] > n_locations:
                n_locations = road[1]

        self.vertices = [None] * (n_locations+1)
        for i in range(n_locations+1):
            self.vertices[i] = Vertex(i)

        #roads = edges
        self.add_edges(roads)  

        #adding in cafes
        self.cafes = cafes

        #for performing dijkstra on a reversed graph
        self.rev_vertices = [None] * (n_locations+1)
        for i in range(n_locations+1):
            self.rev_vertices[i] = Vertex(i)

        self.add_rev_edges(roads)  
        

         
    def routing(self, start, end):
        """
        Dijkstra's Algorithm implementation referenced from Dr. Wern Han (Ian) Lim's live programming session.

        Finds the shortest path with minimum wait time, going through a cafe from start to end. Performs Dijkstra's Algorithm to determine the shortest path taken from the closest cafe to start,
        and once more to determine the shortest path taken from the closest cafe to end, and returns the shorter path.

        :Input:
            start: A non-negative integer indicating the starting location.
            end: A non-negative integer indicating the ending location.

        :Return: A list of vertices indicating the route to be taken.

        :Time complexity: O(ElogV) where E is the number of edges in the RoadGraph, V is the number of vertices in the RoadGraph. Adding and Serving the MinHeap is in O(logV) time, and we perform
        this for all edges, which is in O(E) * O(logV) = O(ElogV). Determining the shortest route is in O(V) since the number of cafes is at most V, and the worst case of reconstructing the path
        is when we go through all edges, which is in O(E), both don't affect the overall time complexity. 

        :Auxiliary space complexity: O(V+E) where E is the number of edges in the RoadGraph, V is the number of vertices in the RoadGraph. The MinHeap has size O(V), and the result array containing
        the solution has at most O(E) space, which totals up to a space complexity of O(V+E).
        """
        startv = self.vertices[start]
        endv = self.rev_vertices[end]
        self.reset()
        startv.distance = 0
        startv.discovered = True
        discoveryqueue = MinHeap(len(self.vertices))
        discoveryqueue.add(startv.distance, startv)
        while len(discoveryqueue) > 0: 
            u = discoveryqueue.get_min()[1] #O(logV)
            u.visited = True #u is visited
            for edge in u.edges: #O(V) since for any vertex u, it can only have at most v-1 neighbours 
                v = edge.v
                if v.discovered == False: #means distance is still infinity
                    v.distance = u.distance + edge.w 
                    v.previous = u
                    v.discovered = True #v has been discovered and added to the Qeuue
                    discoveryqueue.add(v.distance, v)
                elif v.visited == False:   
                #if I find a shorter distance, update
                    if v.distance > u.distance + edge.w:
                        #update distance
                        v.distance = u.distance + edge.w
                        v.previous = u
                        #update heap
                        discoveryqueue.update(v.distance, v) #add vertex v into heap with distance = v.distance(smaller) O(logV)
        

        #2nd dijkstra
        startv2 = self.rev_vertices[end]
        startv2.distance = 0
        startv2.discovered = True
        discoveryqueue = MinHeap(len(self.rev_vertices))
        discoveryqueue.add(startv2.distance, startv2)
        while len(discoveryqueue) > 0: 
            u = discoveryqueue.get_min()[1] #O(logV)
            u.visited = True #u is visited
            for edge in u.edges: #O(V) since for any vertex u, it can only have at most v-1 neighbours 
                v = edge.v
                if v.discovered == False: #means distance is still infinity
                    v.distance = u.distance + edge.w 
                    
                    v.previous = u
                    v.discovered = True #v has been discovered and added to the Qeuue
                    discoveryqueue.add(v.distance, v)
                elif v.visited == False:   
                #if I find a shorter distance, update
                    if v.distance > u.distance + edge.w:
                        
                        #update distance
                        v.distance = u.distance + edge.w
                        v.previous = u
                        #update heap
                        discoveryqueue.update(v.distance, v) #add vertex v into heap with distance = v.distance(smaller) O(logV)
        
        #reconstructing the solution
        curr_min = math.inf
        res = []
        start_cafe = None
        end_cafe = None
        for cafe in self.cafes:
            v1 = self.vertices[cafe[0]]
            v2 = self.rev_vertices[cafe[0]]
            if v1.distance + v2.distance + cafe[1] < curr_min:
                curr_min = v1.distance + v2.distance + cafe[1]
                start_cafe = v1
                end_cafe = v2
        if start_cafe == None or end_cafe == None: 
            return None
        curr_v = start_cafe
        while curr_v != startv:
            res.append(curr_v.id)
            curr_v = curr_v.previous
        res.append(curr_v.id)
        res.reverse()

        curr_v = end_cafe
        while curr_v != endv:
            curr_v = curr_v.previous
            res.append(curr_v.id)
            

        return res
        
        
        

    def __str__(self):
        retstr = ""
        for vertex in self.vertices:
            retstr = retstr + "Location " + str(vertex) + "\n"
            if vertex.coffee != math.inf:
                retstr = retstr + "Wait time " + str(vertex.coffee) + "\n"
        return retstr

    def reset(self):
        """
        Resets the graph to its initial state.

        :Postcondition: The graph has all vertices reset back to their initial states.

        :Time complexity: O(V) where V is the number of vertices. We go through each vertex and reset its state.

        :Auxiliary space complexity: O(1) as no extra space is created.
        """
        for vertex in self.vertices:
            vertex.distance = math.inf
            vertex.visited = False
            vertex.discovered = False
            vertex.previous = None

        for vertex in self.rev_vertices:
            vertex.distance = math.inf
            vertex.visited = False
            vertex.discovered = False
            vertex.previous = None
        


    def add_edges(self, edges):
        """
        Appends edges to their respective vertices.

        :Input:
            edges: A list of edges (u,v,w), where u = start vertex, v = end vertex, w = weight of edge.
       
        :Postcondition: Each vertex has its outgoing edges stored in its adjacency list.

        :Time complexity: O(E) where E is the number of edges given.

        :Aux space complexity: O(1) as no extra space is required.
        """
        for edge in edges:
            u = self.vertices[edge[0]]
            v = self.vertices[edge[1]]
            w = edge[2]
            #add v to u
            current_edge = Edge(u,v,w)
            current_vertex = self.vertices[u.id]
            current_vertex.add_edge(current_edge)

    def add_rev_edges(self, edges):
        """
        Appends reversed edges to their respective vertices.

        :Input:
            edges: A list of edges (u,v,w), where u = original start vertex, v = original end vertex, w = weight of edge.
       
        :Postcondition: Each vertex has its outgoing edges stored in its adjacency list.

        :Time complexity: O(E) where E is the number of edges given.

        :Aux space complexity: O(1) as no extra space is required.
        """
        for edge in edges:
            v = self.rev_vertices[edge[0]]
            u = self.rev_vertices[edge[1]]
            w = edge[2]
            #add v to u
            current_edge = Edge(u,v,w)
            current_vertex = self.rev_vertices[u.id]
            current_vertex.add_edge(current_edge)
            

class Edge:
    def __init__(self,u,v,w):
        self.u = u
        self.v = v
        self.w = w

    def __str__(self):
        retstr = "u: " + str(self.u) + ", v: " + str(self.v) + ", w: " + str(self.w)  
        return retstr


class Vertex:
    def __init__(self, id):
        self.id = id
        self.edges = []
        self.distance = math.inf
        self.visited = False
        self.discovered = False
        self.previous = None
        self.coffee = math.inf

    def __str__(self):
        retstr = "Vertex" + str(self.id)
        return retstr

    def add_edge(self, edge):
        self.edges.append(edge)


class MinHeap:
    """
    Adapted MaxHeap class from FIT1008 code and reworked into MinHeap.
    """
    def __init__(self, n_vertices):
        self.heap = [None]
        self.length = 0
        self.index = [0] * n_vertices
        for i in range(n_vertices):
            self.index[i] = i #index of list = vertex, value = current index in the MinHeap

    def __len__(self):
        return self.length

    def __str__(self):
        return str(self.heap)

    def is_empty(self):
        return self.length == 0

    def smallest_child(self, k):
        """
        Returns the index of k's child with smallest value.

        :Input:
            k: An integer representing the index of the parent.

        :Precondition: 1 <= k <= self.length // 2

        :Return: The index of the smallest child of k.

        :Time complexity: O(1). We only need to compare the children of a node once.

        :Auxiliary space complexity: O(1) as no extra space is created. 
        """
        if 2*k == self.length or self.heap[2*k][0] < self.heap[2*k+1][0]:
            return 2*k
        else:
            return 2*k+1
    
    def rise(self, k):
        """
        Rise element at index k to its correct position.

        :Input:
            k: An integer representing the index of the item.

        :Precondition: 1 <= k <= self.length

        :Postcondition: The element at index k is at its correct position.

        :Time complexity: O(logV) where V is the number of nodes in the MinHeap. We only need to traverse at most half the MinHeap.

        :Auxiliary space complexity: O(1) as no extra space is created.
        """
        item = self.heap[k] 
        curr_index = item[1].id
        while k > 1 and item[0] < self.heap[k // 2][0]:
            parent_index = self.heap[k // 2][1].id #the index of the parent
            self.heap[k] = self.heap[k // 2]
            self.index[parent_index] = k
            k = k // 2
        self.heap[k] = item
        self.index[curr_index] = k

    def sink(self, k):
        """ 
        Make the element at index k sink to the correct position.

        :Input:
            k: An integer representing the index of the item.

        :Precondition: 1 <= k <= self.length

        :Postcondition: The element at index k is at its correct position.

        :Time complexity: O(logV) where V is the number of nodes in the MinHeap. We only need to traverse at most half the MinHeap.

        :Auxiliary space complexity: O(1) as no extra space is created.
        """
        item = self.heap[k]
        curr_index = item[1].id
        while 2*k <= self.length and item[0] > self.heap[self.smallest_child(k)][0]:
            child_index = self.heap[self.smallest_child(k)][1].id
            self.heap[k] = self.heap[self.smallest_child(k)]
            self.index[child_index] = k
            k = self.smallest_child(k)
    
        self.heap[k] = item
        self.index[curr_index] = k

    def add(self, key, item):
        """
        Adds an element to the MinHeap and moving it to its correct position.

        :Input:
            key: An integer representing the key for comparison.
            item: The item to be inserted into the MinHeap.

        :Postcondition: The key-item pair is added to the MinHeap and is at its correct position.

        :Time complexity: O(logV) where V is the number of nodes in the MinHeap. The call to the rise() function is the dominant line, which runs in O(logV) time.

        :Auxiliary space complexity: O(1), we only create 1 extra space for putting the new item into the heap.
        """
        self.length += 1
        self.heap += [None]
        self.heap[self.length] = (key, item)
        self.rise(self.length)


    def get_min(self):
        """
        Removes the minimum element from the MinHeap, returning it.

        :Precondition: Heap is non-empty.

        :Return: The minimum element of the MinHeap.

        :Time complexity: O(logV) where V is the number of nodes in the MinHeap. The dominant line is the call to the sink() function which runs in O(logV) time.

        :Auxiliary space complexity: O(1) as no extra space is created.
        """
        curr_min = self.heap[1]
        self.length -= 1
        if self.length > 0:
            index = self.heap[self.length+1][1].id
            self.heap[1] = self.heap[self.length+1]
            self.index[index] = 1
            self.sink(1)
        self.heap.pop()
        return curr_min

    def update(self, key, item):
        """
        Updates the item in the heap with the key and performs a rise.

        :Input:
            key: An integer representing the key for comparison.
            item: The item to be inserted into the MinHeap.

        :Postcondition: The key is updated and the key-item pair is in its correct position.

        :Time complexity: O(logV) where V is the number of nodes in the MinHeap. The call to the rise() function is the dominant line, which runs in O(logV) time.

        :Auxiliary space complexity: O(1) as no extra space is created.
        """
        index = self.index[item.id]
        self.heap[index] = (key,self.heap[index][1])
        self.rise(index)


#===============================================================Question 2=========================================================================
def optimalRoute(routes, start, finish):
    """
    Given the start and finish position, uses Bellman-Ford algorithm to find the optimal route to obtain maximum score. 

    :Input:
        routes: A list of possible downhill segments (u,v,w) where u = start position, v = end position, w = score obtained.
        start: An integer representing the start position.
        finish: An integer representing the finish position.

    :Output: A list of positions stating the route to take.

    :Time complexity: O(DP) where D is the number of downhill segments, P is the total number of intersection points. We always loop P-1 times over D edges, therefore the 
    overall time complexity is O(P) * O(D) = O(DP).

    :Aux space complexity: O(D) where D is the number of downhill segments. The size of memo and pred are both O(P), whereas the size of res is at most O(D), 
    totalling up to an auxiliary space complexity of O(D) + O(P) = O(D+P). Since P is always <= D, the overall auxiliary space complexity is O(D).
    """
    n = 0
    for route in routes:
        if route[0] > n:
            n = route[0]
        if route[1] > n:
            n = route[1]
    
    #initializing memo
    memo = [-math.inf] * (n+1)
    pred = [None] * (n+1)

    #base case- starting and ending on the same point has score 0.
    memo[finish] = 0

    for _ in range(len(routes)):
        for route in routes:
            u = route[1]
            v = route[0]
            w = route[2]
            if memo[v] < memo[u] + w:
                memo[v] = memo[u] + w
                pred[v] = u

    #reconstructing the solution
    res = []
    curr = start   
    while curr != finish:
        res.append(curr)
        curr = pred[curr]
        if curr == None:
            return None
        
    res.append(curr)
    

    return res





    
    
    