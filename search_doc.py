import os
import json
import time

from nltk import PorterStemmer

f=open('index_table.json','r')
#start=time.time()
ind_table=json.load(f)
for word in ind_table.keys():
	if word=='both' or word=='Both':
		print word 
#end=time.time()
#print end-start

search_term=raw_input("Enter search term:")
search_words=search_term.split()

doc_list=[]
stemmer=PorterStemmer()

first_word=stemmer.stem(search_words[0])
if first_word in ind_table and ind_table[first_word] not in doc_list:
	#print ind_table[first_word]
	doc_list+=ind_table[first_word]

#print doc_list

'''for word in search_words:
	word=stemmer.stem(word)
	if word in ind_table and ind_table[word] not in doc_list:
		doc_list+=ind_table[word]'''

for doc in doc_list:
	f=open(doc)
	#print ('\n').join(f.readlines())

