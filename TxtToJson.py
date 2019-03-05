'''
Created on Mar 4, 2019

@author: filipe
'''

from glob import glob
import re
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
                #out = '{ "id" : \"' + str(777) + '\", "text": \"' + text + '\"}'
                out = txtToJson.textTojson(text)  
                writer.write(out)
        jsonname = glob(textDir + "/*.json")
        for jname in enumerate(jsonname):
            filename = ntpath.basename(fname[1]).split(".")[0] + ".json"
            new_path = os.path.join(jsonDir, filename)
            shutil.move(jname[1], new_path)
    
    @staticmethod
    def textTojson(text,jname):
        print ("Converting Essay Text to Json...")
        with open(jname, 'w') as writer:
            out = '{ "id" : \"' + str(777) + '\", "text": \"' + text + '\"}'
            writer.write(out)
        return out