'''
Created on Mar 5, 2019

@author: filipe
'''

#from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet as wn
from nltk import word_tokenize, pos_tag
from nltk.tokenize import sent_tokenize

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
    def summaries_similarity(file1, file2):
        print ('Performing summary similarity analysis...')
        summary1 = open(file1, 'r').read()
        summary1 = sent_tokenize(summary1) #split into sentences

        
        summary2 = open(file2, 'r').read()
        summary2 = sent_tokenize(summary2) #split into sentences

        
        resultText = ''
        for focus_sentence in summary1:
            for sentence in summary2:
                resultText += focus_sentence + ','+sentence + ',' + str(similarity.symmetric_sentence_similarity(focus_sentence, sentence)) + '\n'
                #===============================================================
                # print ("SymmetricSimilarity(\"%s\", \"%s\") = %s" % (
                # focus_sentence, sentence, 
                # similarity.symmetric_sentence_similarity(focus_sentence, sentence)))
                #===============================================================
        
        return resultText
        
if __name__ == '__main__':   

     
    sentences = [
        "Dogs are awesome.",
        "Some gorgeous creatures are felines.",
        "Dolphins are swimming mammals.",
        "Cats are beautiful animals.",
    ]
     
    focus_sentence = "Cats are beautiful animals."
    
    #===========================================================================
    # print ("SymmetricSimilarity(\"%s\", \"%s\") = %s" % (focus_sentence, focus_sentence, 
    #          similarity.symmetric_sentence_similarity(focus_sentence, focus_sentence)))
    #   
    # for sentence in sentences:
    #     print ("Similarity(\"%s\", \"%s\") = %s" % (focus_sentence, sentence, 
    #                                                similarity.sentence_similarity(focus_sentence, sentence)))
    #     print ("Similarity(\"%s\", \"%s\") = %s" % (sentence, focus_sentence, 
    #                                                similarity.sentence_similarity(sentence, focus_sentence)))
    #     print 
    #===========================================================================
     
    # Similarity("Cats are beautiful animals.", "Dogs are awesome.") = 0.511111111111
    # Similarity("Dogs are awesome.", "Cats are beautiful animals.") = 0.666666666667
     
    # Similarity("Cats are beautiful animals.", "Some gorgeous creatures are felines.") = 0.833333333333
    # Similarity("Some gorgeous creatures are felines.", "Cats are beautiful animals.") = 0.833333333333
     
    # Similarity("Cats are beautiful animals.", "Dolphins are swimming mammals.") = 0.483333333333
    # Similarity("Dolphins are swimming mammals.", "Cats are beautiful animals.") = 0.4
     
    # Similarity("Cats are beautiful animals.", "Cats are beautiful animals.") = 1.0
    # Similarity("Cats are beautiful animals.", "Cats are beautiful animals.") = 1.0   
    
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