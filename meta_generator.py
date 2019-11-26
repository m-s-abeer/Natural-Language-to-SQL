import pandas as pd
import json
import os
import sqlite3 as sqlite
# from nltk.corpus import wordnet
from messytables import CSVTableSet, type_guess, types_processor, \
                        headers_guess, headers_processor, offset_processor, \
                        any_tableset

class generator:
    def __init__ (self, filepath):      
        self.filename, extension = os.path.splitext(filepath)
        if extension == '.csv':
            self.csvMeta(filepath)
        elif extension == '.db':
            self.dbMeta(filepath)
    
    def csvMeta(self, filepath):
        dump = csvdump(filepath)
        meta = dump.getcolnames()
        # meta = self.addthes(meta)
        self.savemeta(meta)

    def dbMeta(self, filepath):
        dump = dbdump(filepath)
        meta = dump.createdump()
        # meta = self.addthes(prelimeta)
        self.savemeta(meta)

    def addthes(self, data):
        for table in data:
            for column in data[table]:
                data[table][column]['thesaurus'].extend(self.uniqueList([x.lemmas()[0].name() for x in wordnet.synsets(column)]))
        return data

    def uniqueList(self, l):
        return list(set(l))

    def savemeta(self, meta):
        print(meta)
        with open('meta.json', 'w') as file:
            json.dump(meta, file)

class csvdump:
    def __init__(self, path):
        self.path = path

    def getcolnames(self):
        file = open(self.path, 'rb')
        tableset = CSVTableSet(file)
        rowset = tableset.tables[0]
        offset, headers = headers_guess(rowset.sample)
        rowset.register_processor(headers_processor(headers))
        rowset.register_processor(offset_processor(offset+1))
        types = type_guess(rowset.sample, strict=True)
        meta = {}
        filename, ext = os.path.splitext(self.path)
        filename = filename.split('/')[-1]
        meta[filename] = {headers[i]: {'type': str(types[i])} for i in range(len(headers))}
        return meta

class dbdump:
    def __init__ (self, path):
        self.con = sqlite.connect(path)
        self.metadata = {}

    def __close__ (self):
        self.con.close()

    def createdump(self):
        cursor = self.con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
        tables = cursor.fetchall()
        # print(tables)
        meta = {}
        for table in tables:
            table_name = table[0]            
            cursor.execute('PRAGMA TABLE_INFO({})'.format(table_name))
            data = [[description[0],description[1],description[2]] for description in cursor.fetchall()]
            meta[table_name] = {data[i][1] : {'type': str(data[i][2])} for i in range(len(data))}
        return meta

class addsimilarities:
    def __init__ (self, databasedata):
        self.string_data = ['string', 'text', 'varchar', 'char']
        with open('meta.json') as file:
            self.meta = json.load(file)
        self.databasedata = databasedata
        self.addsimfield()
        self.update()
        self.save()
    
    def save(self):
        with open('meta.json', 'w') as file:
            json.dump(self.meta, file)

    def addsimfield(self):
        for table in self.meta:
            for column in self.meta[table]:
                self.meta[table][column]['similar'] = []

    def update(self):
        for table in self.meta:
            for column1 in self.meta[table]:
                for column2 in self.meta[table]:
                    # sim = similaritychecker(self.databasedata[table][column1], self.databasedata[table][column2])
                    # print(sim.result)
                    # print(column1, '', column2)
                    # print(len(self.databasedata[table][column1]))
                    # print(len(self.databasedata[table][column2]))
                    if self.meta[table][column1]['type'].lower() in self.string_data and self.meta[table][column2]['type'].lower() in self.string_data:
                        # print('pass 1 ', column1, ' ', column2)
                        if column1 != column2 and not ((column1 in self.meta[table][column2]['similar']) or (column2 in self.meta[table][column1]['similar'])):                            
                            # print('pass 2 ', column1, ' ', column2)
                            # print(len(self.databasedata[table][column1]))
                            sim = similaritychecker(self.databasedata[table][column1], self.databasedata[table][column2])
                            # print(sim.result)
                            if sim.result:
                                self.meta[table][column1]['similar'].append(column2)
                                self.meta[table][column2]['similar'].append(column1)

class similaritychecker:
    def __init__(self, lista, listb):
        self.lista = lista
        self.listb = listb
        self.threshold = 7
        self.tenpercentile = int(min(len(lista), len(listb)))
        self.result = self.check()
    
    def check(self):
        checkunique = []
        similarityhit = 0
        k = 1
        for element in self.lista:
            if k > self.tenpercentile:
                break
            k += 1
            if element in self.listb:
                similarityhit += 1
                if not element in checkunique:
                    checkunique.append(element)
                if similarityhit >= self.threshold:
                    return True
        return False
