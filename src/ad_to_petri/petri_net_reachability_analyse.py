'''
Created on 04.11.2015

@author: Kai
'''


import numpy as np
import log
from bean import petri_net_element

class PetriNetReachabilityAnalyser(object):
    '''Petri Net Reachability Analyzer
    '''
    def show_pt_net_details(self, petri_net, show=False):
        '''show the details of the petri net
        '''
        if show:
            places_dict = petri_net.places_dict
            transitions_dict = petri_net.transitions_dict
            arcs_dict = petri_net.arcs_dict
            print "the number of placesDict:" + str(len(places_dict))
            for p_id in places_dict:
                place = places_dict[p_id]
                print "pt_id:" + place.pt_id
                print "name:" + str(place.name)
                print "incomings:",
                for incoming in place.incomings:
                    print incoming,
                print
                print "outgoings:",
                for outgoing in place.outgoings:
                    print outgoing,
                print
                print "--------------------"
            print "********************************"
            print "the number of transitionsDict:" + str(len(transitions_dict))
            for t_id in transitions_dict:
                transition = transitions_dict[t_id]
                print "pt_id:" + transition.pt_id
                print "name:" + str(transition.name)
                print "incomings:",
                for incoming in transition.incomings:
                    print incoming,
                print
                print "outgoings:",
                for outgoing in transition.outgoings:
                    print outgoing,
                print
                print "--------------------"
            print "********************************"
            print "the number of arcsDict:" + str(len(arcs_dict))
            for pt_id in arcs_dict:
                arc = arcs_dict[pt_id]
                print "pt_id:" + arc.pt_id
                print "name:" + str(arc.name)
                print "source:" + arc.source
                print "target:" + arc.target
                print "--------------------"

    def get_petri_type(self, petri_net):
        '''get the type of Petri-Net
        @see: http://www.informatik.uni-hamburg.de/TGI/PetriNets/classification/
        -Place/Transition (P/T) Nets
            *(Ordinary) Petri Nets (PN)
                ~1-safe Net Systems
                ~Free Choice Nets: @1
                    S-Systems
                        State Machines (SM): @2
                    T-System
                        Marked Graphs (MG): @3
                    Structural Free Choice Extensions:
        ps:
        1: A Free Choice Net is an ordinary Petri Net such that every arc from a place is
        either a unique outgoing arc or a unique incoming arc to a transition
            1a.if two transitions share a common input place then they have no other input places
            1b.If two places share a common transition then they have no other transition
            --here algorithm
        2: A State Machine is a Petri Net where every transition has only
        one input place and one output place
        3: A Marked Graph is a pure (ordinary) Petri Net system where every place has only
        one input transition and one output transition
        '''
        petri_type = []

        places_dict = petri_net.places_dict
        transitions_dict = petri_net.transitions_dict
        arcs_dict = petri_net.arcs_dict

        free_choice = True
        state_machines = True
        marked_graphs = True

        for t_id in transitions_dict:
            transition = transitions_dict[t_id]
            incomings = transition.incomings
            outgoings = transition.outgoings
            in_num = len(incomings)
            out_num = len(outgoings)
            if in_num > 1:
                state_machines = False
                # if it is free_choice
                for incoming in incomings:
                    arc = arcs_dict[incoming]
                    p_id = arc.source
                    place = places_dict[p_id]
                    if len(place.outgoings) > 1:
                        # the place has another transition
                        free_choice = False
                        marked_graphs = False
                        break
                # if not free_choice,break. it is neither state_machines nor marked_graphs
                if not free_choice:
                    break
            elif out_num > 1:
                state_machines = False

        # it is free_choice, see if it is marked_graphs
        if free_choice:
            for p_id in places_dict:
                place = places_dict[p_id]
                incomings = place.incomings
                outgoings = place.outgoings
                in_num = len(incomings)
                out_num = len(outgoings)
                if in_num > 1 or out_num > 1:
                    marked_graphs = False
                    break

        if free_choice:
            if state_machines and marked_graphs:
                petri_type.append(petri_net_element.PetriNetTypes.STATE_MACHINES)
                petri_type.append(petri_net_element.PetriNetTypes.MARKED_GRAPHS)
                log.show_info("the type of the transformed Petri-Net is state_machines, "\
                "and also marked_graphs. name:%s" % petri_net.name)
            elif state_machines and not marked_graphs:
                petri_type.append(petri_net_element.PetriNetTypes.STATE_MACHINES)
                log.show_info("the type of the transformed Petri-Net is state_machines."\
                               + " name:%s" % petri_net.name)
            elif not state_machines and marked_graphs:
                petri_type.append(petri_net_element.PetriNetTypes.MARKED_GRAPHS)
                log.show_info("the type of the transformed Petri-Net is marked_graphs."\
                              + " name:%s" % petri_net.name)
            else:
                petri_type.append(petri_net_element.PetriNetTypes.FREE_CHOICE)
                log.show_info("the type of the transformed Petri-Net is free_choice, "\
                              "it is neither state_machines nor marked_graphs."\
                               + " name:%s" % petri_net.name)
        else:
            petri_type.append(petri_net_element.PetriNetTypes.NOT_FREE_CHOICE)
            log.show_info("the type of the transformed Petri-Net is not free_choice."\
                           + " name:%s" % petri_net.name)

        return petri_type

    def get_matrix(self, petri_net):
        '''get the net matrix of the Petri-Net.
        the way to change the number of a matrix in numpy
        matrix[0][0] = 1 or matrix[0,0] = 1
        '''

        places_dict = petri_net.places_dict
        transitions_dict = petri_net.transitions_dict
        arcs_dict = petri_net.arcs_dict

        p_num = len(places_dict)
        t_num = len(transitions_dict)
        # create the matrix
        matrix = np.zeros((p_num, t_num))
        for p_id in places_dict:
            # "s1"-->1, "s12"-->12
            row_str = p_id[1:]
            # if it is "p1", also id_changed is True, the place can be enabled
            if row_str.isdigit():
                row = int(row_str)
                place = places_dict[p_id]
                incomings = place.incomings
                for incoming in incomings:
                    arc_id = incoming
                    arc = arcs_dict[arc_id]
                    source = arc.source
                    t_id = source
                    col_str = t_id[1:]
                    # if it is "t1", also id_changed is True, the transition can fire
                    if col_str.isdigit():
                        col = int(col_str)
                        matrix[row - 1, col - 1] = 1
                outgoings = place.outgoings
                for outgoing in outgoings:
                    arc_id = outgoing
                    arc = arcs_dict[arc_id]
                    target = arc.target
                    t_id = target
                    # if it is "t1", also id_changed is True, the transition can fire
                    col_str = t_id[1:]
                    if col_str.isdigit():
                        col = int(col_str)
                        matrix[row - 1, col - 1] = -1
        log.show_info("the matrix of the Petri-Net, see below." + " name:" + petri_net.name)
        petri_net.matrix = matrix
        print matrix
        return matrix

    def find_deadlock(self, petri_net):
        '''find the deadlock.1)the place can never be marked.2)the transition can never fire
        also if the id_changed is False.
        '''
        # put the deadlock id to the list
        place_ids = []
        transition_ids = []

        places_dict = petri_net.places_dict
        transitions_dict = petri_net.transitions_dict
        for place in places_dict.values():
            if place.id_changed is False:
                place_ids.append(place.pt_id)
                log.show_warn("the place can never be marked "\
                              + "name:" + str(place.name) + " id:" + place.pt_id)
        for transition in transitions_dict.values():
            if transition.id_changed is False:
                transition_ids.append(transition.pt_id)
                log.show_warn("the transition can never fire "\
                              + "name:" + str(transition.name) + " id:" + transition.pt_id)

        return place_ids + transition_ids
