'''
Created on Mar 4, 2019

@author: filipe
'''

from glob import glob
import argparse, json, re
import os
import shutil, ntpath

class txtToJson(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    @staticmethod
    def ttJson(textDir, jsonDir, directory=False):
        WORD = re.compile(r'[\w\.]+')
        if directory:
            name = glob(textDir + "/*.txt")
        else:
            name = [name]
        for fname in enumerate(name):
            jname = fname[1].split(".")[0] + ".json"
            with open(jname, 'w') as writer:
                text = open(fname[1], 'r').read()
                text = " ".join(WORD.findall(text))
                out = '{ "id" : \"' + str(777) + '\", "text": \"' + text + '\"}'  
                writer.write(out)
        jsonname = glob(textDir + "/*.json")
        for jname in enumerate(jsonname):
            filename = ntpath.basename(fname[1]).split(".")[0] + ".json"
            new_path = os.path.join(jsonDir, filename)
            shutil.move(jname[1], new_path)
        print ("Done with converting")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--dir", type=str, help='please type the name of the directory which have your .txt file : \
                            python cnv.py -d "temp dir"')

    parser.add_argument("-f", "--file", type=str, help='please type the name of the file which have want to convert into json : \
                            python cnv.py -f "tempfile.txt"')

    parser.add_argument("-c", "--clear", type=int, choices=[0,1], default=0, help="You want to delete all of the \
                            .txt file , 0 for yes, 1 for no")

    args = parser.parse_args()

    if args.dir:
        ttJson(args.dir, directory=True)

    if args.file:
        ttJson(args.file)    