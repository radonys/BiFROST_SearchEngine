import os
import importlib
import sys
import collections
import json
import math

import text_extract as TE

#Indexing words.
def index(words,filepath):

    total_files = 0
    flag = 0

    for folder,subfolders,files in os.walk(filepath):
        
        for filename in files:
    
            total_files = total_files + 1
            text_data = TE.extract(os.path.join(os.path.abspath(folder),filename))
            document = None

            if text_data != None:
                
                processed = TE.textprocess(text_data)
                
                for word in processed:
                    
                    term = word
                    document = os.path.join(os.path.abspath(folder),filename)
                    positions = [index for index, value in enumerate(processed) if value == term]
                    words[term][document] = positions
            
            print "File : ", total_files, " done. File Path : ", document

            if total_files==10000:
                flag = 1
                break
        
        if flag==1:
            break

    return total_files

#Loading Data
def dataload(words,filepath):

    file = open(filepath,'r')
    words.update(json.load(file))
    file.close()

#Saving Data
def datasave(words,i):

    if i==1:
        file = open("data/tfidf_index.json",'w')
    elif i==2:
        file = open("data/text_doc.json",'w')
    elif i==3:
        file = open("data/positions.json","w")

    json.dump(words,file)
    file.close()

#Calculating TF-IDF
def tfidf(words,words_tfidf,filecount):

    for word in words:

        inverse_ratio = filecount/len(words[word])
        idf = math.log(inverse_ratio,10)

        for doc in words[word]:

            tf = len(words[word][doc])
            tf_idf = (1 + math.log(tf))*idf
            words_tfidf[word][doc] = (tf,idf,tf_idf)

def is_empty(any_structure):
    
    if any_structure:
        return False

    else:
        return True

def cosine_vector(words,processed,filepath):

    cosinevector = collections.defaultdict(dict)

    for folder,subfolders,files in os.walk(filepath):

        for filename in files:
                
            document = os.path.join(os.path.abspath(folder),filename)
            cosinevector[document] = list()

            for word in sorted(set(processed)):
                
                if document in words[word]:
                    cosinevector[document].append(words[word][document][2])
                else:
                    cosinevector[document].append(0)

    return cosinevector

def query_tfidf(processed,words):
    
    vector = list()
    
    for word in sorted(set(processed)):
        for doc in words[word]:
            
            tf_idf = (1+math.log(processed.count(word)))*(words[word][doc][1])
            vector.append(tf_idf)

    return vector

def score_calculator(cosinevector,queryvector):
    
    scorevector = collections.defaultdict(dict)

    for doc in cosinevector:
        
        docvector = cosinevector[doc]
        score = 0

        dot_product = sum(p*q for p,q in zip(docvector, queryvector))
        magnitude = math.sqrt(sum([val**2 for val in docvector])) * math.sqrt(sum([val**2 for val in queryvector]))
        
        if not magnitude:
            score = 0
        else:
            score = dot_product/magnitude

        scorevector[doc] = score
    
    return scorevector

