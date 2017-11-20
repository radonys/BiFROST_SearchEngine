import numpy as np
import heapq
import json
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk import PorterStemmer
from nltk.corpus import stopwords
import normalization
import nltk

import text_extract as TE

nltk.data.path.append("/Users/yashsrivastava/Documents/Files/IR/nltk_data")


def summarize():
    
    stop_words=list(set(stopwords.words("english")))
    
    f=open('data/text_doc.json','r')
    text=json.load(f)
    f.close()

    f=open('data/tfidf_index.json','r')
    indices=json.load(f)
    f.close()

    all_summaries=dict()

    def row_normalize(A):

        return (A.transpose()*(1/A.sum(1))).transpose()


    def idf(word):

        stemmer=PorterStemmer()
        word=stemmer.stem(word)

        #global indices
        idf_value=indices[word].values()[0][1]
        return idf_value


    def idf_modified_cosine(str1,str2):

        x = TE.tokenize(str1)
        y = TE.tokenize(str2)

        num=den1=den2=0.0

        for w in list(set(x+y)):
            if w not in stop_words:
                num+=x.count(w)*y.count(w)*(idf(w)**2)

        for xi in x:
            if xi not in stop_words:
                den1+=(x.count(xi)*idf(xi))**2

        for yi in y:
            if yi not in stop_words:
                den2+=(y.count(yi)*idf(yi))**2

        result=num/np.sqrt(den1*den2)
        return result


    def create_centrality_matrix(sentences):

        N=len(sentences)

        centrality_matrix=np.zeros([N,N])

        for i,senti in enumerate(sentences):
            for j,sentj in enumerate(sentences):
                centrality_matrix[i][j]=idf_modified_cosine(senti,sentj)

        centrality_matrix=row_normalize(centrality_matrix)

        return centrality_matrix


    def LexRank(str):

        sentences=sent_tokenize(str)
        N=len(sentences)
        M=create_centrality_matrix(sentences)
        d=0.85

        page_rank=np.zeros(N)
        degree=np.zeros(N)

        for u in range(N):
            for v in range(N):
                if u!=v and M[u][v]>0:
                    degree[u]+=M[u][v]

        for i in range(100):
            for u in range(N):
                rank=0
                for v in range(N):
                    if M[u][v]>0 and u!=v:
                        rank+=(M[u][v]*page_rank[v]/degree[v])
                page_rank[u]=(1-d)/N+d*rank

        summary=''
        
        for i in heapq.nlargest(2,range(N),page_rank.take):
            summary+=sentences[i]

        return summary

    for i in range(len(text)):
        
        txt=text.values()[i]
        docname=text.keys()[i]

        summary=LexRank(normalization.normalize(txt))
        all_summaries[docname]=summary

    f=open('data/summaries.json','w')
    json.dump(all_summaries,f)
    f.close()

    print ("Summarization Done")
