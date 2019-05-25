import os
datasets = os.path.abspath("datasets")


class qWord:

    words = list()
    lemma = str()
    pos_tag = str()
    word_id = int()
    parent_id = int()
    col_names = set()
    aggr = str()
    operat = str()
    stop_word = bool()
    possible_rec_cols = set()

    def __init__(self, word="", lem="", p_tag="", w_id="-1", par_id="-1"):
        self.words = [word]
        self.lemma = lem
        self.pos_tag = p_tag
        self.word_id = w_id
        self.parent_id = par_id
        self.col_names = self.getColMatches(word)
        self.aggr = self.getAggrId(word)
        self.operat = self.getOperator(word)
        self.stop_word = self.isStopWord(word)
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
        show = show + ("col_names: " + str(self.col_names)) + "\n"
        show = show + ("aggr: " + str(self.aggr)) + "\n"
        show = show + ("operat: " + str(self.operat)) + "\n"
        show = show + ("stop_word: " + str(self.stop_word)) + "\n"
        show = show + ("possible_rec_cols: " + str(self.possible_rec_cols)) + "\n"
        show = show + "\n"
        
        return show

    def getColMatches(self, word):
        colFile = open(os.path.join(datasets, "col_names.txt"), "r", encoding="utf-8")
        col_mat = set()

        for line in colFile:
            name, it = line.split()
            if (name == word): # or name == self.lemma
                col_mat.add(int(it))

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


    def isStopWord(self, word):
        return False


    def getRecMatches(self, word):
        return set()