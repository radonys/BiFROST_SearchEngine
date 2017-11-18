import os
import importlib
import argparse
import sys
import collections

import indexing

def main(args):

    words = collections.defaultdict(dict)
    words_idf = dict()

    indexing.index(words,args.data_dir)

def parse_arguments(argv):
    	
	parser = argparse.ArgumentParser()
	parser.add_argument('--data_dir', type=str, help='Path to the data directory', default='/Users/yashsrivastava/Documents/Files/IR/Datasets/en.docs.2011')  
	return parser.parse_args(argv)

if __name__ == '__main__':
	
	main(parse_arguments(sys.argv[1:]))