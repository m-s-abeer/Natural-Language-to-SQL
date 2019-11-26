#imports
from flask import Flask as flask, render_template, request, send_from_directory, jsonify
from importlib import reload
import meta_generator as mg
import json
import query
import os
import pandas as pd
import csv2db
import signal
import abeerQuery as aq
import socket

app = flask(__name__,static_url_path='', static_folder='templates/')
app.config['UPLOAD_FOLDER'] = 'uploads/'


#global variables
dbmetadata = {}
filepath = ''
nlp = query.connectserver('http://corenlp.run/', port=80)


#global methods
def loadmeta(path):
    global dbmetadata
    with open(path, 'rb') as file:
        dbmetadata = json.load(file)

def reloadLibs():
    reload(mg)
    reload(query)

def loadalldata():
    global filepath
    global dbmetadata
    filename, ext = os.path.splitext(filepath)
    print(filename)
    print(filename.split('/')[-1])
    if ext == '.db':
        # return query.loaddatabasedata(filepath)
        pass
    elif ext == '.csv':
        converter = csv2db.c2d('meta.json', filename+'.db', filepath)
        os.remove(filepath)
        filepath = filename+'.db'
        # return query.loaddatabasedata(filepath)
        loadmeta('meta.json')

def prepareengine():
    global dbmetadata
    global nlp
    query.databasemetainfo = dbmetadata
    query.databasedata = loadalldata()
    # query.stringwordlist = query.stringDataList()
    # nlp = query.connectserver('http://corenlp.run/', port=80)
    # while nlp == '':
    #     nlp = query.connectserver('http://corenlp.run/', port=80)
    # print(type(nlp))
    # nlp = query.runserver()

def getColumnNames():
    global dbmetadata
    print("Printing column names from meta.json")
    # print(dbmetadata)
    firstTable = dbmetadata[list(dbmetadata.keys())[0]]
    print(firstTable)
    return [x for x in firstTable.keys()]

#routing functions

@app.route('/shutdown', methods=['GET'])
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    print('Quitting! Bye!')
    global nlp
    if nlp != '':
        nlp.close()
    func()
    return 'Shut Down'

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/upload',methods=['POST'])
def upload():
    global filepath
    print("uploading")
    file=request.files['file']
    filename=file.filename.split('.')[0]+'_new.'+file.filename.split('.')[-1]
    path=app.config['UPLOAD_FOLDER']+'/'+filename
    file.save(path)
    filepath = path
    mg.generator(path)
    loadmeta('meta.json')
    prepareengine()
    return jsonify({"path":path})

@app.route('/download/<filename>')
def download(filename):
    print('DOWNLOAD='+filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/getmeta', methods=['GET'])
def returnmeta():
    loadmeta('meta.json')
    global dbmetadata
    return jsonify(dbmetadata)

@app.route('/query', methods=['POST'])
def queryanalyzer():
    global dbmetadata
    global nlp
    global filepath
    # nlp = query.connectserver('http://corenlp.run/', port=80)
    finder = aq.aggQueryFinder()
    print("On function query: ", end='')
    print(type(nlp))
    nlq = request.form['query']
    originalquery = nlq
    # loadmeta('meta.json')
    columns = getColumnNames()
    finder.updateColumnNames(columns)
    finder.query(originalquery)
    abeerSql = finder.getSqlString(list(dbmetadata.keys())[0])
    print(abeerSql)
    # nlq, lemmadics = query.getlemma(nlp, nlq)
    # nlq, hashmap = query.dbMatch(nlq)
    # print(list(dbmetadata.keys())[0])
    # sql = query.generateprimaryquery(nlq, hashmap, list(dbmetadata.keys())[0])
    # analysis = query.getanalysis(nlp, originalquery)
    # query.printdependency()
    # tablerelation = query.printcurrenttablerelationfromanalysis()
    # intersql = query.intermediatesql(sql)
    return jsonify({'nlq': nlq, #'hash': hashmap,# 'sql': sql,
            # 'dependencies' : query.currentsentencedependencies,
            # 'parserdepend': tablerelation,
            # 'data': query.runquery(intersql, filepath),
            # 'intersql': intersql,
            'abeerSql': abeerSql})


@app.route('/filelist', methods=['GET'])
def retFileList():
    return jsonify(os.listdir('uploads'))

@app.route('/filechange', methods=['POST'])
def changeFile():
    global filepath
    filepath = request.form['file']
    print(filepath)
    reloadLibs()
    mg.generator(filepath)
    loadmeta('meta.json')
    prepareengine()
    return 'File Changed'

# reloadLibs()
# app.run(port=2211)

host_name = socket.gethostname() 

if __name__ == '__main__':
    reloadLibs()
    if host_name=="msabeer":
        app.run(debug='True')
    else:
        app.run()
