import sys
import collections

import indexing
import text_extract as TE

def query_vector(query):

    words = collections.defaultdict(dict)
    words_tfidf = collections.defaultdict(dict) #Stores TF, IDF & TF-IDF.
    cosinevector = dict()

    processed = TE.textprocess(query)

    for word in processed:
                    
        term = word
        document = query
        positions = [index for index, value in enumerate(processed) if value == term]
        words[term][document] = positions
    
    indexing.dataload(words_tfidf,'data/tfidf_index.json')
    print words_tfidf.get(u'Zlatan')
    indexing.cosine_vector(query,cosinevector,words_tfidf,processed)

    print cosinevector[query]

query = raw_input()
query_vector(query)