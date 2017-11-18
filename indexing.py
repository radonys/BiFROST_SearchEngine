import os
import importlib
import sys
import collections
import json
import math

import text_extract as TE

def index(words,filepath):

    total_files = 0

    for folder,subfolders,files in os.walk(filepath):
        
        for filename in files:
    
            total_files = total_files + 1
            text_data = TE.extract(os.path.join(os.path.abspath(folder),filename))

            if text_data != None:
                
                processed = TE.textprocess(text_data)

                for word in processed:
                    
                    term = word
                    document = os.path.join(os.path.abspath(folder),filename)
                    positions = [index for index, value in enumerate(processed) if value == term]
                    words[term][document] = positions
            
            print "File : ", total_files, " done."

    return total_files

def dataload(words,filepath):

    file = open(filepath,'r')
    words = json.load(file)
    file.close()

def datasave(words):

    file = open("index_table.json",'w')
    json.dump(words,file)
    file.close()

def tfidf(words,words_tfidf,filecount):

    for word in words:

        inverse_ratio = filecount/len(words[word])
        idf = math.log(inverse_ratio,10)

        for doc in words[word]:

            tf = len(words[word][doc])
            tf_idf = (1 + math.log(tf))*idf
            words_tfidf[word][doc] = (tf,idf,tf_idf)