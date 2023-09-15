import random
import math

def nim_sum(piles):
    nim_sim = 0
    for p in piles:
        nim_sim = nim_sim ^ p

    return nim_sim

def nim_player(piles):
    # Convert to a list to allow chips to be removed from the piles
    piles = list(piles)

    # Get nim sum of game
    current_nim_sum = nim_sum(piles)

    # If nim_sum == 0, then game is in a P position so make a random move
    if current_nim_sum == 0:
        index = random.randint(0, len(piles)-1)
        while (piles[index] == 0):
            index = random.randint(0, len(piles)-1)
        chips = random.randint(1, piles[index])
        print("No winning move, taking", str(chips), "chips from pile", str(index+1))
        piles[index] -= chips
    # nim_sum != 0 therefore game is in an N position.  Make a move that puts the opponent into a P position
    else:
        for i in range(len(piles)):
            pile_nim_sum = nim_sum((piles[i], current_nim_sum))
            if pile_nim_sum <= piles[i]:
                take_amount = piles[i] - pile_nim_sum
                print("Take", str(take_amount), "chips from pile", str(i+1))
                piles[i] -= take_amount
                break
    return tuple(piles)

if __name__ == "__main__":
    piles = (100, 100, 101, 50, 25, 100, 43)
    round = 0
    while not(piles == (0,0,0,0,0,0,0)):
        print("Round:", math.floor((round)/2) + 1, "Player:", round % 2 + 1)
        print(piles)
        piles = nim_player(piles)
        round += 1

    if round % 2 == 0:
        print("Player 2 wins!")
    else:
        print("Player 1 wins!")
