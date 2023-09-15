n = 100
G = set(range(n+1))
S = {1,2,4,8,16,32,64}

P = set()
N = set()

while G:
    P = P.union({min(G)})

    for s in S:
        for p in P:
            value = p + s
            if value <= n:
                N = N.union({p + s})

    G = G - P - N

print(P)
print(N)

if n in P:
    print("Second")
else:
    print("First")
