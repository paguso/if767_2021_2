# 04/04/2022 Construção Suffix Array

from math import ceil, log2

"""
Sigma = { A, B, C, D, E}
        0        1         2         3          4          5         6

        A        E         A         E          C          B         D
        _        _         _         _          _          _         _
P0      0        4         0         4          2          1         3
        __________
        (0,4)    ____________
                 (4,0)     ___________ 
                           (0,4)     ____________
                                     (4,2)      ____________
                                                (2,1)      ___________
                                                           (1,3)     ___________
                                                                     (3,-1)

pairs   (0,4,0)  (4,0,1)   (0,4,2)   (4,2,3)    (2,1,4)    (1,3,5)   (3,-1,6)
        (0,4,0)  (0,4,2)   (1,3,5)   (2,1,4)    (3,-1,6)   (4,0,1)   (4,2,3)
P1      0        4         0         5          2          1         3 
        -------------------------------
        (0,0)    (4,5)     (0,2)     (5,1)      (2,3)      (1,-1)    (3,-1)
P2      0        5          1        6          3          2         4
P3      0        5          1        6          3          2         4

SA      0        2          5        4          6          1         3
"""

def sort_letters(txt, ab):
    return [ab.index(c) for c in txt]


def build_P(txt, ab):
    n = len(txt)
    P = []
    P.append(sort_letters(txt, ab))
    k = 1
    t = int(ceil(log2(n)))
    while k <= t:
        l = 2**(k-1)
        pairs = [(P[k-1][i], P[k-1][i+l] if i+l<n else -1, i) for i in range(n)]
        pairs.sort()
        Pk = n * [0]
        order = 0
        Pk[pairs[0][2]] = order
        for i in range(1,n):
            if pairs[i-1][:2] != pairs[i][:2]:
                order += 1
            Pk[pairs[i][2]] = order
        P.append(Pk)
        k += 1
    return P

"""
SA[P[i]] = i
"""
def build_sarr(P):
    n = len(P)
    sa = n * [0]
    for i in range(n):
        sa[P[i]] = i
    return sa


"""
computes lcp(txt[i:], txt[j:]) 
"""
def lcp(P, i, j):
    n = len(P[0])
    assert(i<n and j<n)
    if i == j:
        return n-i
    else:
        k = len(P)-1
        lcp = 0
        while k >= 0 and i < n and j < n:
            l = 2**k 
            if P[k][i] == P[k][j]: # txt[i:i+l]==txt[j:j+l]
                lcp += l
                i += l
                j += l 
            k -= 1
        return lcp


def test():
    txt = "aeaeabd"
    ab  = "abcde"
    P = build_P(txt, ab)
    print("P=",P)
    sa = build_sarr(P[-1])
    print("sa=",sa)
    for i in range(len(txt)):
        print("%dth suffix: %s"%(i, txt[sa[i]:]))
    i, j = 0, 2
    l = lcp(P, i, j)
    print("lcp(%s,%s)=%d"%(txt[i:], txt[j:], l))



if __name__ == "__main__":
    test()