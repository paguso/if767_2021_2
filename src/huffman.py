# 04/05/2022 Huffman coding

import heapq

class Node:
    def __init__(self, chars, freq, left=None, right=None):
        self.chars = chars
        self.freq = freq
        self.chd = [left, right]
    def __lt__(self, other):
        return self.freq < other.freq

class Huffman:
    def __init__(self, ab, freqs):
        self.ab = ab
        self.freqs = freqs
        self.root = None
        self.codes = {}
        self.init_tree()
        self.init_codes()

    def init_tree(self):
        heap = [Node(self.ab[i], self.freqs[i]) for i in range(len(self.ab))]
        heapq.heapify(heap)
        while len(heap) > 1:
            r1 = heapq.heappop(heap)
            r2 = heapq.heappop(heap)
            r = Node(r1.chars+r2.chars, r1.freq+r2.freq, r1, r2)
            heapq.heappush(heap, r)
        self.root = heapq.heappop(heap)

    def _print_node(self, root, level):
        if root==None:
            return
        self._print_node(root.chd[1], level+1)
        print("%s[%s %d]"%(level*"    ", root.chars, root.freq))
        self._print_node(root.chd[0], level+1)

    def print_tree(self):
        self._print_node(self.root, 0)

    def _init_code(self, root, codeword):
        if root.chd[0] == None: # i'm a leaf
            self.codes[root.chars] = codeword
        else:
            for bit in range(2):
                self._init_code(root.chd[bit], codeword+str(bit))

    def init_codes(self):
        self._init_code(self.root, "")

    def encode(self, txt):
        return "".join([self.codes[c] for c in txt])
    
    def decode(self, code):
        txt = ""
        cur = self.root
        for bit in code:
            cur = cur.chd[int(bit)]
            if cur.chd[0] == None: # cur is a leaf
                txt += cur.chars
                cur = self.root
        return txt


def compute_freqs(ab, txt):
    f_ascii = 128 * [0]
    for c in txt:
        f_ascii[ord(c)] += 1
    return [f_ascii[ord(c)] for c in ab]


def test():
    txt = "abracadabra"
    ab = "abcdr"
    freqs = compute_freqs(ab, txt)
    print("freqs=",freqs)
    huff = Huffman(ab, freqs)
    huff.print_tree()
    print(huff.codes)

    txt = "abraabracabraaabracadabra"

    encoded = huff.encode(txt)
    print("encoded =", encoded)
    decoded = huff.decode(encoded)
    print("decoded =", decoded)
    assert(decoded==txt)

if __name__=="__main__":
    test()