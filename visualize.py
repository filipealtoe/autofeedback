'''
Created on Mar 5, 2019

@author: filipe
'''
from graphviz import Digraph
from graphviz import Source

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
    
    @staticmethod
    def plot_graphclusters(concepttriplets):

        try:
            i = 1
            allfiles = []
            for cluster in concepttriplets:
                filename='unix' + str(i) + '.gv'
                allfiles.append(filename)
                u = Digraph('unix', filename)
                u.attr(size='6,6')
                u.node_attr.update(color='lightblue2', style='filled')
                for triplet in cluster:
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
                u.render(filename)
                u = None
        except:
            pass
        
        for file in allfiles:
            s = Source.from_file(file)
            s.view()
    
    
    @staticmethod
    def display_graph(u):
        u.view()
if __name__ == '__main__':
    visualize.plotGraph(None)