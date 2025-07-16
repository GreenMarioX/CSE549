# compute floor(log2(x)) for x = 1 to n in O(n)
# returns a list where log_table[x] = floor(log2(x))
def build_log_table(n):
    log_table = [0] * (n + 1)
    for i in range(2, n + 1):
        log_table[i] = log_table[i // 2] + 1
    return log_table

# build KMR arrays for string T in O(nlogn)
# returns a 2d list where kmr_array[k][i] is rank of substring T[i..i+2^k]
def build_kmr(T, log_array):
    n = len(T)
    max_log = log_array[n]

    # 2D array with dimension (max_log+1) x n
    # kmr_array[k][i] represents rank of the substring from i with length 2^k
    kmr_array = [[0] * n for m in range(max_log + 1)]

    # k = 0, rank of a single character
    for i in range(n):
        kmr_array[0][i] = ord(T[i]) - ord('a')  # map a..z to 0..25

    # temp array for sorting
    temp = [((0, 0), 0)] * n
    # get ranks for substrings of lengths 2^k by doubling the length each iteration
    length, k = 1, 0
    while length < n:
        # creating pairs (current rank, next rank) for each index.
        for i in range(n):
            temp[i] = ((kmr_array[k][i], kmr_array[k][i + length] if i + length < n else -1), i)

        # sort indices by the pair (first, second).
        temp.sort(key=lambda x: x[0])

        # assign new ranks for A[k+1] using sorted order
        new_rank = 0
        kmr_array[k + 1][temp[0][1]] = 0
        for i in range(1, n):
            # if pair differs from the previous, increase rank
            if temp[i][0] != temp[i - 1][0]:
                new_rank += 1
            kmr_array[k + 1][temp[i][1]] = new_rank
        k += 1
        length *= 2
    return kmr_array

# compare T[i..i+L) and T[j..j+L) in O(1) using KMR array
# returns True is equal, false if not
# params: KMR array, log table, i and j (starting indicies), length (substring lengths to compare), n (total T length)
def substr_equal(KMR_array, log_array, i, j, length, n):
    # two empty substrings -> True or identical starting positons -> True
    if length == 0 or i == j:
        return True
    # bad counts -> False
    if i + length > n or j + length > n:
        return False

    # find largest power of 2 that is <= L.
    k = log_array[length]
    p = 2 ** k

    # compare rank of the first 2^k block.
    if KMR_array[k][i] != KMR_array[k][j]:
        return False
    # compare rank of the last 2^k block.
    if KMR_array[k][i + length - p] != KMR_array[k][j + length - p]:
        return False
    return True


# read from "in.txt"
with open("in.txt", "r") as f:
    T = f.readline().strip()
    q = int(f.readline().strip())
    queries = []
    for m in range(q):
        line = f.readline().strip()
        i, j, length = map(int, line.split())
        queries.append((i, j, length))

n = len(T)
# create logarithm table for KMR and queries
log_array = build_log_table(n)
# build the KMR data structure
A = build_kmr(T, log_array)

# process each query and output
with open("out.txt", "w") as out:
    for (i, j, L) in queries:
        i -= 1
        j -= 1
        # compare substrings
        if substr_equal(A, log_array, i, j, L, n):
            out.write("YES\n")
        else:
            out.write("NO\n")
