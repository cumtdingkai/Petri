'''
Created on 23.09.2015

@author: Kai
'''
class ReachabilityGraph(object):
    '''the class of Reachability Graph
    '''
    def __init__(self, states_dict, edges_dict, name):
        '''
        '''
        self.states_dict = states_dict
        self.edges_dict = edges_dict
        self.name = name

class State(object):
    '''the element state in a Reachability Graph
    '''
    def __init__(self, state_id, name, incomings, outgoings):
        '''
        @param state_id: the marked places
        @type state_id: str, for example '<s1,s2>'
        @param outgoings: the id of the can be enabled transition possible,
        for example "s1#s2", see Edge.edgeId
        @type outgoings: list, for example edgeId1,edgeId2....[edgeId1,edgeId1],edgeId1 is string
        '''
        self.state_id = state_id
        self.name = name
        self.incomings = incomings
        self.outgoings = outgoings
        # default true, if in timed petri-net
        self.reachability = True

class Edge(object):
    '''the element edge in a Reachability Graph
    '''
    def __init__(self, edge_id, name, source, target):
        '''
        label: the id of the transition,"t1"or"t2"
        @param edge_id: the id of the edge, s1--edge-->s2,e
        the id is "s1#s2"
        @type edge_id: str
        @param source: the id of the states "s1,s2"
        @type source: str
        @param target: the id of the states "s1,s2"
        @type target: str
        '''
        self.edge_id = edge_id
        self.name = name
        self.source = source
        self.target = target
        self.label = ""
        # default true, if in timed petri-net
        self.reachability = True
        # prob
        self.prob = 1
