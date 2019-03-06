'''
Created on Mar 5, 2019

@author: filipe
'''

#from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet as wn
from nltk import word_tokenize, pos_tag
from nltk.tokenize import sent_tokenize
import numpy as np
from util import util

class similarity(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''

        
    @staticmethod
    def penn_to_wn(tag):
    #Convert between a Penn Treebank tag to a simplified Wordnet tag
        if tag.startswith('N'):
            return 'n'
     
        if tag.startswith('V'):
            return 'v'
     
        if tag.startswith('J'):
            return 'a'
     
        if tag.startswith('R'):
            return 'r'
 
        return None
 
    @staticmethod
    def tagged_to_synset(word, tag):
        wn_tag = similarity.penn_to_wn(tag)
        if wn_tag is None:
            return None
     
        try:
            test = wn.synsets(word, wn_tag)[0]          
            return test

        except:
            return None
     
    @staticmethod
    def sentence_similarity(sentence1, sentence2):
        """ compute the sentence similarity using Wordnet """
        # Tokenize and tag
        sentence1 = pos_tag(word_tokenize(sentence1))
        sentence2 = pos_tag(word_tokenize(sentence2))
     
        # Get the synsets for the tagged words
        synsets1 = [similarity.tagged_to_synset(*tagged_word) for tagged_word in sentence1]
        synsets2 = [similarity.tagged_to_synset(*tagged_word) for tagged_word in sentence2]
     
        # Filter out the Nones
        synsets1 = [ss for ss in synsets1 if ss]
        synsets2 = [ss for ss in synsets2 if ss]
     
        score, count = 0.0, 0
     
        # For each word in the first sentence
        for synset in synsets1:
            # Get the similarity value of the most similar word in the other sentence
            best_score = [synset.path_similarity(ss) for ss in synsets2]
            best_score = [0 if v is None else v for v in best_score]
            best_score = max(best_score)
     
            # Check that the similarity could have been computed
            if best_score is not None:
                score += best_score
                count += 1
     
        # Average the values
        try:
            score /= count
        except:
            score = 0
        return score
    
    @staticmethod
    def symmetric_sentence_similarity(sentence1, sentence2):
    #compute the symmetric sentence similarity using Wordnet
        return (similarity.sentence_similarity(sentence1, sentence2) + similarity.sentence_similarity(sentence2, sentence1)) / 2 
    

    @staticmethod
    def summaries_similarity(file1, file2, sentencelevel=True):
        '''
        If sentence level is set, method will output similarity between each sentence of the two files.
        Else, it will do similarity for the entire summary
        '''
        print ('Performing summary similarity analysis...')
        summary1 = open(file1, 'r').read()        
        summary2 = open(file2, 'r').read()
        
        if sentencelevel:
            summary1 = sent_tokenize(summary1) #split into sentences
            summary2 = sent_tokenize(summary2) #split into sentences
            
            resultText = ''
            for focus_sentence in summary1:
                for sentence in summary2:
                    resultText += focus_sentence + ','+sentence + ',' + str(similarity.symmetric_sentence_similarity(focus_sentence, sentence)) + '\n'
        
        else:
            resultText = file1 + ','+ file2 + ',' + str(similarity.symmetric_sentence_similarity(summary1, summary2)) + '\n'
        
        return resultText
    
    @staticmethod
    def summaries_multiplefiles_similarity(files):
        '''
        It will perform similarity comparison between every combination of two files from the provided list of summary
        file paths input
        '''
        print ('Performing all files summary similarity analysis...')
        allfiles = files
        if (len(files) < 2):
            resultText = 'Number of supplied files less than 2. No similatiry analysis performed.'
            print (resultText)
            similarityresults = None
        else:
            resultText = 'basesummaryfile,summaryfile,similarityvalue,basefileindex,testfileindex' + '\n'
            fileindex = 0
            similarityresults = []
            while (len(allfiles) > 0):
                fileindex += 1
                basefile = allfiles.pop(0)
                summary1 = open(basefile, 'r').read()
                i = 1
                for file in allfiles:                        
                    summary2 = open(file, 'r').read()
                    similarityvalue = similarity.symmetric_sentence_similarity(summary1, summary2)
                    similarityresults.append({'basefilepath':basefile, 'testfilepath':file, 'basefile':fileindex, 'testfile':fileindex + i, 'similarity':similarityvalue})
                    resultText += basefile + ','+ file + ',' + str(similarityvalue) + ',' + str(fileindex) + ',' + str(fileindex + i) + '\n'
                    i += 1
        
        return resultText,similarityresults
    
    @staticmethod
    def get_highest_similar_summary(similarityvalue):
        if (similarityvalue == None):
            return None
        else:
            print ('Calculating highest averaged similarity summary...')
            highestindex = max([d['testfile'] for d in similarityvalue])
            similarities = []
            basefiles = [d['basefile'] for d in similarityvalue]
            testfiles = [d['testfile'] for d in similarityvalue]
            basefilespath = [d['basefilepath'] for d in similarityvalue]
            testfilespath = [d['testfilepath'] for d in similarityvalue]
            allsimilarities = np.array([d['similarity'] for d in similarityvalue])
            for index in range(1,highestindex+1):
                indices = [i for i, x in enumerate(basefiles) if x == index]
                if len(indices) < highestindex - 1: #all the other indexes except 1
                    indicestest = [i for i, x in enumerate(testfiles) if x == index]
                    indices = indices + indicestest
                averagesimilarity = sum(list(allsimilarities[indices])) / (highestindex - 1)
                similarities.append(averagesimilarity)
            maxsimilarityvalue = np.max(np.array(similarities))
            maxsimilarityindex = similarities.index(maxsimilarityvalue) + 1
            indices = [i for i, x in enumerate(basefiles) if x == maxsimilarityindex]
            if (len(indices) == 0): #this cathes the last file that doesn't show up on the basefiles indices
                indices = [i for i, x in enumerate(testfiles) if x == maxsimilarityindex]
                summaryfilepath = testfilespath[indices[0]]
            else:
                summaryfilepath = basefilespath[indices[0]]
            
            summarytext = open(summaryfilepath, 'r').read()
        return ({'rubrictext':summarytext, 'similarities':similarities, 'maxsimilarity':maxsimilarityvalue})
    
    @staticmethod
    def debug_highest_sim_summary():
        similarities = util.extract_foundsimilarities()
        similaritiesdata = []
        for line in similarities:
            similaritiesdata.append({'basefilepath':str(line[0]), 'testfilepath':str(line[1]),'basefile':int(line[3]), 'testfile':int(line[4]), 'similarity':float(line[2])})
        return (similarity.get_highest_similar_summary(similaritiesdata))   
        
if __name__ == '__main__':   

    #debug highest similar summary algorithm. Requires an existing autogeneratedrubric.csv file
    
    #===========================================================================
    # rubrictext, returnedsimilaties, maxsimilarity = similarity.debug_highest_sim_summary()
    # print (rubrictext)
    # print (returnedsimilaties)
    # print (maxsimilarity)
    #===========================================================================
     
    sentences = [
        "Dogs are awesome.",
        "Some gorgeous creatures are felines.",
        "Dolphins are swimming mammals.",
        "Cats are beautiful animals.",
    ]
     
    focus_sentence = "Cats are beautiful animals."
   
    
    for sentence in sentences:
        print ("SymmetricSimilarity(\"%s\", \"%s\") = %s" % (
            focus_sentence, sentence, 
            similarity.symmetric_sentence_similarity(focus_sentence, sentence)))
        print ("SymmetricSimilarity(\"%s\", \"%s\") = %s" % (
            sentence, focus_sentence, similarity.symmetric_sentence_similarity(sentence, focus_sentence)))
        print 
  
#SymmetricSimilarity("Cats are beautiful animals.", "Dogs are awesome.") = 0.588888888889
#SymmetricSimilarity("Dogs are awesome.", "Cats are beautiful animals.") = 0.588888888889
 
# SymmetricSimilarity("Cats are beautiful animals.", "Some gorgeous creatures are felines.") = 0.833333333333
# SymmetricSimilarity("Some gorgeous creatures are felines.", "Cats are beautiful animals.") = 0.833333333333
 
# SymmetricSimilarity("Cats are beautiful animals.", "Dolphins are swimming mammals.") = 0.441666666667
# SymmetricSimilarity("Dolphins are swimming mammals.", "Cats are beautiful animals.") = 0.441666666667
 
# SymmetricSimilarity("Cats are beautiful animals.", "Cats are beautiful animals.") = 1.0
# SymmetricSimilarity("Cats are beautiful animals.", "Cats are beautiful animals.") = 1.0