from stanfordcorenlp import StanfordCoreNLP as corenlp
import json
import sys
from qClasses import qWord, wordGraph, Sql, Condition, Column
import os
# sys.stdout=open("output.txt", "w")

# nlp = corenlp('http://corenlp.run', 80)

# props = {
#     'annotators': 'pos,lemma,depparse',
#     'pipelineLanguage': 'en',
#     'outputFormat' : 'json',
#     'connection': 'open'
# }

# # nlq=str(input())
# nlq = "max solve from department of cse and section A"
# nlq = "max in solve"
# nlq = "solve from department of cse and section A"


# analysis = json.loads(nlp.annotate(nlq, properties=props))
# allanalysis = analysis['sentences'][0]
# basicDependencies=allanalysis['basicDependencies']
# tokens=allanalysis['tokens']

# # Dependency print
# for deps in basicDependencies:
#     print(deps['governorGloss'] + " -> " + deps['dependentGloss'])
#     # print(deps)
# print()

# words = list()

# lim = len(tokens)

# # qWord generation
# for it in range(lim):
#     words.append(qWord( word=tokens[it]['word'],
#                         lem=tokens[it]['lemma'],
#                         p_tag=tokens[it]['pos'],
#                         w_id=basicDependencies[it]['dependent']-1,
#                         par_id=basicDependencies[it]['governor']-1))

# # for w in words:
# #     print(w)

# # print("{} {} {}".format(words[1].isPossibleData(), words[1].isPossibleAggregate(), words[1].isPossibleColumn()))

# # Graph Conversion
# G = wordGraph(lim)

# for w in words:
#     G.addEdge(a=w.parent_id, b=w.word_id)

# # Word merging (DSU) and chunking


# # traverse graph bottom-up and generate conditions and selection clauses


# resQuery = Sql()

# vis = {}


# # remove unused 0 degree stopwords
# def removeStopWords(u):
#     # print("trying to remove {} {} {} {}".format(u, vis.get(u, 0)==0, words[u].stop_word, G.outdeg[u]==0))
#     now = u
#     while(now!=-1 and vis.get(u, 0)==0 and words[now].stop_word and G.outdeg[now]==0):
#         vis[u]=1
#         # print("visiting %d" %u)
#         par = G.P[now][-1]
#         G.outdeg[par]-=1
#         print("marking {} as stopword and outDeg[{}]={}".format(now, par, G.outdeg[par]))
#         now = par


# def isCondition(u, val=0):
#     if(u==-1):
#         return 0
#     if(val==3):
#         return 1
#     print("now at {} {} {}".format(u, words[u].words[-1], words[u].pos_tag))
#     par = G.P[u][-1]
#     # if(par==u):
#     #     print("whaaaaaaaaaaaaaaaaaaaaaaat?")
#     #     return 0
#     if(words[u].isPossibleColumn()):
#         if(vis.get(u, 0)==0 and (val&1) == 0):
#             print("Column found")
#             return isCondition(par, val|1)
#         else:
#             return 0
#     elif(words[u].isPossibleData() and (val&2) == 0):
#         if(vis.get(u, 0)==0):
#             print("Data found")
#             return isCondition(par, val|2)
#         else:
#             return 0
#     else:
#         print("Stopword")
#         return isCondition(par, val)

# condsCnt = 0

# def markCondition(u, val=0):
#     if(val==3):
#         return Condition(cond_id=condsCnt)

#     vis[u] = 1
#     par = G.P[u][-1]
#     G.outdeg[par]-=1
#     print("marking {} as visited and indeg[{}]={}".format(u, par, G.outdeg[par]))
#     if(words[u].isPossibleColumn()):
#         con = markCondition(par, val|1)
#         con.col_id = words[u].col_ids[-1]
#         return con
#     elif(words[u].isPossibleData()):
#         con = markCondition(par, val|2)
#         con.condition = words[u].words[-1]
#         return con
#     else:
#         return markCondition(par, val)
    
# # adding conditions

# print("Finding conditions")
# for u in reversed(range(G.sz)):
#     if(G.outdeg[u] == 0):
#         print("\n{} outdegree is zero".format(u))
#         if(isCondition(u)):
#             print("Condition found at {}".format(u))
#             con = markCondition(u)
#             resQuery.addCondition(cond=con)
#             condsCnt += 1
#         if(words[u].isPossibleStopWord):
#             removeStopWords(u)



# for con in resQuery.conditions:
#     print(con)

# def markSelection(u, val=0):
#     if(val==3 or u==-1):
#         return [-1, ""]

#     par = G.P[u][-1]
#     G.outdeg[par]-=1
#     if(words[u].isPossibleColumn() and vis.get(u, 0)==0):
#         if((val&1) == 0):
#             vis[u] = 1
#             print("Col found {}".format(u))
#             sel = markSelection(par, val|1)
#             sel[0] = words[u].col_ids[-1]
#             return sel
#         else:
#             return [-1, ""]
#     elif(words[u].isPossibleAggregate() and vis.get(u, 0)==0):
#         if((val&2) == 0):
#             vis[u] = 1
#             print("Agg found {}".format(u))
#             sel = markSelection(par, val|2)
#             sel[1] = words[u].aggr
#             return sel
#         else:
#             return [-1, ""]
#     else:
#         vis[u] = 1
#         return markSelection(par, val)


# for u in reversed(range(G.sz)):
#     if(G.outdeg[u] == 0 and words[u].stop_word):
#         removeStopWords(u)

# #adding selection clauses, including aggreate function if found
# print("Finding selection clauses")
# for u in reversed(range(G.sz)):
#     if(G.outdeg[u] == 0):
#         # print("Possible selection clause %d %d %d %d" %(u, words[u].isPossibleAggregate(), words[u].isPossibleColumn(), vis.get(u, 0)) )
#         if((words[u].isPossibleAggregate() or words[u].isPossibleColumn()) and vis.get(u, 0)==0):
#             print("Selection found at {}".format(u))
#             sele = markSelection(u)
#             resQuery.addSelection(sel=sele)
#     else:
#         removeStopWords(u)

# print(resQuery.selections)

######################################### NEW ###########################################



class aggQueryFinder:
    # global nlp
    # global nlq
    # global props
    # global column_names
    # global resQuery
    datasets = os.path.abspath("datasets")


    def __init__(self):
        self.nlp = corenlp('http://corenlp.run', 80)
        self.nlq = "No string yet"
        self.resQuery = Sql()
        self.props = {
            'annotators': 'pos,lemma,depparse',
            'pipelineLanguage': 'en',
            'outputFormat' : 'json',
            'connection': 'open'
        }
    
    def getSqlString(self, table_name):
        return self.resQuery.getFinalQuery(table_name)

    def __str__(self):
        return self.nlq
    
    def updateColumnNames(self, columns):
        self.column_names = list()
        # making a list of column names orederwise in this class scope
        for col in columns:
            self.column_names.append(col)
            self.resQuery.columns.append(col)
        
        colFile = open(os.path.join(self.datasets, "col_names.txt"), "w", encoding="utf-8")

        for i in range(len(self.column_names)):
            words = self.column_names[i].split()
            for word in words:
                colFile.write(word + " " + str(i) + "\n")
        
        colFile.close()
        pass
    
    ''' Takes a natural language query in qq
        And returns a Sql object from qClasses
    '''

    def query(self, qq):
        if not qq:
            return "The string is empty"
        
        self.nlq = qq

        analysis = json.loads(self.nlp.annotate(self.nlq, properties=self.props))
        allanalysis = analysis['sentences'][0]
        basicDependencies=allanalysis['basicDependencies']
        tokens=allanalysis['tokens']

        # Dependency print
        for deps in basicDependencies:
            print(deps['governorGloss'] + " -> " + deps['dependentGloss'])
            # print(deps)
        print()

        words = list()

        lim = len(tokens)

        # qWord generation
        for it in range(lim):
            words.append(qWord( word=tokens[it]['word'],
                                lem=tokens[it]['lemma'],
                                p_tag=tokens[it]['pos'],
                                w_id=basicDependencies[it]['dependent']-1,
                                par_id=basicDependencies[it]['governor']-1))

        # for w in words:
        #     print(w)

        # print("{} {} {}".format(words[1].isPossibleData(), words[1].isPossibleAggregate(), words[1].isPossibleColumn()))

        # Graph Conversion
        G = wordGraph(lim)

        for w in words:
            G.addEdge(a=w.parent_id, b=w.word_id)

        # Word merging (DSU) and chunking


        # traverse graph bottom-up and generate conditions and selection clauses

        vis = {}


        # remove unused 0 degree stopwords
        def removeStopWords(u):
            # print("trying to remove {} {} {} {}".format(u, vis.get(u, 0)==0, words[u].stop_word, G.outdeg[u]==0))
            now = u
            while(now!=-1 and vis.get(u, 0)==0 and words[now].stop_word and G.outdeg[now]==0):
                vis[u]=1
                # print("visiting %d" %u)
                par = G.P[now][-1]
                G.outdeg[par]-=1
                print("marking {} as stopword and outDeg[{}]={}".format(now, par, G.outdeg[par]))
                now = par


        def isCondition(u, val=0):
            if(u==-1):
                return 0
            if(val==3):
                return 1
            print("now at {} {} {}".format(u, words[u].words[-1], words[u].pos_tag))
            par = G.P[u][-1]
            # if(par==u):
            #     print("whaaaaaaaaaaaaaaaaaaaaaaat?")
            #     return 0
            if(words[u].isPossibleColumn()):
                if(vis.get(u, 0)==0 and (val&1) == 0):
                    print("Column found")
                    return isCondition(par, val|1)
                else:
                    return 0
            elif(words[u].isPossibleData() and (val&2) == 0):
                if(vis.get(u, 0)==0):
                    print("Data found")
                    return isCondition(par, val|2)
                else:
                    return 0
            else:
                print("Stopword")
                return isCondition(par, val)

        condsCnt = 0

        def markCondition(u, val=0):
            if(val==3):
                return Condition(cond_id=condsCnt)

            vis[u] = 1
            par = G.P[u][-1]
            G.outdeg[par]-=1
            print("marking {} as visited and indeg[{}]={}".format(u, par, G.outdeg[par]))
            if(words[u].isPossibleColumn()):
                con = markCondition(par, val|1)
                con.col_id = words[u].col_ids[-1]
                return con
            elif(words[u].isPossibleData()):
                con = markCondition(par, val|2)
                con.condition = words[u].words[-1]
                return con
            else:
                return markCondition(par, val)
            
        # adding conditions

        print("Finding conditions")
        for u in reversed(range(G.sz)):
            if(G.outdeg[u] == 0):
                print("\n{} outdegree is zero".format(u))
                if(isCondition(u)):
                    print("Condition found at {}".format(u))
                    con = markCondition(u)
                    self.resQuery.addCondition(cond=con)
                    condsCnt += 1
                if(words[u].isPossibleStopWord):
                    removeStopWords(u)



        for con in self.resQuery.conditions:
            print(con)

        def markSelection(u, val=0):
            if(val==3 or u==-1):
                return [-1, ""]

            par = G.P[u][-1]
            G.outdeg[par]-=1
            if(words[u].isPossibleColumn() and vis.get(u, 0)==0):
                if((val&1) == 0):
                    vis[u] = 1
                    print("Col found {}".format(u))
                    sel = markSelection(par, val|1)
                    sel[0] = words[u].col_ids[-1]
                    return sel
                else:
                    return [-1, ""]
            elif(words[u].isPossibleAggregate() and vis.get(u, 0)==0):
                if((val&2) == 0):
                    vis[u] = 1
                    print("Agg found {}".format(u))
                    sel = markSelection(par, val|2)
                    sel[1] = words[u].aggr
                    return sel
                else:
                    return [-1, ""]
            else:
                vis[u] = 1
                return markSelection(par, val)


        for u in reversed(range(G.sz)):
            if(G.outdeg[u] == 0 and words[u].stop_word):
                removeStopWords(u)

        #adding selection clauses, including aggreate function if found
        print("Finding selection clauses")
        for u in reversed(range(G.sz)):
            if(G.outdeg[u] == 0):
                # print("Possible selection clause %d %d %d %d" %(u, words[u].isPossibleAggregate(), words[u].isPossibleColumn(), vis.get(u, 0)) )
                if((words[u].isPossibleAggregate() or words[u].isPossibleColumn()) and vis.get(u, 0)==0):
                    print("Selection found at {}".format(u))
                    sele = markSelection(u)
                    self.resQuery.addSelection(sel=sele)
            else:
                removeStopWords(u)
        return self.resQuery