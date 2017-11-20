import sys
import os
import collections
import json

import indexing
import text_extract as TE

f=open('data/tfidf_index.json','r')
doc_tfidf = json.load(f)
f.close()

def one_term_query(query,words):
    
    doc_list = dict()

    if len(query)==1:
        for term in query:
            if term in words:
                for doc in words[term]:
                    doc_list[doc] = doc_tfidf[term][doc][2]

    return doc_list

def free_text_query(query,words):
    
    doc_list = set()

    if len(query)>0:
        for term in query:
            if term in words:
                for doc in words[term]:
                    doc_list.add(doc)

    return list(doc_list)

def phrase_query(query,words):
    
    doc_list = dict()
    docs = []

    for term in query:
        if term not in words:
            return doc_list

    query_docs = dict()
    
    for term in query:
        if term in words:
            query_docs[term] = list(words[term].keys())

    common_docs = set()

    for term in query:
        common_docs = set(query_docs[term])
        break

    for term in query_docs:
        
        common_docs.intersection(query_docs[term])

        if indexing.is_empty(common_docs):
            return list(common_docs)
    
    common_docs = list(common_docs)

    for doc in common_docs:
        
        count = 0
        flag = 0
        position_set = set()

        for term in query:
            
            if count==0:
                position_set = set(words[term][doc])

            else:
                position_set.intersection([x-count for x in words[term][doc]])

            if indexing.is_empty(position_set):
                flag = 1
                break

            count = count + 1
        
        if flag==0:
            docs.append(doc)
    
    for doc in docs:
        
        doc_list[doc] = 0

        for term in query:
            if term in words:
                doc_list[doc] = doc_list[doc] + doc_tfidf[term][doc][2]
    
    return doc_list

def query_vector(query):

    words = collections.defaultdict(dict)
    words_tfidf = collections.defaultdict(dict)
    cosinevector = collections.defaultdict(dict)
    scorevector = collections.defaultdict(dict)

    processed = TE.textprocess(query)

    for word in processed:
                    
        term = word
        document = query
        positions = [index for index, value in enumerate(processed) if value == term]
        words[term][document] = positions
    
    indexing.dataload(words_tfidf,'data/tfidf_index.json')

    file = open('data/path.json','r')
    path = json.load(file)
    file.close()
    cosinevector.update(indexing.cosine_vector(words_tfidf,processed,path))

    queryvector = indexing.query_tfidf(processed,words_tfidf)

    scorevector.update(indexing.score_calculator(cosinevector,queryvector))

    return scorevector

def query_position(query):

    words_query = collections.defaultdict(dict)
    words_doc = collections.defaultdict(dict)

    query_type = TE.query_type(query)

    processed = TE.textprocess(query)

    for word in processed:
                    
        term = word
        document = query
        positions = [index for index, value in enumerate(processed) if value == term]
        words_query[term][document] = positions

    indexing.dataload(words_doc,'data/positions.json')

    if len(words_query)==1:
        return one_term_query(words_query,words_doc)
    elif query_type=='PQ':
        return phrase_query(words_query,words_doc)
    '''elif query_type=='FTQ':
        return free_text_query(words_query,words_doc)'''