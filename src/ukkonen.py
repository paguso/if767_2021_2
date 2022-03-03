# 03/03/2022 Ukkonen approx matching

from debug import debug
import sys

ascii = [chr(i) for i in range(128)]

def next_col(col, y, a, r):
    m = len(y)
    nxt = (m + 1) * [0]
    for i in range(1, m+1):
        nxt[i] = min(r + 1, col[i] + 1, nxt[i-1] + 1, col[i-1] + (0 if a == y[i-1] else 1))
    return nxt


def build_fsm(pat, r, ab):
    m = len(pat)
    s = tuple(range(0,m+1))
    queue = [(s,0)]
    all_states = {s:0}
    index_seq = 1 
    delta = {}
    final_states = set()
    if s[-1] <= r:
        final_states.add(0)   
    while queue:
        (cur, cur_index) = queue.pop(0)
        for a in ab:
            nxt = tuple(next_col(cur, pat, a, r))
            if nxt in all_states:
                nxt_index = all_states[nxt]
            else:
                nxt_index = index_seq
                index_seq +=1 
                queue.append((nxt, nxt_index))
                all_states[nxt] = nxt_index
                if nxt[-1] <= r:
                    final_states.add(nxt_index)   
            delta[(cur_index, a)] = nxt_index
    print("The FSM of %s has %d states"%(pat, index_seq))
    #print(delta)
    return (index_seq, delta, final_states)


def scan(txt, fsm):
    (q, delta, final) = fsm
    occ = []
    cur = 0
    if cur in final:
        occ.append(-1)
    n = len(txt)
    for i in range(n):
        cur = delta[(cur, txt[i])]
        if cur in final:
            occ.append(i)
    return occ


def test():
    pat = "cada"
    txt = "abadac"
    ab = "abcd"
    r = 2
    fsm = build_fsm(pat, r, ab)
    occ = scan(txt, fsm)
    print("occ = ", occ)


def main():
    print("Usage: python3 ukkonen.py pattern txt_file error")
    occ = []
    global verbose
    verbose = False
    pat = sys.argv[1]
    txtfile = open(sys.argv[2], "r")
    err = int(sys.argv[3])
    count = 0
    count_lines = 0
    fsm = build_fsm(pat, err, ascii)
    for line in txtfile:
        txt = line.strip("\n")
        occ = scan(txt, fsm)
        if occ:
            count_lines += 1 
            #pass
            print(txt)
        count += len(occ)        
    txtfile.close()
    print("Total occurrences", count, "in", count_lines, "lines")


if __name__ == "__main__":
    #test()
    main()
