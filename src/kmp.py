import sys

verbose = True

def debug(s):
    global verbose
    if verbose:
        print(s, end="") 

"""

AAAAAAAAAAAAAAAAAAAA
----      ---- 
  k        k   
--------------
      j       

"""
def init_next_bf(pat):
    m = len(pat)
    nxt = (m + 1) * [-1] 
    for j in range(1, m + 1):
        for k in range(0, j):
            if pat[:k] == pat[j-k:j]:
                nxt[j] = k
    return nxt


def init_next(pat):
    m = len(pat)
    nxt = (m+1) * [0]
    nxt[0] = -1
    nxt[1] = 0
    i, j = 1, 0
    while i + j < m:
        debug("\n"+pat+"\n")
        debug((i*" ") + (j*"="))
        while i + j < m and pat[i+j] == pat[j]:
            debug(".")
            j += 1
            nxt[i + j] = j
            #debug("match nxt[%d]=%d\n"%(i+j, j))
        if i + j < m:
            debug("!")
        debug("\n"+(i*" ")+pat+"\n")
        i += (j - nxt[j])
        j = max(0, nxt[j])
    return nxt


def init_strict_next(pat):
    m = len(pat)
    nxt = (m+1) * [-1]
    nxt[0] = -1
    if m==1 or (m > 1 and pat[0] != pat[1]):
        nxt[1] = 0
    i, j = 1, 0
    while i + j < m:
        debug("\n"+pat+"\n")
        debug((i*" ") + (j*"="))
        while i + j < m and pat[i+j] == pat[j]:
            debug(".")
            j += 1
            if i + j == m or pat[i + j] != pat[j]:
                nxt[i + j] = j
            else:
                nxt[i + j] = nxt[j]
            #debug("match nxt[%d]=%d\n"%(i+j, j))
        if i + j < m:
            debug("!")
        if j == 0 and ((i + 1 == m) or (pat[0] != pat[i + 1])):
            nxt[i + 1] = 0
        debug("\n"+(i*" ")+pat+"\n")
        i += (j - nxt[j])
        j = max(0, nxt[j])
    return nxt



def kmp(txt, pat, nxt = None):
    occ = []
    n = len(txt)
    m = len(pat)
    nxt = init_next(pat) if not nxt else nxt
    i, j = 0, 0
    while i <= n - m:
        debug("\n"+txt+"\n")
        debug((i*" ") + (j*"="))
        while j < m and txt[i+j] == pat[j]:
            j += 1
            debug(".")
        if j == m:
            occ.append(i)
        else:
            debug("!")
        debug("\n"+(i*" ")+pat+"\n")
        i = i + (j - nxt[j])
        j = max(0, nxt[j])
    return occ


def test():
    txt = "abracadabraabraabracadabra"
    pat = "abracadabra"
    nxt = init_strict_next(pat)
    print(pat)
    print(nxt)
    occ = kmp(txt, pat, nxt)
    print(occ)    



def main():
    global verbose
    verbose = False
    pat = sys.argv[1]
    txtfile = open(sys.argv[2], "r")
    count = 0
    for line in txtfile:
        txt = line.strip("\n")
        occ = kmp(txt, pat)
        if occ:
            print(txt)
        count += len(occ)        
    txtfile.close()
    print("Total occurrences", count)


if __name__ == "__main__":
    #test()
    main()