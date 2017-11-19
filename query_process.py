import sys
import os
import collections

import indexing
import text_extract as TE

def one_term_query(query,words):
    
    doc_list = []

    if len(query)==1:
        for term in query:
            if term in words:
                for doc in words[term]:
                    doc_list.append(doc)
    
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
    
    doc_list = []

    for term in query:
        if term not in words:
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
    cosinevector.update(indexing.cosine_vector(words_tfidf,processed,'/Users/yashsrivastava/Desktop/raw'))

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
    elif query_type=='FTQ':
        return free_text_query(words_query,words_doc)
    elif query_type=='PQ':
        return phrase_query(words_query,words_doc)
