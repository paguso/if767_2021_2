# 05/05/22 LZ77

"""
        search buf           lahead buf
                             i
                                 !    
-------|----****a-----------|****c---------|-------------
        0   p   p+l
                codeword ---> p,l,c

-------|----****a-----------|****c---------|-------------
------------|--------------------|--------------|-------------
       avanco = l+1 
"""

import sys

sbufbytes = 1
labufbytes = 1
sbufsize = 1 << (8*sbufbytes)
labufsize = 1 << (8*labufbytes)

"""
returns pos and length of the max prefix of pat in txt
"""
def max_prefix_match_bf(txt, pat):
    n = len(txt)
    m = len(pat) - 1
    p = 0
    l = 0
    for i in range(n):
        j = 0
        while i+j<n and j<m and pat[j]==txt[i+j]:
            j += 1
        if j > l:
            l = j
            p = i
    return p, l 


"""

      a    b    a    b    a    a
    0--->1--->2--->3--->4--->5--->6
                        ^____|  
                           b  


    -------------------------|a
    ******             ******
    **a                    ** 


"""      

def max_prefix_match(txt, pat):
    m = len(pat)-1
    n = len(txt)

    fsm = [128*[0]]
    fsm[0][ord(pat[0])] = 1
    brd = 0
    for c in range(1,m):
        fsm.append(fsm[brd][:])
        fsm[c][ord(pat[c])] = c+1
        brd = fsm[brd][ord(pat[c])]

    l = 0
    p = 0
    cur = 0
    i = 0
    while i < n and l < m:
        cur = fsm[cur][ord(txt[i])]
        if cur > l:
            l = cur
            p = i - l + 1
        i += 1
    return p, l

def encode():
    inp = open(sys.argv[2], "r")
    out = open(sys.argv[3], "wb")
    sbuf = sbufsize * ' ' 
    labuf = inp.read(labufsize)
    m = len(labuf)
    while m > 0:
        p, l = max_prefix_match(sbuf, labuf)
        c = labuf[l]
        assert 0 <= p and p < sbufsize
        assert 0 <= l and l < m 
        out.write(p.to_bytes(sbufbytes, "little"))
        out.write(l.to_bytes(labufbytes, "little"))
        out.write(ord(c).to_bytes(1, "little"))
        sbuf = sbuf[l+1:] + labuf[:l+1] 
        labuf = labuf[l+1:] + inp.read(l+1)
        m = len(labuf)
    inp.close()
    out.close()


def decode():
    inp = open(sys.argv[2], "rb")
    out = open(sys.argv[3], "w")
    sbuf = sbufsize * ' ' 
    while True:
        b = inp.read(sbufbytes)
        if not b:
            break
        p = int.from_bytes(b, "little")
        b = inp.read(labufbytes)
        l = int.from_bytes(b, "little")
        b = inp.read(1)
        c = chr(int.from_bytes(b, "little"))
        prefix = sbuf[p:p+l]
        out.write(prefix)
        out.write(c)
        sbuf = sbuf[l+1:] + prefix + c
    inp.close()
    out.close()


def main():
    if sys.argv[1] == "c":
        encode()
    elif sys.argv[1] == "d":
        decode()
    else:
        print("invalid options")
        exit(1)

if __name__=="__main__":
    main()