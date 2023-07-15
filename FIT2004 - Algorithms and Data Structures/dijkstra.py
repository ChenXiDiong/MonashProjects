class Graph:
    def __init__(self, n_vertices):
        self.vertices = [None] * n_vertices
        for i in range(n_vertices):
            self.vertices[i] = Vertex(i)

    def __str__(self):
        retstr = ""
        for vertex in self.vertices:
            retstr = retstr + "Vertex " + str(vertex) + "\n"
        return retstr

    def reset(self):
        for vertex in self.vertices:
            vertex.distance = 0
            vertex.visited = False
            vertex.discovered = False
            vertex.previous = None

    def add_edges(self, edges, directed = True):
        for edge in edges:
            u = edge[0]
            v = edge[1]
            w = edge[2]
            #add v to u
            current_edge = Edge(u,v,w)
            current_vertex = self.vertices[u]
            current_vertex.add_edge(current_edge)
            if not directed: #if graph is undirected
                #add u to v
                current_edge = Edge(v,u,w)
                current_vertex = self.vertices[v]
                current_vertex.add_edge(current_edge)

    def dijkstra(self, source, target):
        """
        Performs dijkstra's algorithm to find shortest path from source to target. 
        """
        self.reset()
        source.distance = 0
        res = []
        discoveryqueue = MinHeap(len(self.vertices))
        discoveryqueue.add(source.distance, source)
        while len(discoveryqueue) > 0: 
            u = discoveryqueue.get_min()[1] #O(logV)
            u.visited = True #u is visited
            res.append(u.id)
            if u == target: #terminate early
                return
            for edge in u.edges: #O(V) since for any vertex u, it can only have at most v-1 neighbours 
                v = edge.v
                if v.discovered == False: #means distance is still infinity
                    v.distance = u.distance + edge.w 
                    v.previous = u
                    v.discovered = True #v has been discovered and added to the Qeuue
                    discoveryqueue.add(v.distance, v)
                # it is in heap, but not yet finalized
                elif v.visited == False:
                    #if I find a shorter distance, update
                    if v.distance > u.distance + edge.w:
                        #update distance
                        v.distance = u.distance + edge.w
                        v.previous = u
                        #update heap
                        discoveryqueue.update(v.distance, v) #add vertex v into heap with distance = v.distance(smaller) O(logV)

        return res


class Edge:
    def __init__(self,u,v,w):
        self.u = Vertex(u)
        self.v = Vertex(v)
        self.w = w

    def __str__(self):
        retstr = "u: " + str(self.u) + ", v: " + str(self.v) + ", w: " + str(self.w) 
        return retstr


class Vertex:
    def __init__(self, id):
        self.id = id
        self.edges = []
        self.distance = 0
        self.visited = False
        self.discovered = False
        self.previous = None

    def __str__(self):
        retstr = str(self.id)
        for edge in self.edges:
            retstr = retstr + "\n with edge" + str(edge)
        return retstr

    def add_edge(self, edge):
        self.edges.append(edge)

#%% MinHeap Class
class MinHeap:
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
        :pre: 1 <= k <= self.length // 2
        """
        if 2*k == self.length or self.heap[2*k][0] < self.heap[2*k+1][0]:
            return 2*k
        else:
            return 2*k+1
    
    def rise(self, k: int) -> None:
        """
        Rise element at index k to its correct position
        :pre: 1 <= k <= self.length
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
        """ Make the element at index k sink to the correct position """
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
        Swaps elements while rising
        """
        self.length += 1
        self.heap += [None]
        self.heap[self.length] = (key, item)
        self.rise(self.length)


    def get_min(self):
        """
        Removes the minimum element from the heap, returning it.
        :pre: Heap is non-empty.
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
        """
        index = self.index[item.id]
        self.heap[index][0] = key
        self.rise(index)


#%%
if __name__ == "__main__":
    #vertices
    #vertex id = 0..5
    total_vertices = 6
    mygraph = Graph(total_vertices)
    

    edges = []
    edges.append((3,1,5))  #u=3, v=1, w=5
    edges.append((1,2,1))
    edges.append((2,5,-888))
    edges.append((3,2,-5))
    mygraph.add_edges(edges, False)
    
    print(mygraph.dijkstra(mygraph.vertices[3],mygraph.vertices[1]))


    

# %%
