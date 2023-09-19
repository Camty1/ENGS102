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
        queue.append(self.piles)

        while queue:
            front_of_queue = queue.pop(0)
            next_states = self.get_next_states(front_of_queue)
            
            for state in next_states:
                G.add_edge(front_of_queue, state)
                if not state in queue:
                    queue.append(state)

        G.calculate_g_function()
        return G

if __name__ == '__main__':
    game = Nim(tuple([21]), tuple([{1,2,3}]))
    game.print_game()

    game_graph = game.generate_graph()

    game_graph.print_graph()

    P = []
    N = []

    for v in game_graph.vertices:
        if game_graph.g_function[v] == 0:
            P.append(v)
        else:
            N.append(v)

    print(sorted(P))
    print(sorted(N))


