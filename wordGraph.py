from collections import defaultdict

class wordGraph:
    sz = int()
    indeg = defaultdict(int)
    outdeg = defaultdict(int)
    G = defaultdict(list)

    def __init__(self, sz=0):
        self.sz=sz

    def addEdge(self, a, b):
        self.G[a].append(b)
        self.indeg[b] += 1
        self.outdeg[a] += 1
        print("Edge from {} to {} added.".format(a, b))