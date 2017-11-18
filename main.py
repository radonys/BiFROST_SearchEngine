import os
import importlib
import argparse
import sys
import collections

import indexing

def main(args):

    words = collections.defaultdict(dict) #Stores words, documents containing them and positional indices.
    words_tfidf = collections.defaultdict(dict) #Stores TF, IDF & TF-IDF.
    filecount = 0

    #If no data is given as input.
    if args.data_dir==None and args.tfidf_json_file==None:
        
        sys.exit("No Data Available")

    #TF-IDF data is given.
    elif args.tfidf_json_file!=None:
        indexing.dataload(words_tfidf,args.tfidf_json_file)

    #Text documents are given.
    elif args.data_dir!=None:
        filecount = indexing.index(words,args.data_dir)
        indexing.tfidf(words,words_tfidf,filecount)
        indexing.datasave(words_tfidf)

    if words_tfidf:
        
        print "Success"
    
def parse_arguments(argv):
    
    parser = argparse.ArgumentParser()

    parser.add_argument('--data_dir', type=str, help='Path to the data directory', default=None)
    parser.add_argument('--tfidf_json_file', type=str, help='Path to the TF-IDF JSON file', default=None)

    return parser.parse_args(argv)

if __name__ == '__main__':
	
	main(parse_arguments(sys.argv[1:]))