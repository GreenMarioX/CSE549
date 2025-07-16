# this function is from Part A. Refer to Part A for comments
def edit_distance(X, Y):
    m, n = len(X), len(Y)
    row = list(range(n + 1))
    for i in range(1, m + 1):
        diag = row[0]
        row[0] = i
        for j in range(1, n + 1):
            up = row[j]
            cost = 0 if X[i - 1] == Y[j - 1] else 1
            row[j] = min(up + 1, row[j - 1] + 1, diag + cost)
            diag = up
    return row[n]

# read from "in.txt"
with open("in.txt", "r") as f:
    T = f.readline().strip()
    q = int(f.readline().strip())
    queries = []
    for _ in range(q):
        line = f.readline().strip()
        i, j, length = map(int, line.split())
        queries.append((i, j, length))

# get each substring and calculate the edit distance
results = []
for i, j, length in queries:
    X = T[i - 1: i - 1 + length]
    Y = T[j - 1: j - 1 + length]
    dist = edit_distance(X, Y)
    results.append(str(dist))

# write to out.txt
with open("out.txt", "w") as f:
    f.write("\n".join(results) + "\n")

