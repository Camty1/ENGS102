from graph import *
import math

# subtraction sets are as follows: 0 is standard, 1 is at least half, 2 is even if not all all if odd, and a set is a what you give it.  Can eiter specify by pile or just apply the rule to all piles at once

class Nim():

    def __init__(self, piles, subtraction_sets=0):

        assert all(elem > 0 for elem in piles), "All elements must be positive integers"
        self.piles = piles
        self.num_piles = len(piles)
        self.current_state = piles

        if isinstance(subtraction_sets, int):
            value = subtraction_sets
            subtraction_sets = []
            for x in piles:
                subtraction_sets.append(value)

        assert len(subtraction_sets) == self.num_piles

        self.subtraction_sets = tuple(subtraction_sets)

    def get_next_states(self, state=-1):
        if state == -1:
            state = self.current_state
        next_states = set()

        for pile_index in range(self.num_piles):

            pile_size = state[pile_index]
            if pile_size != 0:

                if self.subtraction_sets[pile_index] == 0:
                    subtraction_set = set(list(range(1, pile_size+1)))
                elif self.subtraction_sets[pile_index] == 1:
                    bottom_val = math.ceil(pile_size/2)
                    subtraction_set = set(list(range(bottom_val, pile_size+1)))
                elif self.subtraction_sets[pile_index] == 2:
                    if pile_size % 2 == 1:
                        subtraction_set = {pile_size}
                    else:
                        subtraction_set = set(list(range(2, pile_size+1, 2)))
                elif isinstance(self.subtraction_sets[pile_index], set):
                    subtraction_set = []
                    for s in self.subtraction_sets[pile_index]:
                        if s <= pile_size:
                            subtraction_set.append(s)

                    subtraction_set = set(subtraction_set)

                state = list(state)
                for s in subtraction_set:
                    new_state = state[:]
                    new_state[pile_index] = state[pile_index] - s
                    new_state = tuple(new_state)
                    next_states.add(new_state)

        return next_states

    def print_game(self):
        print(self.piles)
        print(self.num_piles)
        print(self.current_state)
        print(self.subtraction_sets)

    def generate_graph(self):
        G = Graph()
        queue = []
        visited = set()
        queue.append(self.piles)
        visited.add(self.piles)

        while queue:
            front_of_queue = queue.pop(0)
            next_states = self.get_next_states(front_of_queue)
            
            for state in next_states:
                G.add_edge(front_of_queue, state)
                if not state in visited:
                    queue.append(state)
                    visited.add(state)

        G.calculate_g_function()
        return G

class Kayles():

    def __init__(self, num_pins):
        
        self.num_pins = num_pins
        self.pins = []
        for i in range(num_pins):
            self.pins.append(1)

        self.pins = tuple(self.pins)
        self.current_state = self.pins

    def get_next_states(self, state=-1):
        if state == -1:
            state = self.current_state

        next_states = set()
        state = list(state) 
        for i in range(self.num_pins-1):
            if state[i] == 1:
                new_state = state[:]
                new_state[i] = 0
                next_states.add(tuple(new_state))
                if state[i+1] == 1:
                    new_state[i+1] = 0
                    next_states.add(tuple(new_state))

        if state[-1] == 1:
            new_state = state[:]
            new_state[-1] = 0
            next_states.add(tuple(new_state))

        return next_states

    def print_game(self):
        print("Num pins:", str(self.num_pins))
        print(str(self.pins))

    def generate_graph(self):
        G = Graph()
        queue = []
        visited = set()
        queue.append(self.pins)
        visited.add(self.pins)

        while queue:
            current_state = queue.pop(0)
            next_states = self.get_next_states(current_state)

            for s in next_states:
                G.add_edge(current_state, s)
                if not s in visited:
                    queue.append(s)
                    visited.add(s)
        
        G.calculate_g_function()
        return G

class Dawson():

    def __init__(self, num_boxes):

        self.num_boxes = num_boxes
        self.boxes = []

        for i in range(num_boxes):
            self.boxes.append(1)

        self.boxes = tuple(self.boxes)
        self.current_state = self.boxes

    def get_next_states(self, state=-1):
        if state == -1:
            state = self.current_state

        next_states = set()
        state = list(state)
        for i in range(self.num_boxes):
            if state[i] == 1:
                new_state = state[:]
                new_state[i] = 0
                if i > 0:
                    new_state[i-1] = 0
                if i < self.num_boxes - 1:
                    new_state[i+1] = 0
                next_states.add(tuple(new_state))

        return next_states
    
    def generate_graph(self):
        G = Graph()
        queue = []
        visited = set()
        queue.append(self.boxes)
        visited.add(self.boxes)

        while queue:
            current_state = queue.pop(0)
            next_states = self.get_next_states(current_state)

            for s in next_states:
                G.add_edge(current_state, s)
                if not s in visited:
                    queue.append(s)
                    visited.add(s)
        
        G.calculate_g_function()
        return G

class Grundy():

    def __init__(self, pile_size):
        self.piles = (pile_size,)
        self.current_state = self.piles

    def get_next_states(self, state=-1):
        if state == -1:
            state = self.current_state
        
        next_states = set()
        state = list(state)

        for pile in range(len(state)):
            pile_size = state[pile]
            if pile_size > 2:
                for move in range(1,math.ceil(pile_size/2)):
                    new_state = state[:]
                    new_state[pile] -= move
                    new_state.append(move)
                    next_states.add(tuple(sorted(new_state))) 

        return next_states
        
    def generate_graph(self):
        G = Graph()
        queue = []
        visited = set()
        queue.append(self.piles)
        visited.add(self.piles)

        while queue:
            current_state = queue.pop(0)
            next_states = self.get_next_states(current_state)

            for s in next_states:
                G.add_edge(current_state, s)
                if not s in visited:
                    queue.append(s)
                    visited.add(s)
        
        G.calculate_g_function()
        return G

if __name__ == '__main__':
    game = Grundy(6)

    game_graph = game.generate_graph()
    game_graph.visualize()
    
#    game2 = Kayles(10)
#
#    game2_graph = game2.generate_graph()
#
#    game2_graph.visualize()
    #game_graph.print_graph()

#    P = []
#    N = []
#
#    for v in game_graph.vertices:
#        if game_graph.g_function[v] == 0:
#            P.append(v)
#        else:
#            N.append(v)
#    print("")
#    print(sorted(N))
#    print("")
#    print(sorted(P))
#
#    print((100,100,100) in P)


