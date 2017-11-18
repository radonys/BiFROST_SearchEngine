import os
import importlib
import argparse
import sys
import collections

import indexing

def main(args):

    words = collections.defaultdict(dict)
    words_idf = dict()

    if args.json_file==None and args.data_dir==None:
        
        sys.exit("No Data Available")

    elif args.json_file!=None:
        indexing.dataload(words,args.json_file)

    elif args.data_dir!=None:
        indexing.index(words,args.data_dir)

    indexing.datasave(words)


def parse_arguments(argv):
    
    parser = argparse.ArgumentParser()

    parser.add_argument('--data_dir', type=str, help='Path to the data directory', default=None)
    parser.add_argument('--json_file', type=str, help='Path to the JSON file', default=None) 

    return parser.parse_args(argv)

if __name__ == '__main__':
	
	main(parse_arguments(sys.argv[1:]))