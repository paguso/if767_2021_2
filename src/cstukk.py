"""
28/03/22 CST Ukkonen
"""
nid = 0

class Node:
    def __init__(self, l, r=None):
        global nid
        self.id = nid
        nid += 1
        self.l = l
        self.r = r
        self.slink = None
        self.chd = {}
    def edge_len(self):
        return self.r-self.l if self.r!=None else float('inf')

class CST:
    def __init__(self, ab):
        self.ab = ab
        self.grnd = Node(-1,-1)
        self.root = Node(-1,0)
        for c in ab:
            self.grnd.chd[c] = self.root
        self.root.slink = self.grnd
    
    def _prt(self, nd, lvl, in_char):
        print("%s%c:[id=%d l=%d r=%s slink=%s]"%(lvl*"    ", in_char, nd.id, nd.l, str(nd.r) if nd.r!=None else 'inf', str(nd.slink.id) if nd.slink else 'None'))
        for c in self.ab:
            if c in nd.chd:
                self._prt(nd.chd[c], lvl+1, c)

    def prt(self):
        self._prt(self.root, 0, '*')


def test_and_split(cur, txt, i):
    (u,l,r) = cur
    if l < r:
        v = u.chd[txt[l]] 
        """ 
           x[l] ... x[r-1] w ?=txt[i]? 
        u -----------------o----------------------------> v
           x[l']      ....  x[l'+(r-l)]  ....   x[r'-1]
                   [l',r') 
        """
        if txt[v.l + (r-l)] == txt[i]:
            return (True, None)
        else:
            w = Node(v.l, v.l + (r-l))
            v.l += (r-l)
            w.chd[txt[v.l]] = v
            u.chd[txt[w.l]] = w
            return(False, w)
    else:
        if txt[i] in u.chd:
            return (True, u)
        else:
            return (False, u)



"""
retorna ref canonica para vertice implicito cur = (u,l,r)
"""
def canonise(cur, txt):
    (u,l,r) = cur
    if l < r:
        v = u.chd[txt[l]]
        while (l < r) and v.edge_len() <= (r-l):
            u = v
            l += v.edge_len()        
            v = u.chd[txt[l]] if (l<r) else u
        return (u,l,r)
    else:
        return cur


"""
acrescenta novas folhas 
cur ----[i,+inf)----> leaf
onde cur é nó da fronteira do [ativo ao terminador)
retornando referência para o terminador
act = referência canônica p/ ativo
"""
def update(act, txt, i):
    cur = act
    last_w = None
    (is_term, w) = test_and_split(cur, txt, i)
    while not is_term:
        leaf = Node(i)
        w.chd[txt[i]] = leaf
        if last_w:
            last_w.slink = w
        last_w = w
        (u,l,r) = cur
        cur = canonise((u.slink, l, r), txt)
        (is_term, w) = test_and_split(cur, txt, i)
    if last_w:
        last_w.slink = w
    return cur


def build_cst(ab, txt):
    n = len(txt)
    cst = CST(ab)
    act = (cst.root,0,0)
    for i in range(n):
        term = update(act, txt, i)
        (u,l,r) = term
        assert(r==i)
        act = canonise((u,l,i+1), txt)
        print("CST[%s]:"%txt[:i+1])
        cst.prt()
    return cst


def test():
    ab = "ab"
    txt = "babaaabaabab"
    cst = build_cst(ab, txt)



if __name__ == "__main__":
    test()