'''
Created on Mar 6, 2019

@author: filipe
'''
from util import util
import os
import json
import numpy as np
from nltk.tokenize import sent_tokenize
from operator import itemgetter

class conceptmap(object):
    '''
    classdocs
    '''
    def __init__(self, params):
        '''
        Constructor
        '''
   
    @staticmethod
    def open_text_json(jsonFile):
        jsontext = []
        with open(jsonFile) as f:
            for line in f:
                jsontext.append(json.loads(line))
        return jsontext
        
    @staticmethod
    def retrieve_ngram_params(jsonobj):    
        ids = np.array([d['ids'] for d in jsonobj])
        text = np.array([d['text'] for d in jsonobj])
        pos = np.array([d['pos'] for d in jsonobj])
        ngramids = []
        ngramtext= []
        ngrampos = []
        for i in range (0, ids.shape[0]):
            if (len(ids[i])>1):
                ngramids.append(ids[i])
                ngramtext.append(text[i])
                ngrampos.append(pos[i])
        return ngramids, ngramtext, ngrampos
    
    @staticmethod
    def get_ngram_sentences(text, ngramtext):
        ngramsentences = []
        sentences = sent_tokenize(text)
        for element in ngramtext:
            for sentence in sentences:
                if (element in sentence): ngramsentences.append(sentence)
        singlegramsentences = list(set(sentences) - set(ngramsentences))        
        return ngramsentences, singlegramsentences
    
    @staticmethod
    def get_top_node(jsonobj):
        ids = np.array([d['ids'] for d in jsonobj])
        counts = np.array([d['count'] for d in jsonobj])
        texts = np.array([d['text'] for d in jsonobj])
        idcount = []
        for i in range(0,len(ids)):
            idcount.append([ids[i], counts[i], texts[i]])
        idcount.sort(key=itemgetter(1)) #sort on count
        idcount.reverse()
        continueTrying = True
        while (len(ids)!=0 and continueTrying):            
            nextid = np.array([idcount.pop(0)[0][0]])
            for line in idcount:
                testid = np.array(line[0])
                if ((np.sum((nextid == testid))) == nextid.shape[0]):
                    continueTrying = False
                    break             
        return line[2]
if __name__ == '__main__':
    jsonFile = os.path.join(util.get_path('jsonessays'), 'rubric_o2.json')
    summaryFile = os.path.join(util.get_path('rubric'), 'rubric.txt')
    with open(summaryFile, 'r') as f:
        summarytext = f.read()
    jsonobj = conceptmap.open_text_json(jsonFile)
    ngramids, ngramtext, ngrampos = conceptmap.retrieve_ngram_params(jsonobj)
    topconcept = conceptmap.get_top_node(jsonobj)
    ngramsentences, singlegramsentences = conceptmap.get_ngram_sentences(summarytext, ngramtext)
    pass