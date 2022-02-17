"""

Shift-Or 

17/02/2002

"""

from debug import debug
import sys


from bitarray import bitarray


ascii = [chr(i) for i in range(128)]


def char_masks(pat, ab):
    m = len(pat)
    C = { a : bitarray(m*[1]) for a in ab}
    for j in range(m):
        C[pat[j]][m-1-j] = 0 # bitarray indexado do j=0(msb)...m-1(lsb)
    return C


def shift_or(txt, pat, ab, C=None):
    n = len(txt)
    m = len(pat)
    C = char_masks(pat, ab) if not C else C
    S = bitarray(m * [1])
    occ = []
    for i in range(n):
        S = (S << 1) | C[txt[i]]
        if S[0] == 0:
            occ.append(i+1-m)
    return occ


def test():

    pat = "abab" # C[b]= 1101
    txt = "abcabab"
    ab = "abc"
    occ = shift_or(txt, pat, ab)
    print(occ)


def main():
    ab = ascii
    occ = []
    global verbose
    verbose = False
    pat = sys.argv[1]
    C = char_masks(pat, ab)
    txtfile = open(sys.argv[2], "r")
    count = 0
    for line in txtfile:
        txt = line.strip("\n")
        occ = shift_or(txt, pat, ab, C)
        if occ:
            #pass
            print(txt)
        count += len(occ)        
    txtfile.close()
    print("Total occurrences", count)


if __name__ == "__main__":
    #test()
    main()