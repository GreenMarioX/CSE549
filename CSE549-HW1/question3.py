
# read from 'in.txt'
with open('in.txt', 'r') as f:
    T = f.readline()  # Long string
    k = int(f.readline())  # Query Amount
    queries = []
    for l in range(k):
        line = f.readline()
        i, j, length = map(int, line.split())
        queries.append((i, j, length))

# parameters
MOD = 1000000021 # THIS IS q
BASE = 257 # THIS IS r
n = len(T)
H = [0] * (n + 1) # Prefix hash array

# precompute powers of BASE
# R[i] = BASE^i mod MOD
R = [0] * (n + 1)
R[0] = 1
for i in range(1, n + 1):
    R[i] = (R[i - 1] * BASE) % MOD

# char to integers
for i in range(1, n + 1):
    H[i] = (H[i - 1] * BASE + (ord(T[i - 1]) - ord('a') + 1)) % MOD

# get the hash of substring TIME: O(1)
def get_hash(a, b):
    result = H[b] - (H[a - 1] * R[b - a + 1] % MOD) # defined in part A
    return result % MOD

# process each query and output
with open('out.txt', 'w') as out:
    for (i, j, length) in queries:
        if length == 0: # len == 0 should match
            out.write("YES\n")
            continue

        # calculate T[i..i+length-1] and T[j..j+length-1] then compare
        hash1 = get_hash(i, i + length - 1)
        hash2 = get_hash(j, j + length - 1)

        if hash1 == hash2:
            out.write("YES\n")
        else:
            out.write("NO\n")