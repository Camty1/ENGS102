# Define parameters of game
n = 46
G = set(range(n+1))
S = {1,3,6}

# Initialize P and N sets
P = set()
N = set()

# Go through until every position in G has been added to either P or N
while G:
    # Put the smallest value left in G into P, as this can only go to N, as it would have otherwise been put in N by smaller P values
    P = P.union({min(G)})
    
    # For all values p in P, there exists a value n in N and a value s in S such that n - s = p
    for s in S:
        for p in P:
            value = p + s
            if value <= n:
                N = N.union({p + s})
    
    # Remove values in P and N from G
    G = G - P - N

# Print P and N sets
print("P set: ")
print(sorted(P))
print("N set: ")
print(sorted(N))

# Determine whether to play first or second based on whether n (the number of coins) is in P or N
if n in P:
    print("Play second to win.")
else:
    print("Play first to win.")
