import random
import string

# computes the Longest Prefix Suffix (pi) array for the pattern.
# this is derived from the Version 2 from the slides with some modifications
def compute_pi(pattern):
    pi = [0] * len(pattern)
    b = 0  # length of the previous longest prefix suffix
    for i in range(1, len(pattern)):
        while b > 0 and pattern[i] != pattern[b]:
            b = pi[b - 1]  # backtrack to the prev pi value
        if pattern[i] == pattern[b]:
            b += 1
            pi[i] = b
    return pi

# performs kmp algorithm.
# this algorithm is based on the pseudocode provided but modified to have one less while loop.
def kmp_search(text, pattern):
    if not pattern:
        return list(range(len(text) + 1))

    lps = compute_pi(pattern)
    occurrences = []  # store indices

    i, l = 0, 0  # pointers for text and pattern

    while i < len(text):
        if text[i] == pattern[l]:
            i += 1
            l += 1
            if l == len(pattern):  # full pattern match
                occurrences.append(i - l)
                l = lps[l - 1]
        else:
            if l > 0:
                l = lps[l - 1]
            else:
                i += 1
    return occurrences

# naive method, returns array of indices
def naive_search(text, pattern):
    occurrences = [] # stores indices
    n, m = len(text), len(pattern)
    for start in range(n - m + 1):
        match = True
        for j in range(m):
            if text[start + j] != pattern[j]:
                match = False
                break
        if match:
            occurrences.append(start)
    return occurrences

# this function is just to create random strings using the alphabet
def generate_random_string(length, alphabet):
    return ''.join(random.choice(alphabet) for i in range(length))

# this function is for testing my kmp vs naive
# give it 3 params: number of tests, max length of text, and alphabet size
# will terminate test on mismatch!
def run_test(num_tests=10000000, max_length=10000, alphabet_size=4):
    alphabet = string.ascii_lowercase[:alphabet_size] # build alphabet

    for i in range(num_tests):
        text_len = random.randint(0, max_length)
        pattern_len = random.randint(2, 8)
        text = generate_random_string(text_len, alphabet)
        pattern = generate_random_string(pattern_len, alphabet)
        kmp_result = kmp_search(text, pattern)
        naive_result = naive_search(text, pattern)

        # comparing Results
        if kmp_result != naive_result:
            print("Mismatch found!")
            print("Text:    ", text)
            print("Pattern: ", pattern)
            print("KMP:     ", kmp_result)
            print("Naive:   ", naive_result)
            return  # Stop on first mismatch

        print("text: ", text)
        print("pattern: ", pattern)
        print("kmp_result: ", kmp_result)
        print("naive_result: ", naive_result)
        print("------------------------")

    print("Test Passed!")

run_test(1000, 10000, 4)

