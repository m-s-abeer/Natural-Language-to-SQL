from stanfordcorenlp import StanfordCoreNLP as corenlp
import json
import sys
from qword import qWord
# sys.stdout=open("output.txt", "w")

nlp = corenlp('http://corenlp.run', 80)

props = {
    'annotators': 'pos,lemma,depparse',
    'pipelineLanguage': 'en',
    'outputFormat' : 'json',
    'connection': 'open'
}

nlq=str(input())

analysis = json.loads(nlp.annotate(nlq, properties=props))
allanalysis = analysis['sentences'][0]
enhancedDependencies=allanalysis['enhancedPlusPlusDependencies']
tokens=allanalysis['tokens']

words = list()

lim = len(tokens)

# qWord generation
for it in range(lim):
    words.append(qWord( word=tokens[it]['word'],
                        lem=tokens[it]['lemma'],
                        p_tag=tokens[it]['pos'],
                        w_id=it,
                        par_id=enhancedDependencies[it]['governor']-1))

for w in words:
    print(w)

# Graph Conversion


# Word merging (DSU) and chunking


# traverse graph bottom-up and generate conditions and selection clauses