'''
Created on Mar 4, 2019

@author: filipe
'''

from TxtToJson import txtToJson
import os, sys
from glob import glob
import pytextrank
import networkx as nx
import pylab as plt

if __name__ == '__main__':
    plotGraph = False  #For debugging purposes
    essayDir = "essays"
    jsonDir = "jsonessays"
    path = os.path.dirname(sys.argv[0])
    essay_path = os.path.join(path, essayDir)
    json_path = os.path.join(path, jsonDir)
    
    #Delete left over processed files
    name = glob(json_path + "/*.json")
    for fname in enumerate(name):
        try:
            os.remove(fname[1])
        except OSError:
            pass
    
    #Convert txts to Jsons
    txtToJson.ttJson(essay_path,json_path, directory=True)

    
    #Repeat the process for each Json file in the essays dir
    name = glob(json_path + "/*.json")
    for fname in enumerate(name):
        #Start by doing statistical parsing/tagging for 
        path_stage1 = fname[1].split('.json')[0] + '_o1.json'
        try:
            os.remove(path_stage1)
        except OSError:
            pass
        with open(path_stage1, 'w') as f:
            for graf in pytextrank.parse_doc(pytextrank.json_iter(fname[1])):
                f.write("%s\n" % pytextrank.pretty_print(graf._asdict()))
                #print(pytextrank.pretty_print(graf))

        #Collect and Normalize the key sentences from the parsed doc
        graph, ranks = pytextrank.text_rank(path_stage1)
        pytextrank.render_ranks(graph, ranks)
        path_stage2 = path_stage1.replace('o1', 'o2')
        try:
            os.remove(path_stage2)
        except OSError:
            pass
        with open(path_stage2, 'w') as f:
            for rl in pytextrank.normalize_key_phrases(path_stage1, ranks):
                f.write("%s\n" % pytextrank.pretty_print(rl._asdict()))
                #print(pytextrank.pretty_print(rl))
        if plotGraph:
            nx.draw(graph, with_labels = True)  
            plt.show()      
            
        #Calculate a significance weight for each sentence, using MinHash to approximate a Jaccard distance from key phrases determined by TextRank    
        kernel = pytextrank.rank_kernel(path_stage2)
        path_stage3 = path_stage1.replace('o1', 'o3')
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
        phrases = ", ".join(set([p for p in pytextrank.limit_keyphrases(path_stage2, phrase_limit=12)]))
        sent_iter = sorted(pytextrank.limit_sentences(path_stage3, word_limit=150), key=lambda x: x[1])
        s = []
        
        for sent_text, idx in sent_iter:
            s.append(pytextrank.make_sentence(sent_text))
        
        graf_text = " ".join(s)
        print("**excerpts:** %s\n\n**keywords:** %s" % (graf_text, phrases,))