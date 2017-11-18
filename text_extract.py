import os
from bs4 import BeautifulSoup
import nltk
from nltk import word_tokenize
from nltk import PorterStemmer
from nltk.corpus import stopwords

#tokenise,remove punctuation and convert to lowercase
def tokenize(f):
    
    processed=[]

    for word in word_tokenize(f):
        if word.isalnum():
            processed.append(word.lower())

    return processed

#stemming
def stem_words(f):

	stemmer=PorterStemmer()
	processed=tokenize(f)

	for i in range(len(processed)):
		processed[i]=stemmer.stem(processed[i])

	return processed

#remove stopwords
def remove_stopwords(f):
    
    processed=stem_words(f)
    
    for word in processed:
        if word in stopwords.words('english'):
            processed.remove(word)
    
    return processed

#preprocess
def textprocess(data):
    
    nltk.data.path.append("/Users/yashsrivastava/Documents/Files/IR/nltk_data")
    
    processed=remove_stopwords(data)
    return processed

#text-extraction
def extract(file):
    
    with open(file, 'r') as myfile:
        data=myfile.read().replace('\n', '')

    soup = BeautifulSoup(data, "html.parser")

    if soup.find('text')!=None:
        return soup.find('text').text        

