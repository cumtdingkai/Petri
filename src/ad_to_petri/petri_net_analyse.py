'''
Created on 04.11.2015

@author: Kai
'''

from bean import petri_net_element
import log

class PetriNetAnalyser(object):
    '''petri net analyzer
    '''
    def set_next_place_tokens(self, place, tokens_num, petri_net):
        '''set the place.max_tokens after the place.
        tokens_num = place.max_tokens
        '''
        places_dict = petri_net.places_dict
        transitions_dict = petri_net.transitions_dict
        arcs_dict = petri_net.arcs_dict

        place_outgoings = place.outgoings
        for place_outgoing in place_outgoings:
            arc1 = arcs_dict[place_outgoing]
            next_transiton_id = arc1.target
            next_transition = transitions_dict[next_transiton_id]
            for transition_outgoing in next_transition.outgoings:
                arc2 = arcs_dict[transition_outgoing]
                next_place_id = arc2.target
                # get the next_place after the place
                next_place = places_dict[next_place_id]
                if next_place.max_tokens == 1:
                    next_place.max_tokens = tokens_num
                    self.set_next_place_tokens(next_place, tokens_num, petri_net)
                else:
                    log.show_error("the place.max_tokens is already not 1 ")

    def set_place_tokens(self, petri_net):
        '''set the place.max_tokens,when it >1, and also the places after the place.
        '''
        places_dict = petri_net.places_dict

        for place_id in places_dict:
            place = places_dict[place_id]
            # if the place.max_tokens >1, for example merge in PayOrder
            if place.max_tokens != 1:
                tokens_num = place.max_tokens
                self.set_next_place_tokens(place, tokens_num, petri_net)

    def find_self_loop(self, petri_net):
        '''A Petri Net without any self loop is called "Pure Petri Net".
        A self-loop occurs when a place p is at same time input and output to a transition t.
        A Petri Net is said to be ordinary if the weight of all its arcs is 1.
        auf deutsch: reines PN ohne Selbstschleifen,Schlingen--> eliminieren
        '''
        places_dict = petri_net.places_dict
        transitions_dict = petri_net.transitions_dict
        arcs_dict = petri_net.arcs_dict

        self_loop_places = []
        self_loop_arcs = []
        # the number of the self_loops
        num = 0

        # place->arc1->transition->arc2->place
        for place_id in places_dict:
            place = places_dict[place_id]
            for place_outgoing in place.outgoings:
                arc1 = arcs_dict[place_outgoing]
                transiton_id = arc1.target
                transition = transitions_dict[transiton_id]
                for transition_outgoing in transition.outgoings:
                    arc2 = arcs_dict[transition_outgoing]
                    next_place_id = arc2.target
                    # place p is at same time input and output to a transition t.
                    if next_place_id == place_id:
                        num += 1
                        self_loop_places.append(place)
                        self_loop_arcs.append(arc2)
        if num > 0:
            log.show_warn("the petri net has " + str(num) + " self-loop.")
            for index in range(num):
                place = self_loop_places[index]
                arc = self_loop_arcs[index]
                self.eliminate_self_loop(place, arc, petri_net)
        return num

    def eliminate_self_loop(self, place, arc, petri_net):
        '''eliminate the self_loop(place-->transition-->arc-->place)
        place-->transition-->arc-->new_place-->new_arc1-->new_transition-->new_arc2-->place
        step1.separate the place and arc
        step2.create the new object,put it in the dict
        step3.connect the object to the front and back object
        '''

        places_dict = petri_net.places_dict
        transitions_dict = petri_net.transitions_dict
        arcs_dict = petri_net.arcs_dict
        # separate the place and arc
        place.incomings.remove(arc.pt_id)
        arc.target = None

        # create a new place
        new_place_pt_id = self._get_new_id("place", places_dict)
        new_place = petri_net_element.Place(new_place_pt_id, new_place_pt_id, [arc.pt_id], [])
        places_dict[new_place_pt_id] = new_place
        arc.target = new_place_pt_id
        # create a new arc1
        new_arc1_pt_id = self._get_new_id("arc", arcs_dict)
        new_arc1 = petri_net_element.Arc(new_arc1_pt_id, new_arc1_pt_id, new_place_pt_id, None)
        arcs_dict[new_arc1_pt_id] = new_arc1
        new_place.outgoings.append(new_arc1_pt_id)
        # create a new ImmediateTransition
        new_transition_pt_id = self._get_new_id("transition", transitions_dict)
        new_transition = petri_net_element.ImmediateTransition(new_transition_pt_id,\
                                                        new_transition_pt_id, [new_arc1_pt_id], [])
        transitions_dict[new_transition_pt_id] = new_transition
        new_arc1.target = new_transition_pt_id
        # create a new arc2
        new_arc2_pt_id = self._get_new_id("arc", arcs_dict)
        new_arc2 = petri_net_element.Arc(new_arc2_pt_id, new_arc2_pt_id, new_transition_pt_id, None)
        arcs_dict[new_arc2_pt_id] = new_arc2
        new_transition.outgoings.append(new_arc2_pt_id)

        new_arc2.target = place.pt_id
        place.incomings.append(new_arc2_pt_id)

    def _get_new_id(self, element_type, element_dict):
        '''get one not exist id of element in element_dict,
        such as "place_id1","transition_id2","arc_id3"...
        @param element_type: the type of the element, such as "place", "transition","arc"
        @type element_type: string
        '''
        element_id = element_type + "_id"
        tem = True
        num = 1
        while tem:
            new_id = element_id + str(num)
            if new_id not in element_dict:
                tem = False
            else:
                num += 1
        return new_id
