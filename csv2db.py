import sqlite3 as sqlite
import json
import pandas as pd
import os

typedict = {
    'text':['string', 'varchar', 'character', 'text'],
    'integer':['number', 'integer']
}

class c2d:
    def __init__(self, metapath, dbpath, csvpath):
        with open(metapath, 'r') as file:
            self.meta = json.load(file)
        self.con = sqlite.connect(dbpath)
        self.data = self.loaddata(csvpath)
        self.generatedb()
        self.pushdata()

    def loaddata(self, filepath):
        df = pd.read_csv(filepath)
        filename, ext = os.path.splitext(filepath)
        keylist = list(self.meta[filename.split('/')[-1]].keys())
        data = {filename.split('/')[-1]: {keylist[i] : list(df[keylist[i]]) for i in range(len(keylist))}}
        return data

    def generatedb(self):
        cursor = self.con.cursor()
        metadict = self.meta
        for table in metadict:
            query = "CREATE TABLE IF NOT EXISTS " + table + "(id INTEGER PRIMARY KEY"
            for column in metadict[table]:
                 query += ", " + column + " " + self.gettype(metadict[table][column]['type']).upper()
            query += ");"
            cursor.execute(query)
            self.con.commit()

    def pushdata(self):
        metadata = self.meta
        data = self.data
        cursor = self.con.cursor()
        for table in self.meta:
            columns = '('
            whats = 'VALUES('
            columnnames = []
            for column in self.meta[table]:
                columns += column + ','
                whats += '?,'
                columnnames.append(column)
            columns = columns[:-1]
            whats = whats[:-1]
            columns += ')'
            whats += ')'
            # for i in range(len(self.data[table][columnnames[0]])):
            #     datatopass = [self.data[table][columnnames[k]][i] for k in range(len(columnnames))]                
            #     datatopass = tuple(datatopass)
            #     query = "INSERT INTO " + table + columns + whats
            #     cursor.execute(query ,(datatopass))
        self.con.commit()
        cursor.close()
        self.con.close()


    def gettype(self, type):
        type = type.lower()
        global typedict
        for t in typedict:
            if type in typedict[t]:
                return t
        return type