# Boyer Moore
# 10/02/2022

import sys

from debug import  debug
from kmp import init_next

verbose = False

ascii = [chr(i) for i in range(128)]


def bad_char(pat, alphabet=ascii):
    l = len(alphabet)
    m = len(pat)
    C = {alphabet[i]:-1 for i in range(l)}
    for i in range(m):
        C[pat[i]] = i
    return C


"""

ABRACADABRA


caso 1
        k    j 
        8    13
0       |    | 
ABRACADABRAABRADA
     ___      ---
               U

caso 1
 k         j 
 1         11
 |         | 
ABRACADABRAABRADA
_           -----
               U

"""
def good_suffix_bf(pat):
    m = len(pat)
    delta = (m+1) * [0]
    for j in range(-1,m):
        U = pat[j+1:]
        len_U = m-1-j
        for k in range(m-1,-1,-1):
            if (len_U <= k and U == pat[k-len_U:k]) or \
                (k < len_U and pat[:k] == pat[m-k:]):
                break
        delta[j] = k
    debug("delta="+str(delta))
    return [m-d for d in delta]        


def good_suffix(pat):
    Pi = init_next(pat)
    PiR = init_next(pat[::-1])
    m = len(pat)
    S = (m+1) * [m - Pi[m]]
    for l in range(1, m):
        j = (m-1) - PiR[l]
        if l - PiR[l] < S[j]:
            S[j] = l - PiR[l]
    return S


def boyermoore(txt, pat, ab = ascii, bc = None, gs = None):
    occ = []
    n = len(txt)
    m = len(pat)
    C = bad_char(pat, ab) if not bc else bc
    S = good_suffix_bf(pat) if not gs else gs
    i = 0
    while i <= n - m:
        j = m-1
        debug("\n"+txt+"\n")
        while j >= 0  and txt[i+j] == pat[j]:
            j -= 1
        debug((i*" ") + (j*" ") + ("!" if j > 0 else "") + ((m-1-j)*"."))
        debug("\n"+(i*" ")+pat+"\n")
        if j < 0:
            occ.append(i)
            i += S[j]
        else:
            i += max(S[j], j - C[txt[i+j]])
    return occ


def test():
    txt = "abracadabraabraabracadabra"
    pat = "abracadabra"

    print(pat)
    C = bad_char(pat, "abcdr")
    print(C)
    S = good_suffix_bf(pat)
    print(S)
    S = good_suffix(pat)
    print(S)

    occ = boyermoore(txt, pat, "abcdr")


def main():
    global verbose
    verbose = False
    pat = sys.argv[1]
    bc = bad_char(pat)
    gs = good_suffix(pat)
    txtfile = open(sys.argv[2], "r")
    count = 0
    for line in txtfile:
        txt = line.strip("\n")
        occ = boyermoore(txt, pat, ascii, bc, gs)
        if occ:
            #pass
            print(txt)
        count += len(occ)        
    txtfile.close()
    print("Total occurrences", count)


if __name__ == "__main__":
    #test()
    main()