'''
Created on Mar 6, 2019

@author: filipe
'''
from util import util
import os
import json
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from operator import itemgetter
from visualize import visualize
from summary import summary

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
        while(len(sentences) != 0):
            sentence = sentences.pop(0)
            for element in ngramtext:
                #for sentence in sentences:
                    if (element in sentence): 
                        ngramsentences.append(sentence)
                        break
        singlegramsentences = list(set(sentences) - set(ngramsentences))        
        return ngramsentences, singlegramsentences
    
    @staticmethod
    def get_top_node(jsonobj):
        '''
        it gets the top ranked element
        '''
        return jsonobj[0]
    
    
    
    @staticmethod
    def process_sentence(sentence, jsonobj):
        starttoken = '{'
        endtoken = '}'
        processedtext = sentence.lower()
        concepts = []
        #concatenate some custom stop words to Wordnet stopwords
        custom_stopwords = ['of course', 'in order']
        for stopword in custom_stopwords:
            processedtext = processedtext.replace(stopword, '')
        stop_words = custom_stopwords + list(stopwords.words('english'))
        #Remove stop words
        processedtext = word_tokenize(processedtext)
        processedtext = [w for w in processedtext if not w in stop_words]
        #Replace all concepts with their tag ids and pos
        previous_word = ''
        for word in processedtext:
            for concept in jsonobj:
                if (concept['text'] == word):
                    try:
                        if (concept['pos'] == concepts[-1]['pos']) and (previous_word != 'and'):
                            if (concept['pos'][0] == 'v'): #If it is a verb, add 'and'
                                connectingword = ' and '
                            else:
                                connectingword = ' '
                            concepts[-1]['text'] += connectingword + concept['text']
                        else:
                            concepts.append(concept)
                    except:
                        concepts.append(concept)
            previous_word = word
        #create node triplets [n (or v-n), v, n]                
        sentencetriplets = conceptmap.create_triplets(concepts)
        return sentencetriplets
    
    @staticmethod
    def create_triplets(concepts):
        '''
        create node triplets [n , v, n] or [v, n, n] where n, v, n are full concept structures
        '''
        noum = 'n'
        propernoum = 'nnp'
        verb = 'v'
        triplets = []
        triplet = []
        while(len(concepts)> 1):
            concept = concepts.pop(0)
            #if starts with verb, finds the noun associated with it and invert order to create triplet
            if (concept['pos'][0] == verb):
                #Gets the np pos associated with initial verb
                for nextconcept in concepts:
                    if(nextconcept['pos'] == propernoum): #if(nextconcept['pos'][0] == noum)
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
                    if (concept['pos'] == propernoum):
                        concept = concepts.pop(0)
                    else:
                        concept = concepts[0]
                    triplet.append(concept)
                    #If next concept is a verb, associate in between the two noums
                    if (concepts[0]['pos'][0] == verb):
                        concept = concepts.pop(0)
                        triplet[1] = concept
                    triplets.append(triplet)
                    triplet = []
                    continue
                #Gets the verb associated with initial noum
                for nextconcept in concepts:
                    if(nextconcept['pos'][0] == verb):
                        nextconcept = concepts.pop(0)
                        triplet.append(concept)
                        triplet.append(nextconcept)
                        break
                #Gets next noun to complete triplet
                for nextconcept in concepts:
                    if(nextconcept['pos'][0] == noum):
                        try:
                            if ((nextconcept['pos'] != propernoum) and (nextconcept['pos'] != 'nns') and (concepts[1]['pos'][0] != noum)): #Only removes from list if not proper noum and next concept is not another noum
                                nextconcept = concepts.pop(0)
                            triplet.append(nextconcept)
                            break
                        except: print
                triplets.append(triplet)
                #if next concept is another noum, it needs to be associated to the same previous verb    
                #===============================================================
                # for nextconcept in concepts:
                #     if(nextconcept['pos'][0] == noum):
                #         nexttriplet = triplet.copy()
                #         nexttriplet[2] = nextconcept
                #         triplets.append(nexttriplet)
                #         triplet = []
                #         nexttriplet = []
                #         break
                #===============================================================
                #===============================================================
                # try:
                #     if ((concepts[0]['pos'][0] == noum) and (concepts[0]['pos'] != propernoum)):
                #         nexttriplet = triplet.copy()
                #         nexttriplet[2] = nextconcept
                #         triplets.append(nexttriplet)
                #     triplet = []s
                #     nexttriplet = []
                # except: 
                #     triplet = []
                #     nexttriplet = []
                #===============================================================
            triplet = []
            nexttriplet = []
        return triplets
    
    @staticmethod
    def build_graph(triplets):
        pass
    
    @staticmethod
    def generate_conceptmap(summarytext, outputdir, plotConceptMap=True, savetriplets=False, separateClusters=False, mapfile = 'unix.gv'):
        '''
        This is the main method that will generate the concept map based on the supplied input text
        '''
        graphoutputfile = "rubric_o2.json"
        summary.generateGraph(summarytext, graphoutputfile, outputdir, plotGraph = False)
        jsonFile = os.path.join(outputdir, graphoutputfile)
        jsonobj = conceptmap.open_text_json(jsonFile)
        ngramids, ngramtext, ngrampos = conceptmap.retrieve_ngram_params(jsonobj)
        topconcept = conceptmap.get_top_node(jsonobj)
        ngramsentences, singlegramsentences = conceptmap.get_ngram_sentences(summarytext, ngramtext)
        allsentences = ngramsentences + singlegramsentences
        firstsentence = True
        clustersentences = []
        u = None
        for sentence in allsentences:
            test = (conceptmap.process_sentence(sentence, jsonobj))
            testcp = test.copy()
            clustersentences.append(testcp)
            if (firstsentence):
                sentencetriplets = test
                firstsentence = False
            else: sentencetriplets += test
        if savetriplets:
            tripletsFile = os.path.join(outputdir, "triplets.json")
            with open(tripletsFile, 'w') as f:
                f.write(str(sentencetriplets))
        if plotConceptMap:
            if(separateClusters):visualize.plot_graphclusters(clustersentences, mapfile)
            else: visualize.plotGraph(sentencetriplets, mapfile)

    
if __name__ == '__main__':
    jsonFile = os.path.join(util.get_path('jsonessays'), 'rubric_o2.json')
    outputdir = util.get_path('rubric')
    summaryFile = os.path.join(outputdir, 'rubric.txt')
    with open(summaryFile, 'r') as f:
        summarytext = f.read()
    conceptmap.generate_conceptmap(summarytext, outputdir, plotConceptMap=True, savetriplets=False, separateClusters=False)
    #===========================================================================
    # jsonobj = conceptmap.open_text_json(jsonFile)
    # ngramids, ngramtext, ngrampos = conceptmap.retrieve_ngram_params(jsonobj)
    # topconcept = conceptmap.get_top_node(jsonobj)
    # ngramsentences, singlegramsentences = conceptmap.get_ngram_sentences(summarytext, ngramtext)
    # allsentences = ngramsentences + singlegramsentences
    # sentencetriplets = []
    # for sentence in allsentences:
    #     sentencetriplets += (conceptmap.process_sentence(sentence, jsonobj))
    # visualize.plotGraph(sentencetriplets)
    #===========================================================================
    pass