import os
from bs4 import BeautifulSoup
import nltk
from nltk import word_tokenize
from nltk import PorterStemmer
from nltk.corpus import stopwords
import normalization

#Tokenise,remove punctuation and convert to lowercase
def tokenize(f):

    processed=[]

    for word in word_tokenize(f):
        if word.isalnum():
            processed.append(word.lower())

    return processed

#Normalization
def normalize(f):
    
     f = normalization.normalize(f)
     processed = tokenize(f)
     
     return processed

#Stemming
def stem_words(f):

	stemmer=PorterStemmer()
	processed=normalize(f)

	for i in range(len(processed)):
		processed[i]=stemmer.stem(processed[i])

	return processed

#Remove stopwords
def remove_stopwords(f):
    
    processed=stem_words(f)
    
    for word in processed:
        if word in stopwords.words('english'):
            processed.remove(word)
    
    return processed

#Preprocess
def textprocess(data):
    
    nltk.data.path.append("/Users/yashsrivastava/Documents/Files/IR/nltk_data")

    processed=remove_stopwords(data)
    return processed

#Text-Extraction
def extract(file):
    
    with open(file, 'r') as myfile:
        data=myfile.read().replace('\n', '')

    soup = BeautifulSoup(data, "html.parser")

    if soup.find('text')!=None:
        return soup.find('text').text        

