'''
Created on Mar 4, 2019

@author: filipe
'''

from TxtToJson import txtToJson
import os, sys
from glob import glob
import pytextrank
import networkx as nx
from summary import summary
import pylab as plt
import re, ntpath

if __name__ == '__main__':
    plotGraph = False  #For debugging purposes
    essayDir = "essays"
    jsonDir = "jsonessays"
    summaryDir = "summaries"
    path = os.path.dirname(sys.argv[0])
    essay_path = os.path.join(path, essayDir)
    json_path = os.path.join(path, jsonDir)
    summary_path = os.path.join(path, summaryDir)
    
    ### TUNNING PARAMETERS
    wordlimit = 100
    phraselimit = 10
    
    #Delete left over processed files
    name = glob(json_path + "/*.json")
    for fname in enumerate(name):
        try:
            os.remove(fname[1])
        except OSError:
            pass
    
    #Repeat process for all essay files
    name = glob(essay_path + "/*.txt")
    WORD = re.compile(r'[\w\.]+')
    for fname in enumerate(name):   
        text = open(fname[1], 'r').read()
        text = " ".join(WORD.findall(text)) 
        filename = ntpath.basename(fname[1]).split(".")[0] + "_o2.json"
        path_stage1 = fname[1].split('.txt')[0] + '_o1.json'
        summary.generateGraph(text, filename, json_path, plotGraph=False)
        
        #Generate summary    
        path_stage2 = os.path.join(json_path, filename)
        path_stage3 = path_stage2.replace('o2', 'o3')
        path_stage1 = path_stage2.replace('o2', 'o1')
        summarytext, keyconcepts = summary.summarize(path_stage1, path_stage2, path_stage3, 
                                                     wordlimit=wordlimit, phraselimit=phraselimit)
        filename = ntpath.basename(fname[1]).split(".")[0] + '_summary.txt'
        summarypath = os.path.join(summaryDir, filename)
        with open(summarypath, 'w') as f:
            f.write(summarytext)
        #Generate summary concept map
        filename = ntpath.basename(fname[1]).split(".")[0] + "_o2.json"
        summary.generateGraph(summarytext, filename, summary_path, plotGraph=True)

