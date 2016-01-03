'''
Created on 26.10.2015

@author: Kai
'''
from bean import petri_net_element as pt_element
from bean import uml_activity_diagram_element as uml_element
import log

class TransformerToPt(object):
    '''activity diagram to petri net
    '''
    def create_arc(self, arcs_dict, pt1, pt2, prob=1):
        '''
        create one arc object between the pt1 and pt2, pt1--(arc)-->pt2
        arc_id: "arc0","arc1","arc2"....
        name : None
        source: pt1.pt_id
        target: pt2.pt_id
        and put it in the arcs_dict
        at the same time, set pt1.outgoings, and pt2.incomings
        @param arcs_dict: the arcs_dict
        @type arcs_dict: dict
        @param pt1: the first place or transition (pt1.pt_id--source)
        @type pt1: a object of PtNetElemnt.Place or PtNetElemnt.Transition
        @param pt2: the second place or transition (pt2.pt_id--target)
        @type pt2: a object of PtNetElemnt.Place or PtNetElemnt.Transition
        '''
        arc_id = "arc" + str(len(arcs_dict))
        arc = pt_element.Arc(arc_id, None, pt1.pt_id, pt2.pt_id)
        arc.prob = prob
        arcs_dict[arc_id] = arc
        # pt1.outgoings, and pt2.incomings
        pt1.outgoings.append(arc_id)
        pt2.incomings.append(arc_id)

    def create_pt_object(self, node1, node2, prob, petri_net):
        '''create p or t object
        '''
        places_dict = petri_net.places_dict
        transitions_dict = petri_net.transitions_dict
        arcs_dict = petri_net.arcs_dict
        # the id is nodeId of the umlActivityElement , also the pt_id of the petri_net_element
        id1 = node1.xmi_id
        id2 = node2.xmi_id
        # the 2 nodes are place
        if node1.place and node2.place:
            # create a transition and put it in the transitionsDict
            # place1 -(arc1)-> transition -(arc2)-> place2
            pt_id = id1 + id2
            if pt_id not in transitions_dict:
                # create one immediate transition
                transition = pt_element.ImmediateTransition(pt_id,
                                                            name=None,
                                                            incomings=[],
                                                            outgoings=[])
                transitions_dict[pt_id] = transition
                # place1
                place1 = places_dict[id1]
                # place2
                place2 = places_dict[id2]
                # create one arc, place1 -(arc1)-> transition,
                # and put it in the arcs_dict
                self.create_arc(arcs_dict, place1, transition, prob)
                # create the other arc, transition -(arc2)-> place2,
                # and put it in the arcs_dict
                self.create_arc(arcs_dict, transition, place2)
            else:
                log.show_warn("id1-->id2 has more than one connection")
        # the 2 nodes are transition
        elif node1.transition and node2.transition:
            # create a place and put it in the placesDict
            # transition1 -(arc1)-> place -(arc2)-> transition2
            pt_id = id1 + id2
            if pt_id not in places_dict:
                # create one place
                place = pt_element.Place(pt_id, name=None,
                                         incomings=[], outgoings=[])
                places_dict[pt_id] = place
                # transition1
                transition1 = transitions_dict[id1]
                # transition2
                transition2 = transitions_dict[id2]
                # create one arc, transition1 -(arc1)-> place,
                # and put it in the arcs_dict
                self.create_arc(arcs_dict, transition1, place)
                # create the other arc, place -(arc2)-> transition2,
                # and put it in the arcs_dict
                self.create_arc(arcs_dict, place, transition2)
            else:
                log.show_warn("id1-->id2 has more than one connection")
        # p --> t    #TODO more than one connection
        elif node1.place and node2.transition:
            # just create one arc, p -(arc)-> t
            place = places_dict[id1]
            transition = transitions_dict[id2]
            self.create_arc(arcs_dict, place, transition, prob)
        # t --> p
        elif node1.transition and node2.place:
            # just create one arc, t -(arc)-> p
            transition = transitions_dict[id1]
            place = places_dict[id2]
            self.create_arc(arcs_dict, transition, place)
        else:
            # Error
            print "type error +create_pt_object():", node1.xmi_type, node2.xmi_type

    def transform_to_petri_net(self, activity):
        '''
        transform the UmlActivityDiagramElemnt objects to the petri_net_element objects
        '''
        # the activity elements
        activity_name = activity.name
        nodes_dict = activity.nodes_dict
        edges_dict = activity.edges_dict

        # the Petri net elements
        # name:Place (class petri_net_element.Place)
        places_dict = {}
        # name:Transition (class petri_net_element.Transition)
        transitions_dict = {}
        # name:Arc (class petri_net_element.Arc)
        arcs_dict = {}
        # create a petri net object
        petri_net = pt_element.PetriNet(places_dict, transitions_dict, arcs_dict, activity_name)

        # create Place,Transition objects from the nodes, if node.petri=True
        for node_id in nodes_dict:
            node = nodes_dict[node_id]
            # nodes_dict[node_id].petri = True
            if node.petri:
                # get the id, name, incomings, outgoings
                pt_id = node.xmi_id
                name = node.name
                incomings = []  # list
                outgoings = []
                # new Place object, and put it in the places_dict
                if node.place:
                    # initial Node is "s1" and start:True
                    if node.xmi_type == uml_element.Types.INITIAL_NODE:
                        place = pt_element.Place(pt_id, name, incomings, outgoings)
                        place.start = True
                        place.tokens = 1
                        places_dict[pt_id] = place
                    elif node.xmi_type == uml_element.Types.ACTIVITY_FINAL_NODE:
                        place = pt_element.Place(pt_id, name, incomings, outgoings)
                        place.final = True
                        places_dict[pt_id] = place
                    elif node.xmi_type == uml_element.Types.MERGE_NODE:
                        place = pt_element.Place(pt_id, name, incomings, outgoings)
                        places_dict[pt_id] = place
                        # if the max_tokens of the merge is not 1
                        # see example:payOrder
                        if node.max_tokens != 1:
                            place.max_tokens = node.max_tokens
                    else:
                        place = pt_element.Place(pt_id, name, incomings, outgoings)
                        places_dict[pt_id] = place
                # new Transition object, and put it in the transitions_dict
                elif node.transition:
                    # fork,join,action without <<Time>> stereotyping
                    if node.immediate:
                        transition = pt_element.ImmediateTransition(pt_id,
                                                                    name,
                                                                    incomings,
                                                                    outgoings)
                        # transition.delay =0
                    # action with <<Time>> stereotyping and property time and "const"
                    elif node.deterministic:
                        transition = pt_element.DeterministicTransition(pt_id,
                                                                        name,
                                                                        incomings,
                                                                        outgoings)
                        transition.delay = node.time
                    # action with <<Time>> stereotyping and property time and "exp"
                    elif node.exponential:
                        transition = pt_element.ExponentialTransition(pt_id,
                                                                        name,
                                                                        incomings,
                                                                        outgoings)
                        transition.delay = node.time
                    transitions_dict[pt_id] = transition
        # edge--> arc
        for edge_id in edges_dict:
            # get the source, target of the edge
            edge = edges_dict[edge_id]
            # if it is control flows
            if edge.xmi_type == uml_element.Types.CONTROL_FLOW:
                source = edge.source
                target = edge.target
                # get the body of the guard.
                # arc_label = ""
                guard = edge.guard
                if guard is not None:
                    pass
                    # arc_label = guard.body
                # get the node in nodes_dict from the ID
                if source in nodes_dict:
                    node1_id = source
                    node1 = nodes_dict[node1_id]
                # pin,pout
                else:
                    log.show_warn("the source is not a node")
                # get the node in nodes_dict from the ID
                if target in nodes_dict:
                    node2_id = target
                    node2 = nodes_dict[node2_id]
                else:
                    log.show_warn("the target is not a node")
                if node1.petri and node2.petri:  # node1 , node2 -- P(merge...) or T(action...)
                    self.create_pt_object(node1, node2, edge.prob, petri_net)
                else:
                    log.show_warn("node1 and node2 are not both petri")
            # object flow, pass
            else:
                pass
        return petri_net
