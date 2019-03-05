'''
Created on Mar 5, 2019

@author: filipe
'''
import os
import pytextrank
import networkx as nx
import pylab as plt
from TxtToJson import txtToJson
from visualize import visualize
import matplotlib
import networkx

class summary(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
   
    @staticmethod
    def generateGraph(text,outputfile, outputdir, plotGraph = False):
        print ('Generating Graph...')
        #Start by doing statistical parsing/tagging for 
        temp_file = os.path.join(outputdir, 'temp.json')
        path_stage1 = os.path.join(outputdir, outputfile.split("_")[0] + '_o1.json')
        txtToJson.textTojson(text, temp_file)
        with open(path_stage1, 'w') as f:
            for graf in pytextrank.parse_doc(pytextrank.json_iter(temp_file)):
                f.write("%s\n" % pytextrank.pretty_print(graf._asdict()))

        #Collect and Normalize the key sentences from the parsed doc
        graph, ranks = pytextrank.text_rank(path_stage1)
        pytextrank.render_ranks(graph, ranks)
        #path_stage2 = path_stage1.replace('o1', 'o2')
        path_stage2 = os.path.join(outputdir, outputfile)
        try:
            os.remove(outputfile)
        except OSError:
            pass
        with open(path_stage2, 'w') as f:
            for rl in pytextrank.normalize_key_phrases(path_stage1, ranks):
                f.write("%s\n" % pytextrank.pretty_print(rl._asdict()))
                #print(pytextrank.pretty_print(rl))
        try:
            os.remove(temp_file)
        except OSError:
            pass
        
        if plotGraph:
#            visualize.plotGraph(graph)
            matplotlib.rcParams['figure.figsize'] = (15.0, 15.0)
            networkx.draw_networkx(graph)
            plt.show()
            #===================================================================
            # nx.draw(graph, with_labels = True)  
            # plt.show()   
            # 
            #===================================================================
    @staticmethod
    def summarize(path_stage1, path_stage2, path_stage3, wordlimit, phraselimit):
        print ('Generating summary...')
        #Calculate a significance weight for each sentence, using MinHash to approximate a Jaccard distance from key phrases determined by TextRank    
        kernel = pytextrank.rank_kernel(path_stage2)

        try:
            os.remove(path_stage3)
        except OSError:
            pass
        with open(path_stage3, 'w') as f:
            for s in pytextrank.top_sentences(kernel, path_stage1):
                f.write(pytextrank.pretty_print(s._asdict()))
                f.write("\n")
                #print(pytextrank.pretty_print(s._asdict()))
        
        #Summarize essay based on most significant sentences and key phrases
        phrases = ", ".join(set([p for p in pytextrank.limit_keyphrases(path_stage2, phrase_limit=phraselimit)]))
        sent_iter = sorted(pytextrank.limit_sentences(path_stage3, word_limit=wordlimit), key=lambda x: x[1])
        s = []
        
        for sent_text, idx in sent_iter:
            s.append(pytextrank.make_sentence(sent_text))
        
        graf_text = " ".join(s)
        #print("**excerpts:** %s\n\n**keywords:** %s" % (graf_text, phrases,))
        return graf_text, phrases