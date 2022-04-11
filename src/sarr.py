# 04/04/2022 Construção Suffix Array

# 11/04/2022 Busca exata com Suffix Arrays


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



def _fill_RL_lcp(txt, P, sa, Llcp, Rlcp, l, r):
    if (r-l) <= 1:
        return
    h = (l+r) // 2
    Llcp[h] = lcp(P, sa[l], sa[h])
    #print("Llcp[%d]==lcp(txt[%d:]=%s, txt[%d:]=%s)==%d"%(h,l,txt[sa[l]:],h,txt[sa[h]:],Llcp[h]))
    Rlcp[h] = lcp(P, sa[h], sa[r])
    #print("Rlcp[%d]==lcp(txt[%d:]=%s, txt[%d:]=%s)==%d"%(h,h,txt[sa[h]:],r,txt[sa[r]:],Rlcp[h]))
    _fill_RL_lcp(txt, P, sa, Llcp, Rlcp, l, h)
    _fill_RL_lcp(txt, P, sa, Llcp, Rlcp, h, r)




def fill_RL_lcp(txt, P, sa, Llcp, Rlcp):
    n = len(sa)
    _fill_RL_lcp(txt, P, sa, Llcp, Rlcp, 0, n-1)

"""
x : --------------------------
y : **********
n : |           |

compares 
x[:min(len(x),n)] to y[:min(len(y),n)]

x : -------------
y : **********
n : |           |
"""
def lex_leq(x, y, n):
    return x[:min(len(x),n)] <= y[:min(len(y),n)]



def lex_cmp(x, y):
    lcp = 0
    lx = len(x)
    ly = len(y)
    for i in range(min(lx,ly)):
        if x[i] == y[i]:
            lcp += 1
        elif x[i] < y[i]:
            return (-1, lcp)
        else:
            return (+1, lcp)
    if lx == ly:
        return (0, lcp)
    elif lx < ly:
        return (-1, lcp)
    else: 
        return (+1, lcp)


def pred(txt, pat, sa):
    m = len(pat)
    n = len(txt)
    if not lex_leq(txt[sa[0]:], pat, m):
        return -1
    elif lex_leq(txt[sa[n-1]:], pat, m):
        return n-1
    else:
        l, r = 0, n-1
        while (r - l) > 1: # pred [l, r)
            h = ( l + r) //2
            print("comparing pat=%s to txt[%d:]=%s"%(pat, h, txt[sa[h]:]))
            if lex_leq(txt[sa[h]:], pat, m):
                l = h
            else:
                r = h
        return l


def succ(txt, pat, sa):
    m = len(pat)
    n = len(txt)
    if lex_leq(pat, txt[sa[0]:], m):
        return 0
    elif not lex_leq(pat, txt[sa[n-1]:], m):
        return n
    else:
        l, r = 0, n-1  # succ in (l,r]
        while (r - l) > 1: 
            h = ( l + r) //2
            print("comparing pat=%s to txt[%d:]=%s"%(pat, h, txt[sa[h]:]))
            if lex_leq(pat, txt[sa[h]:], m):
                r = h
            else:
                l = h
        return r

"""
Llcp > L
                        |    
       |                |                 
Llcp   |----------------|                 |
       |                |                 |
   L   |*               |*                |
       |*               |*                |
       |*               |*                |
       |*_______________|*________________|
       l                h                 r
    l = h
    L não muda         

Llcp = L
                        |    
       |                |                 
       |                |                 |
       |                |                 |
Llcp=L |*---------------|*                |
       |*               |*                |
       |*               |*                |
       |*_______________|*________________|
       l                h                 r
    comparar com txt[sa[h]:] a partir de L 
           
Llcp < L
                        |    
       |                |                 
   L   |*               |                 |
       |*               |                 |
Llcp   |*---------------|*                |
       |*               |*                |
       |*               |*                |
       |*_______________|*________________|
       l                h                 r

       r = h
       R = Llcp[h]

R >= L

Rlcp > R
                        |    
       |                |                 |
       |                |-----------------|  Rlcp
       |                |                 |
       |                |*                |* R
       |                |*                |*
       |                |*                |*
       |________________|*________________|*
       l                h                 r
    r = h
    R não muda         


Rlcp = R
                        |    
       |                |                 |
       |                |                 |
       |                |                 |
       |                |*----------------|* R = Rlcp
       |                |*                |*
       |                |*                |*
       |________________|*________________|*
       l                h                 r
    compara com txt[sa[h]:] a partir de R


Rlcp < R
                        |    
       |                |                 |
       |                |                 |* R
       |                |                 |*
       |                |*----------------|* Rlcp
       |                |*                |*
       |                |*                |*
       |________________|*________________|*
       l                h                 r

l = h
L = Rlcp

"""
def succ2(txt, pat, sa, Llcp, Rlcp):
    m = len(pat)
    n = len(txt)
    (cmp_first,L) = lex_cmp(pat, txt[sa[0]:])
    (cmp_last, R) = lex_cmp(pat, txt[sa[n-1]:])
    if cmp_first <= 0:
        return 0
    elif cmp_last > 0:
        return n
    else:
        l, r = 0, n-1  # succ in (l,r]
        while (r - l) > 1: 
            h = ( l + r) //2
            if L >= R:
                if L <= Llcp[h]:
                    (cmp_h, lcp_h) = lex_cmp(pat[L:], txt[sa[h]+L:])
                    H = L + lcp_h
                else:
                    H = Llcp[h]
            else:
                if R <= Rlcp[h]:
                    (cmp_h, lcp_h) = lex_cmp(pat[R:], txt[sa[h]+R:])
                    H = R + lcp_h
                else:
                    H = Rlcp[h]
            if H==m or pat[H] <= txt[sa[h]+H]:
                r, R = h, H
            else:
                l, L = h, H
        return r



def pred2(txt, pat, sa, Llcp, Rlcp):
    m = len(pat)
    n = len(txt)
    (cmp_first,L) = lex_cmp(pat, txt[sa[0]:])
    (cmp_last, R) = lex_cmp(pat, txt[sa[n-1]:])
    if cmp_first < 0:
        return -1
    elif cmp_last >= 0:
        return n-1
    else:
        l, r = 0, n-1  # pred in [l,r)
        while (r - l) > 1: 
            h = ( l + r) //2
            if L >= R:
                if L <= Llcp[h]:
                    (cmp_h, lcp_h) = lex_cmp(pat[L:], txt[sa[h]+L:])
                    H = L + lcp_h
                else:
                    H = Llcp[h]
            else:
                if R <= Rlcp[h]:
                    (cmp_h, lcp_h) = lex_cmp(pat[R:], txt[sa[h]+R:])
                    H = R + lcp_h
                else:
                    H = Rlcp[h]
            if H==m or pat[H] > txt[sa[h]+H]:
                l, L = h, H
            else:
                r, R = h, H
        return l


def sarr_search(txt, pat, sa, Llcp, Rlcp):
    L = succ2(txt, pat, sa, Llcp, Rlcp)
    R = pred2(txt, pat, sa, Llcp, Rlcp)
    if L <= R:
        return sa[L:R+1]
    else: 
        return []


def test_build():
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


def test():
    txt = "abracadabra"
    n = len(txt)
    pat = "abra"
    m = len(pat)
    ab = "abcdr"
    P = build_P(txt, ab)
    Llcp = n * [-1]
    Rlcp = n * [-1]
    sa = build_sarr(P[-1])
    fill_RL_lcp(txt, P, sa, Llcp, Rlcp)
    occ = sarr_search(txt, pat, sa, Llcp, Rlcp)
    for i in occ:
        assert(pat==txt[i:i+m])



if __name__ == "__main__":
    test()