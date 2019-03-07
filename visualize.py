'''
Created on Mar 5, 2019

@author: filipe
'''
from graphviz import Digraph

class visualize(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    @staticmethod
    def plotGraph(triplets):    
        u = Digraph('unix', filename='unix.gv')
        u.attr(size='6,6')
        u.node_attr.update(color='lightblue2', style='filled')
        try:
            i = 0
            for triplet in triplets:
                firstedge = triplet[0]['text']
                try:
                    label = triplet[1]['text']
                except:
                    label = ''
                try:
                    secondedge = triplet[2]['text']
                except:
                    secondedge = ''
                u.edge(firstedge, secondedge, label=label)
                i += 1
        except:
            pass
        u.view()
        
if __name__ == '__main__':
    visualize.plotGraph(None)