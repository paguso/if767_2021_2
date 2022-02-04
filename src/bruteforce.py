import sys

verbose = True

def debug(s):
    if verbose:
        print(s, end="") 


def bruteforce(txt, pat):
    occ = []
    n = len(txt)
    m = len(pat)
    i, j = 0, 0
    while i <= n - m:
        debug("\n"+txt+"\n")
        debug(i*" ")
        while j < m and txt[i+j] == pat[j]:
            j += 1
            debug(".")
        if j == m:
            occ.append(i)
        else:
            debug("!")
        debug("\n"+(i*" ")+pat+"\n")
        i = i + 1
        j = 0
    return occ


def test():
    txt = "abracadabra"
    pat = "abra"
    occ = bruteforce(txt, pat)
    print(occ)    



def main():
    global verbose
    verbose = False
    pat = sys.argv[1]
    txtfile = open(sys.argv[2], "r")
    count = 0
    for line in txtfile:
        txt = line.strip("\n")
        occ = bruteforce(txt, pat)
        if occ:
            print(txt)
        count += len(occ)        
    txtfile.close()
    print("Total occurrences", count)


if __name__ == "__main__":
    main()