from collections import defaultdict
import os
datasets = os.path.abspath("datasets")

'''
'''
class qWord:

    words = list()
    lemma = str()
    pos_tag = str()
    word_id = int()
    parent_id = int()
    col_ids = list()
    aggr = str()
    operat = str()
    stop_word = bool()
    possible_rec_cols = set()

    def __init__(self, word="", lem="", p_tag="", w_id=-1, par_id=-1):
        self.words = [word]
        self.lemma = lem
        self.pos_tag = p_tag
        self.word_id = w_id
        self.parent_id = par_id
        self.col_ids = self.getColMatches(word)
        self.aggr = self.getAggrId(word)
        self.operat = self.getOperator(word)
        self.stop_word = self.isPossibleStopWord(word)
        self.possible_rec_cols = self.getRecMatches(word)

        print("New object created!")
        # print(self)

    def __str__(self):
        show = str('\nPrinting object\n')
        show = show + ("Words: " + str(self.words)) + "\n"
        show = show + ("Lemma: " + str(self.lemma)) + "\n"
        show = show + ("Pos tag: " + str(self.pos_tag)) + "\n"
        show = show + ("Word_id: " + str(self.word_id)) + "\n"
        show = show + ("parent_id: " + str(self.parent_id)) + "\n"
        show = show + ("col_ids: " + str(self.col_ids)) + "\n"
        show = show + ("aggr: " + str(self.aggr)) + "\n"
        show = show + ("operat: " + str(self.operat)) + "\n"
        show = show + ("stop_word: " + str(self.stop_word)) + "\n"
        show = show + ("possible_rec_cols: " + str(self.possible_rec_cols)) + "\n"
        show = show + "\n"
        
        return show

    def isPossibleAggregate(self):
        return len(self.aggr)!=0

    def isPossibleData(self):
        if(self.isPossibleAggregate()):
            return 0
        dataTags = open(os.path.join(datasets, "data_tags.txt"), "r", encoding="utf-8")

        for line in dataTags:
            words = line.split()
            if (words[0] == self.pos_tag): # or name == self.lemma
                return True

        return False

    def isPossibleColumn(self):
        return len(self.col_ids) > 0

    def getColMatches(self, word):
        colFile = open(os.path.join(datasets, "col_names.txt"), "r", encoding="utf-8")
        col_mat = list()

        for line in colFile:
            name, it = line.split()
            if (name == word): # or name == self.lemma
                col_mat.append(int(it))

        return col_mat


    def getAggrId(self, word):
        aggFile = open(os.path.join(datasets, "agg_functions.txt"), "r", encoding="utf-8")
        agg = str()

        for line in aggFile:
            name, it = line.split()
            if (name == word): # or name == self.lemma
                agg = it

        return agg


    def getOperator(self, word):
        opFile = open(os.path.join(datasets, "operators.txt"), "r", encoding="utf-8")
        op = str()

        for line in opFile:
            name, it = line.split()
            if (name == word): # or name == self.lemma
                op = it

        return op

    def isPossibleStopWord(self, word):
        return self.isPossibleData()==0 and self.isPossibleColumn()==0 and self.isPossibleAggregate()==0


    def getRecMatches(self, word):
        return set()

'''
'''
class Condition:
    cond_id = int()
    col_id = int()
    operator = str()
    condition = str()

    def __init__(self, cond_id=-1, col_id=-1, operat="=", condition=""):
        self.cond_id = cond_id
        self.col_id = col_id
        self.operator = operat
        self.condition = condition

    def __str__(self):
        show = str('\nPrinting Condition\n')
        show += "Cond id: {}".format(self.cond_id) + "\n"
        show += "Col id: {}".format(self.col_id) + "\n"
        show += "Operator: {}".format(self.operator) + "\n"
        show += "Condition: '{}'".format(self.condition) + "\n"
        show += "\n"
        return show

'''
'''
class Column:
    col_id = int()
    column_name = str()
    column_lemmas = list()
    functions = list()

    def __init__(self, col_id=-1, col_name=""):
        self.col_id = col_id
        self.col_name = col_name


'''
'''
class Sql:
    selections = list()
    conditions = list()

    def __init__(self):
        self.selections = list()
        self.conditions = list()

    def addCondition(self, cond):
        self.conditions.append(cond)
    
    def addSelection(self, sel):
        self.selections.append(sel)


'''
'''
class wordGraph:
    sz = int()
    indeg = defaultdict(int)
    outdeg = defaultdict(int)
    P = defaultdict(list)
    G = defaultdict(list)

    def __init__(self, sz=0):
        self.sz=sz

    def addEdge(self, a, b):
        self.G[a].append(b)
        self.P[b].append(a)
        self.indeg[b] += 1
        self.outdeg[a] += 1
        print("Edge from {} to {} added.".format(a, b))