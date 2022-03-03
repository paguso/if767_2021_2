# 03/03/2022 Alg Sellers

import sys
from debug import debug

"""
computa matriz de pd
                           
                    x       
          0  1  2  ...      n    
        --------------------------
   0    | 0  1  2           n  
y  1    | 1            
   2    | 2         d[i,j] = d(y[:i], x[:j])
  ...   |           
   m    | m
"""
def edit_distance(x, y):
    n = len(x)
    m = len(y)
    col = list(range(0,m+1))
    for j in range(0,n):
        nxt = next_col(col, y, x[j], j+1)
        col = nxt
        #print("col[%d]="%(j+1), col)
    return col[m]


def next_col(col, y, a, j = 0):
    m = len(y)
    nxt = (m + 1) * [j]
    for i in range(1, m+1):
        nxt[i] = min(col[i] + 1, nxt[i-1] + 1, col[i-1] + (0 if a == y[i-1] else 1))
    return nxt



def sellers(x, y, r):
    n = len(x)
    m = len(y)
    occ = []
    col = list(range(0,m+1))
    for j in range(0,n):
        nxt = next_col(col, y, x[j])
        col = nxt
        if col[m] <= r:
            occ.append(j)
        #print("col[%d]="%(j+1), col)
    return occ 


def test():
    txt = "abadac"
    pat = "cada"    
    dist = edit_distance(txt, pat)
    print("dist(%s,%s)=%d"%(txt,pat,dist))
    r = 1
    occ = sellers(txt, pat, r)
    print("Approx(%s,%s,%r)="%(txt,pat,r), occ)



def main():
    print("Usage: python3 sellers.py pattern txt_file error")
    occ = []
    global verbose
    verbose = False
    pat = sys.argv[1]
    txtfile = open(sys.argv[2], "r")
    err = int(sys.argv[3])
    count = 0
    count_lines = 0
    for line in txtfile:
        txt = line.strip("\n")
        occ = sellers(txt, pat, err)
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
