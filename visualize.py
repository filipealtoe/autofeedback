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
    def plotGraph(graph):    
        u = Digraph('unix', filename='unix.gv')
        u.attr(size='6,6')
        u.node_attr.update(color='lightblue2', style='filled')
        
        u.edge('5th Edition', '6th Edition')
        
        u.view()