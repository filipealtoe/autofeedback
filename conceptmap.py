'''
Created on Mar 6, 2019

@author: filipe
'''
from util import util
import os
import json
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
from operator import itemgetter
from visualize import visualize

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
        '''
        it gets the top ranked element
        '''
        #=======================================================================
        # ids = np.array([d['ids'] for d in jsonobj])
        # counts = np.array([d['count'] for d in jsonobj])
        # texts = np.array([d['text'] for d in jsonobj])
        # idcount = []
        # for i in range(0,len(ids)):
        #     idcount.append([ids[i], counts[i], texts[i]])
        # idcount.sort(key=itemgetter(1)) #sort on count
        # idcount.reverse()
        # continueTrying = True
        # while (len(ids)!=0 and continueTrying):            
        #     nextid = np.array([idcount.pop(0)[0][0]])
        #     for line in idcount:
        #         testid = np.array(line[0])
        #         if ((np.sum((nextid == testid))) == nextid.shape[0]):
        #             continueTrying = False
        #             break             
        # return line[2]
        #=======================================================================
        return jsonobj[0]
    
    
    
    @staticmethod
    def process_sentence(sentence, jsonobj):
        starttoken = '{'
        endtoken = '}'
        processedtext = sentence.lower()
        processedtext = word_tokenize(processedtext)
        concepts = []
        #Replace all concepts with their tag ids and pos
        for word in processedtext:
            for concept in jsonobj:
                if (concept['text'] == word):
                    concepts.append(concept)
        #create node triplets [n (or v-n), v, n]                
        sentencetriplets = conceptmap.create_triplets(concepts)
        return sentencetriplets
    
    @staticmethod
    def create_triplets(concepts):
        '''
        create node triplets [n , v, n] or [v, n, n] where n, v, n are full concept structures
        '''
        noum = 'n'
        propernoum = 'np'
        verb = 'v'
        triplets = []
        triplet = []
        while(len(concepts)> 1):
            concept = concepts.pop(0)
            #if starts with verb, finds the noun associated with it and invert order to create triplet
            if (concept['pos'][0] == verb):
                #Gets the np pos associated with initial verb
                for nextconcept in concepts:
                    if(nextconcept['pos'][0] == noum):
                        nextconcept = concepts.pop(0)
                        triplet.append(nextconcept)
                        triplet.append(concept)
                        break
                #Gets next noun to complete triplet
                for nextconcept in concepts:
                    if(nextconcept['pos'][0] == noum):
                        triplet.append(nextconcept)
                        break
                triplets.append(triplet)
                triplet = []
            #If starts with noun, follows the usual path
            elif (concept['pos'][0] == noum):
                #if immediately next concept is another noun, associate the two noums and move on to processing next noum
                if(concepts[0]['pos'][0] == noum):
                    triplet.append(concept)
                    triplet.append(None)
                    triplet.append(concepts[0])
                    triplets.append(triplet)
                    triplet = []
                    continue
                #Gets the verb associated with initial verb
                for nextconcept in concepts:
                    if(nextconcept['pos'][0] == verb):
                        nextconcept = concepts.pop(0)
                        triplet.append(concept)
                        triplet.append(nextconcept)
                        break
                #Gets next noun to complete triplet
                for nextconcept in concepts:
                    if(nextconcept['pos'][0] == noum):
                        nextconcept = concepts.pop(0)
                        triplet.append(nextconcept)
                        break
                triplets.append(triplet)
                #if next concept is another noum, it needs to be associated to the same previous verb    
                for nextconcept in concepts:
                    if(nextconcept['pos'][0] == noum):
                        nexttriplet = triplet.copy()
                        nexttriplet[2] = nextconcept
                        triplets.append(nexttriplet)
                        triplet = []
                        nexttriplet = []
                        break
            
        return triplets
    
    @staticmethod
    def build_graph(triplets):
        pass
    
if __name__ == '__main__':
    jsonFile = os.path.join(util.get_path('jsonessays'), 'rubric_o2.json')
    summaryFile = os.path.join(util.get_path('rubric'), 'rubric.txt')
    with open(summaryFile, 'r') as f:
        summarytext = f.read()
    jsonobj = conceptmap.open_text_json(jsonFile)
    ngramids, ngramtext, ngrampos = conceptmap.retrieve_ngram_params(jsonobj)
    topconcept = conceptmap.get_top_node(jsonobj)
    ngramsentences, singlegramsentences = conceptmap.get_ngram_sentences(summarytext, ngramtext)
    allsentences = ngramsentences + singlegramsentences
    sentencetriplets = []
    for sentence in allsentences:
        sentencetriplets += (conceptmap.process_sentence(sentence, jsonobj))
    visualize.plotGraph(sentencetriplets)
    pass