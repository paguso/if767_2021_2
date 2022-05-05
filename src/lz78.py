# 05/05/22 LZ78

import sys

maxdictbytes = 2
maxdictlen = 1 << (8 * maxdictbytes)

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


def encode():
    inp = open(sys.argv[2], "r")
    out = open(sys.argv[3], "wb")

    dic = {"":0}
    
    prefix = ""
    index = 0 
    while True:
        b = inp.read(1)
        if not b:
            break
        prefix += b
        if prefix in dic:
            index = dic[prefix]
        else:
            out.write(index.to_bytes(maxdictbytes, "little"))
            out.write(ord(b).to_bytes(1, "little"))
            if len(dic) == maxdictlen:
                dic = {"":0}
            dic[prefix] = len(dic) 
            prefix = ""
            index = 0
    if prefix:
        out.write(index.to_bytes(maxdictbytes, "little"))
        #out.write(int(0).to_bytes(1, "little"))

    inp.close()
    out.close()


def decode():
    inp = open(sys.argv[2], "rb")
    out = open(sys.argv[3], "w")
    dic = [""]
    while True:
        b = inp.read(maxdictbytes)
        if not b:
            break
        index = int.from_bytes(b, "little")
        match = dic[index]
        out.write(match)
        b = inp.read(1)
        if not b:
            break
        c = chr(int.from_bytes(b, "little"))
        out.write(c)
        if len(dic) == maxdictlen:
            dic = [""]
        dic.append(match+c)
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