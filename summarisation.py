import numpy as np
from nltk.tokenize import sent_tokenize,RegexpTokenizer

def row_normalize(A):

    return (A.transpose()*(1/A.sum(1))).transpose()


def idf(word):

    return 0.5


def idf_modified_cosine(str1,str2):

    rtokenizer=RegexpTokenizer(r'\w+')
    x=rtokenizer.tokenize(str1)
    y=rtokenizer.tokenize(str2)

    num=den1=den2=0.0

    for w in list(set(x+y)):
        num+=x.count(w)*y.count(w)*(idf(w)**2)

    for xi in x:
        den1+=(x.count(xi)*idf(xi))**2

    for yi in y:
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

    print centrality_matrix
    return centrality_matrix


def LexRank(f):

    str=f.read()
    sentences=sent_tokenize(str)
    N=len(sentences)
    M=create_centrality_matrix(sentences)
    d=0.85



if __name__ == '__main__':

    f=open('test.txt')
    LexRank(f)
