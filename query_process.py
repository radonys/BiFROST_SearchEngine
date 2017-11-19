import sys
import os
import collections

import indexing
import text_extract as TE

def query_vector(query,path):

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

    
    
