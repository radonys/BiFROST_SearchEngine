import os
import importlib
import argparse
import sys

import text_extract as TE

def main(args):

    for folder,subfolders,files in os.walk(args.data_dir):
        
        for filename in files:
    
            text_data = TE.extract(os.path.join(os.path.abspath(folder),filename))
            #print text_data
            if text_data!=None:
                processed=TE.textprocess(text_data)
                print processed

        '''for word in processed:
            
            term=word
            document=os.path.join(os.path.abspath(folder),filename)'''

def parse_arguments(argv):
    	
	parser = argparse.ArgumentParser()
	parser.add_argument('--data_dir', type=str, help='Path to the data directory', default='/Users/yashsrivastava/Documents/Files/IR/Datasets/en.docs.2011')  
	return parser.parse_args(argv)

if __name__ == '__main__':
	
	main(parse_arguments(sys.argv[1:]))