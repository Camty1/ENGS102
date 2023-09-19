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

        for v in self.vertices:
            if self.vertices[v] == []:
                self.g_function[v] = 0
                queue.append(v)

        while queue:
            print(queue)
            current_v = queue.pop(0)
            
            values = []
            
            for v in self.vertices[current_v]:
                value = self.g_function[v]
                if value == -1:
                    queue.append(v)
                values.append(value)

            if -1 in values:
                queue.append(current_v)

            else:
                self.g_function[current_v] = mex(values)
                for v in G_rev.vertices[current_v]:
                    queue.append(v)

if __name__ == '__main__':
    G = Graph()

    G.add_edge(0, 2)
    G.add_edge(0, 1)
    G.add_edge(1, 2)
    G.add_edge(2, 3)
    G.add_edge(3, 4)

    G.print_graph()

    G.calculate_g_function()

    G.print_graph()

