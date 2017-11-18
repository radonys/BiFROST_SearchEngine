import numpy as np
from nltk.tokenize import sent_tokenize,RegexpTokenizer

rtokenizer=RegexpTokenizer(r'\w+')

def row_normalize(A):

    return (A.transpose()*(1/A.sum(1))).transpose()


def idf(word):

    return 0.5


def idf_modified_cosine(str1,str2):

    x=rtokenizer.tokenize(str1)
    y=rtokenizer.tokenize(str2)

    num=den1=den2=0.0

    print list(set(x+y))

    for w in list(set(x+y)):
        num+=x.count(w)*y.count(w)*(idf(w)**2)

    for xi in x:
        den1+=(x.count(xi)*idf(xi))**2
    den1=np.sqrt(den1)

    for yi in y:
        den2+=(y.count(yi)*idf(yi))**2
    den2=np.sqrt(den1)

    result=num/(den1*den2)
    return result


def create_centrality_matrix(f):

    str=f.read()
    sentences=sent_tokenize(str)
    words=list(set(rtokenizer.tokenize(str)))

    N=len(sentences)

    centrality_matrix=np.zeros([N,N])

    for i,senti in enumerate(sentences):
        for j,sentj in enumerate(sentences):
            centrality_matrix[i][j]=idf_modified_cosine(senti,sentj)

    centrality_matrix=row_normalize(centrality_matrix)

    return centrality_matrix


if __name__ == '__main__':

    f=open('test.txt')
    C=create_centrality_matrix(f)
    print C
