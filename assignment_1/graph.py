def mex(values):
    i = 0
    while i in values:
        i = i+1
    return i

class Graph():
        
    def __init__(self):
        self.vertices = dict()
        self.g_function = dict()

    def add_vertex(self, vertex):
        if not vertex in self.vertices:
            self.vertices[vertex] = []
            self.g_function[vertex] = -1

    def add_edge(self, vertex_1, vertex_2):
        if not vertex_1 in self.vertices:
            self.add_vertex(vertex_1)

        if not vertex_2 in self.vertices:
            self.add_vertex(vertex_2)
        if not vertex_2 in self.vertices[vertex_1]:
            self.vertices[vertex_1].append(vertex_2)

    def reverse_graph(self):
        G = Graph()
        
        for v_1 in self.vertices:
            for v_2 in self.vertices[v_1]:
                G.add_edge(v_2, v_1)
    
        return G

    def print_graph(self):
        print(self.vertices)
        print(self.g_function)

    def calculate_g_function(self):
        queue = []
        G_rev = self.reverse_graph()

        [_, _, _, last] = G_rev.DFS(G_rev.vertices)

        top_order = [value[0] for value in sorted(last.items(), key=lambda item: item[1], reverse=True)]

        for v in top_order:
            if self.vertices[v] == []:
                self.g_function[v] = 0
            else:
                values = []
                for neighbor in self.vertices[v]:
                    values.append(self.g_function[neighbor])
                self.g_function[v] = mex(values)
        
    def DFS(self, vertices, visited=-1, t=-1, first=-1, last=-1):
        if visited == -1 or t == -1 or first == -1 or last == -1:
            visited = {}
            first = {}
            last = {}
            t = 0
            for v in self.vertices:
                visited[v] = 0
                first[v] = 0
                last[v] = 0
            
        if len(vertices) == 1:
            vertex = vertices[0]
            t = t + 1
            first[vertex] = t
            visited[vertex] = 1
            for v in self.vertices[vertex]:
                if visited[v] == 0:
                    [visited, t, first, last] = self.DFS([v], visited, t, first, last)

            t = t + 1
            last[vertex] = t

        else:
            for v in vertices:
                if visited[v] == 0:
                    [visited, t, first, last] = self.DFS([v], visited, t, first, last)

        return [visited, t, first, last]
if __name__ == '__main__':
    G = Graph()

    G.add_edge(0, 2)
    G.add_edge(0, 1)
    G.add_edge(1, 2)
    G.add_edge(2, 3)
    G.add_edge(3, 4)
    G.add_edge(2,5)

    G.calculate_g_function()

    G.print_graph()


