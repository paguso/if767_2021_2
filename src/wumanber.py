# 03/03/2022 Wu-Manber


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


def wu_manber(txt, pat, ab, r, cmasks=None):
    cmasks = char_masks(pat, ab) if not cmasks else cmasks
    m = len(pat)
    n = len(txt)
    occ = []
    s = [bitarray(m*[1])]
    for q in range(1, r+1):
        s.append(s[q-1]<<1)
    for i in range(n):
        t = [((s[0] << 1) | cmasks[txt[i]])] ## erro 0 == shift or
        for q in range(1,r+1):
            t.append(\
                ((s[q] << 1) | cmasks[txt[i]]) \
                & (s[q-1] << 1)\
                & (t[q-1] << 1)\
                & (s[q-1] ) \
            )
        s = t
        #print("i=",i)
        #print(s)
        if s[r][0] == 0:
            occ.append(i)
    return occ

def test():
    txt ="parolles	a follower of bertram."
    pat = "love"
    ab = ascii
    r = 1
    occ = wu_manber(txt, pat, ab, r)
    print("Occ = ",occ)


def main():
    print("Usage: python3 wumanber.py pattern txt_file error")
    occ = []
    global verbose
    verbose = False
    pat = sys.argv[1]
    txtfile = open(sys.argv[2], "r")
    err = int(sys.argv[3])
    count = 0
    count_lines = 0
    chmask = char_masks(pat, ascii)
    for line in txtfile:
        txt = line.strip("\n")
        occ = wu_manber(txt, pat, ascii, err, chmask)
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