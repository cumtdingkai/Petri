'''
Created on 04.11.2015

@author: Kai
'''
class RgAnalyser(object):
    '''reachability graph analyze
    '''
    def show_rg_details(self, rg_graph, show):
        '''show the details of the reachability graph
        '''
        states_dict = rg_graph.states_dict
        edges_dict = rg_graph.edges_dict
        if show:
            keys = states_dict.keys()
            print keys
            print "the number of statesDict:" + str(len(states_dict))
            for state_id in states_dict:
                state = states_dict[state_id]
                print "state_id:" + state.state_id
                print "name:" + str(state.name)
                print "incomings:",
                for incoming in state.incomings:
                    print incoming,
                print
                print "outgoings:",
                for outgoing in state.outgoings:
                    print outgoing,
                print
                print "--------------------"
            print "********************************"
            print "the number of RgEdgesDict:" + str(len(edges_dict))
            for edge_id in edges_dict:
                edge = edges_dict[edge_id]
                print "edge_id:" + edge.edge_id
                print "name:" + str(edge.name)
                print "source:" + edge.source
                print "target:" + edge.target
                print "--------------------"
                