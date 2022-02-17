"""
15/02/2022

Alg Aho-Corasick
"""
import sys

from debug import debug

ascii = [chr(i) for i in range(128)]


def char_index(ab, c):
    global ascii
    if ab == ascii:
        return ord(c)
    return ab.index(c)    


def print_fsm(goto, fail, occ, ab=ascii):
    l = len(ab)
    n = len(goto)
    print("goto:")
    print("   ",end="")
    for s in range(n):
        print("%5d"%s, end="")
    print()
    for c in range(l):
        print("%c: "%(ab[c]), end="")
        for s in range(n):
            print("%5d"%goto[s][c], end="") 
        print()
    print ("occ:")
    for s in range(n):
        print ("%3d => "%s, end="")
        print (occ[s])
    print("fail:")
    for s in range(n):
        print("%5d"%s, end="")
    print()
    for s in range(n):
        print("%5d"%(fail[s]), end="")
    print()


"""
goto[s][c]
"""
def build_goto(pat_set, ab=ascii):
    l = len(ab)
    goto = [l*[-1]]
    occ = [[]]
    nxt = 1
    for k in range(len(pat_set)):
        pat = pat_set[k]
        m = len(pat)
        cur = 0
        j = 0
        c = char_index(ab, pat[j])
        while j < m and goto[cur][c] != -1:
            cur = goto[cur][c]
            j += 1
            c = char_index(ab, pat[j])
        while j < m:            
            c = char_index(ab, pat[j]) 
            goto[cur][c] = nxt
            goto.append(l*[-1])
            occ.append([])
            cur = nxt
            j += 1 
            nxt += 1
        occ[cur].append(k)
    for c in range(l):
        if goto[0][c] == -1:
            goto[0][c] = 0
    return (goto, occ)


def build_fail(pat_set, ab, goto, occ=ascii):
    n = len(goto)
    l = len(ab)
    fail = n * [-1]
    bfs = []
    for c in range(l):
        if goto[0][c] > 0:
            bfs.append(goto[0][c])
            fail[goto[0][c]] = 0
    while bfs:
        cur = bfs.pop(0)
        for c in range(l):
            suc = goto[cur][c]
            if suc >= 0:
                bfs.append(suc)
                brd = fail[cur]
                assert brd >= 0
                while goto[brd][c] < 0:
                    brd = fail[brd]
                fail[suc] = goto[brd][c]
                occ[suc].extend(occ[fail[suc]])
    return (fail, occ)


def build_fsm(pat_set, ab=ascii):
    goto, occ = build_goto(pat_set, ab)
    fail, occ = build_fail(pat_set, ab, goto, occ)
    return (goto, fail, occ)


def aho_corasick(txt, pat_set, ab = ascii, fsm = None):
    if not fsm:
        fsm = build_fsm(pat_set, ab)
    (goto, fail, occ) = fsm
    pat_lens = [len(p) for p in pat_set]
    occ_set = [[] for p in pat_set]
    n = len(txt)
    cur = 0
    i = 0
    while i < n:
        c = char_index(ab, txt[i])
        while goto[cur][c] < 0:
            cur = fail[cur]
        cur = goto[cur][c]
        for k in occ[cur]:
            occ_set[k].append(i - pat_lens[k] + 1)
        i += 1
    return occ_set

    
def test():
    ab = "ehirsu"
    pat_set = ["he", "she", "his", "hers"]
    fsm = build_fsm(pat_set, ab)
    (goto, fail, occ) = fsm
    print_fsm(goto, fail, occ, ab)
    txt = "ushers"
    occ_set = aho_corasick(txt, pat_set, ab, fsm)
    print(occ_set)


def main():
    global verbose
    verbose = False
    pat_set = sys.argv[1:-1]
    txtfile = open(sys.argv[-1], "r")
    count = 0
    fsm = build_fsm(pat_set)
    for line in txtfile:
        txt = line.strip("\n")
        occ_set = aho_corasick(line, pat_set, fsm=fsm)
        sum_occ = sum([len(occ) for occ in occ_set])
        if sum_occ:
            #pass
            print(txt)
        count += sum_occ        
    txtfile.close()
    print("Total occurrences", count)


if __name__ == "__main__":
    #test()
    main()