'''
Created on Mar 5, 2019

@author: filipe
'''
import networkx as nx

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
         
        nx.draw_spring(graph)