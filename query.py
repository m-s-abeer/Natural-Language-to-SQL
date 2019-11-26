#script is to modified
#default port for connecting to online site 80
#default port to run server and connect to at local machine 9000
#online address http://corenlp.run 80

from stanfordcorenlp import StanfordCoreNLP as corenlp
import json
import pprint
from sys import stdin
import sqlite3 as sqlite
from importlib import reload
import meta_generator as mg
# import time

def reloadLibs():
    reload(lcs)    

# path = r'H:\Libraries\JAVA\CoreNLP\corenlp-full'

#tokenize,ssplit,pos,ner,parse,depparse,openie

props = {
    'annotators': 'tokenize,ssplit,pos,lemma,depparse,parse,openie,ner',
    'pipelineLanguage': 'en',
    'outputFormat' : 'json',
    'connection': 'open'
}

aggregatemap = {
    'count':['number', 'total', 'count'], 
    '>=':['greater than or equal', 'at least', 'not less than'], 
    '>':['greater', 'more than', 'over'],
    '=':['equals', 'as']
}

link = 'http://127.0.0.1'
port = 9000

currentsentenceanalysis = {}
currentsentencetokens = []
currentsentencelemmas = []
currentsentencepos = []
currentsentencedependencies = []
databasemetainfo = {}

database = {}

databasemappedwords = {}
databasedata = {}
stringwordlist = {}

# def demonstrate(type='online', link='http://127.0.0.1', port=9000):
#     nlp =''
#     global databasemetainfo
#     global databasedata
#     global stringwordlist

#     databaseinfo = getmetadata()
#     databasedata = loaddatabasedata()
#     stringwordlist = stringDataList()

#     # if type == 'online':
#     #     nlp = connectserver(link, port)
#     # else:
#     #     nlp = runserver()
#     while True:
#         nlq = str(input('Enter the query: '))
#         # nlq = str(input()) #for input without a line        
#         print('Query: ' + nlq)
#         nlq, hashmap = dbMatch(nlq)
#         print('Phrased query: ' + nlq)
#         print('Hash info')
#         print(hashmap)
#         # analysis = getanalysis(nlp, nlq)     
#         # printdependency()
#         # print('getting table and column info')
#         # printcurrenttablerelationfromanalysis()
#         generateprimaryquery(nlq, hashmap, 'tracks')
#     closeserver(nlp)


def printcurrenttablerelationfromanalysis():
    returndict = []
    for word in getcurrentsentencelemmas():
        ret, table, column = existsindb(word)
        if ret:
            print(word + ' ' + table + ' ', end='')
            print(column)
            returndict.append({word: [table, column]})
    return returndict
    
def generateprimaryquery(nlq, hashed, table):
    structure = 'SELECT * FROM # WHERE __'
    structure = structure.replace('#', table) #table is the column for CSV
    # print(structure)
    conditions = ''
    i = 0
    for element in hashed:
        if i != 0:
            conditions += ' AND LOWER(' +  hashed[element][1] + ") = LOWER('" + hashed[element][0] + "')"
        else:
            conditions += 'LOWER(' + hashed[element][1] + ") = LOWER('" + hashed[element][0] + "')"
        i += 1
    # print(conditions)
    structure = structure.replace('__', conditions)
    if len(hashed) == 0:
        structure = structure.replace('WHERE', '')
    print(structure)
    return structure

def intermediatesql(nlq):
    global currentsentencedependencies
    for word in currentsentencedependencies:
        if word['governorGloss'] == 'ROOT':
            existance, table, column = existsindb(word['dependentGloss'])            
            print(existance)
            if existance:
                nlq = nlq.replace('*', column)
    return str(nlq)

def runquery(query, path='music.db'):
    con = sqlite.connect(path)
    cursor = con.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    con.close()
    return data


def stringDataList():
    global databasedata
    global databasemetainfo
    wordlist = {}
    for table in databasemetainfo:
        for column in databasemetainfo[table]:
            if databasemetainfo[table][column]['type'].lower() == 'string' or databasemetainfo[table][column]['type'].lower() == 'text' or databasemetainfo[table][column]['type'].lower() == 'varchar':
                wordlist[column] = databasedata[table][column]
    return wordlist

def dbMatch(query):
    global stringwordlist
    query, hashmap = lcs.hashTheMatches(query, stringwordlist)
    return query, hashmap


def loaddatabasedata(path='music.db'):
    con = sqlite.connect(path)
    global databasemetainfo
    databasedata = {}
    cursor = con.cursor()
    for table in databasemetainfo:
        query = 'SELECT * FROM ' + table
        cursor.execute(query)
        data = cursor.fetchall()
        cols = [i[0] for i in cursor.description]
        # print(cols)
        databasedata[table] = {cols[i]:[] for i in range(len(cols))}        
        for row in data:
            for i in range(len(cols)):
                databasedata[table][cols[i]].append(row[i])
    # mg.addsimilarities(databasedata)          
    return databasedata                   


def getlemma(nlp, sentence):
    props = {
    'annotators': 'lemma',
    'pipelineLanguage': 'en',
    'outputFormat' : 'json'
    }
    res = json.loads(nlp.annotate(sentence, properties=props))
    lemmadics = {}
    for sen in res['sentences']:
        for token in sen['tokens']:
            lemmadics[token['originalText']] = token['lemma']
    for word in lemmadics:
        sentence = sentence.replace(word, lemmadics[word])
    return sentence, lemmadics

def existsindb(word):
    databaseinfo = getdatabasemetainfo()
    for table in databaseinfo:
        # print(table)
        for column in databaseinfo[table]:
            # databaseinfo[table][column]['thesaurus']
            if word in databaseinfo[table][column]['thesaurus']:
                global databasemappedwords
                #found words that fit in some place db                
                return True, table, column
            # else:
    return False, '', ''

def getdatabaseconnection(path='music.db'):
    return sqlite.connect(path)

def getdatabasemetainfo():
    global databasemetainfo
    return databasemetainfo

def getcurrentsentenceanalysis():
    global currentsentenceanalysis
    return currentsentenceanalysis

def getcurrentsentencedependencies():
    global currentsentencedependencies
    return currentsentencedependencies

def getcurrentsentencelemmas():
    global currentsentencelemmas
    return currentsentencelemmas

def getcurrentsentencepos():
    global currentsentencepos
    return currentsentencepos

def getcurrentsentencetokens():
    global currentsentencetokens
    return currentsentencetokens


def getmetadata(file="meta.json"):
    global databasemetainfo
    databasemetainfo =  json.load(open(file))
    return databasemetainfo

def getanalysis(nlp, text):
    global currentsentenceanalysis
    global props
    currentsentenceanalysis = json.loads(nlp.annotate(text, properties=props))
    getdependencies(currentsentenceanalysis['sentences'][0]['basicDependencies'])
    gettokens(currentsentenceanalysis['sentences'][0]['tokens'])
    getlemmas(currentsentenceanalysis['sentences'][0]['tokens'])
    getpos(currentsentenceanalysis['sentences'][0]['tokens'])
    return currentsentenceanalysis

def getpos(tokens):
    global currentsentencepos
    currentsentencepos = []
    for token in tokens:
        currentsentencepos.append(token['pos'])

def getdependencies(dependencies):
    global currentsentencedependencies
    currentsentencedependencies = []
    for word in dependencies:
        currentsentencedependencies.append(word)

def getlemmas(tokens):
    global currentsentencelemmas
    currentsentencelemmas = []
    for token in tokens:
        currentsentencelemmas.append(token['lemma'])

def gettokens(tokens):
    global currentsentencetokens
    currentsentencetokens = []
    for token in tokens:
        currentsentencetokens.append(token['word']) 

def runserver():
    # path = r'H:\Libraries\JAVA\CoreNLP\corenlp-full'
    path = r'/media/shafi/Codes1/Libraries/JAVA/CoreNLP/corenlp-full'
    nlp = corenlp(path)
    return nlp

def closeserver(nlp):
    nlp.close()

def connectserver(link, port):
    nlp = corenlp(link, port=port)
    return nlp

def printdependency():
    global currentsentencedependencies
    print ("Word\t\tDepends On")
    for word in currentsentencedependencies:
        print(word['dependentGloss'] + '\t\t' + word['governorGloss'])

# demonstrate()
# demonstratefromfile()