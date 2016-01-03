'''
Created on 03.10.2015

@author: Kai
'''

from bean import reachability_graph_element as Rg
import log
from bean import petri_net_element

class PetriToReachabilityGraph(object):
    '''get the ReachabilityGraph from a petri net
    '''

    def _get_new_id(self, pt_element, pt_elements_dict):
        '''get the new ID of P or T, for example, "p3","t4"..
        for example EAID_BB946565_CBA6_4ee7_820E_8D19061435F6 (the id in xml)--> p1
        @param pt_element: place or transition
        @type pt_element: object of petri_net_element.Place or petri_net_element.Transition
        @param pt_elements_dict: places_dict or transitions_dict
        @type pt_elements_dict: dict
        @return: new_id --"p3","t4"..
        @rtype: new_id--str
        '''
        new_id = None
        num = 1
        for pt_id in pt_elements_dict:
            element = pt_elements_dict[pt_id]
            if element.id_changed is True:
                num += 1
        if isinstance(pt_element, petri_net_element.Place):
            new_id = "p" + str(num)
        elif isinstance(pt_element, petri_net_element.Transition):
            new_id = "t" + str(num)
        else:
            log.show_error("the pt_element type is wrong")

        if new_id in pt_elements_dict:
            log.show_error("the new id " + new_id + " exist already..._get_new_id()")
        return new_id



    def change_pt_id(self, pt_element, pt_elements_dict, arcs_dict, petri_net):
        ''' change the id of place or transition element,
        for example EAID_BB946565_CBA6_4ee7_820E_8D19061435F6 (the id in xml)--> p1
        @param pt_element: place or transition
        @type pt_element: object of petri_net_element.Place or petri_net_element.Transition
        @param pt_elements_dict: places_dict or transitions_dict
        @type pt_elements_dict: dict
        @param arcs_dict: the dict of arcs
        @type arcs_dict: dict
        '''
        new_id = self._get_new_id(pt_element, pt_elements_dict)
        # get the old id
        old_id = pt_element.pt_id
        # set the new id
        pt_element.pt_id = new_id
        # log.logWarn(old_id+"--->"+new_id)   # it is for debug
        label = "%s:\t%s \l" % (new_id, pt_element.name)
        petri_net.label += label
        # xlabel:External label for a node or edge.
        # For nodes, the label will be placed outside of the node but near it.
        # For edges, the label will be placed near the center of the edge.(s1,s2...t1,t2...)
        pt_element.xlabel = new_id
        pt_element.id_changed = True
        # the target of the incomings arc --> new_id
        incomings = pt_element.incomings
        for incoming in incomings:
            arc = arcs_dict[incoming]
            arc.target = new_id
        # the source of the outgoings arc --> new_id
        outgoings = pt_element.outgoings
        for outgoing in outgoings:
            arc = arcs_dict[outgoing]
            arc.source = new_id
        # pop the pt_element from the dict
        pt_elements_dict.pop(old_id)
        # put it in the dict
        pt_elements_dict[new_id] = pt_element

    def is_transition_enabled(self, transition, places, places_dict, arcs_dict):
        ''' if the transition is enabled, when all the source-places are marked,
        and the target-place are not marked (German: nicht belegt).

        A finite capacity Petri Net is that in which there is a maximum of tokens defined
        for each place.
        For such Petri Nets there is an additional firing rule that says that
        after firing a transition,
        the number of tokens in its output places must not exceed their maximum.

        auf deutsch:
        @see: Lunze jan Ereignisdiskrete systeme   6.1.3 Verhalten
        eine Transition t ist aktiviert,wenn
        1. alle Praestellen p markiert und
        2. alle Poststellen p nicht markiet sind.
        Beim Schalten aktivierter Transitionen wird allen Praestellen die Marke entzogen
        und alle Poststellen werden markiert
        @param transition: the transition
        @type transition: petri_net_element.Transition
        @param places: the marked places of this state
        @type places: list
        @return: enabled, if the t is enabled
        @rtype: bool  True,False
        '''
        enabled = True

        incomings = transition.incomings
        outgoings = transition.outgoings
        for incoming in incomings:
            arc = arcs_dict[incoming]
            place_id = arc.source
            place = places_dict[place_id]
            # the needed place is not in the places, the transition will not be enabled
            if place not in places:
                enabled = False
                break
        for outgoing in outgoings:
            arc = arcs_dict[outgoing]
            place_id = arc.target
            place = places_dict[place_id]
            # one of the target-places is marked, the transition will not be enabled
            if place in places:
                if place.tokens + 1 > place.max_tokens:
                    enabled = False
                    break

        return enabled

    def determine_marking(self, places, transition, places_dict, arcs_dict):
        '''fire t and determine the marking m' after firing.
        get the next state, in the state which places are marked
        @param places: the current marked places, pre-places. attention: do not change places!!!
        @type places: list
        @param transition: the next enabled transition,here just one transition from our definition
        @type transition: petri_net_element.Transition
        '''
        pre_places = places[:]
        incomings = transition.incomings
        for incoming in incomings:
            arc = arcs_dict[incoming]
            source = arc.source
            place = places_dict[source]
            if place in pre_places:
                place.tokens -= 1
                # not any more tokens,remove it
                if place.tokens == 0:
                    pre_places.remove(place)
            else:
                log.show_error(place.pt_id + " is not marked")
        outgoings = transition.outgoings
        for outgoing in outgoings:
            arc = arcs_dict[outgoing]
            target = arc.target
            place = places_dict[target]
            place.tokens += 1
            if place not in pre_places:
                pre_places.append(place)

        return pre_places

    def my_cmp(self, id1, id2):
        ''' sort by the number of the id, not default
        if sort default "p11" < "p6"
        ensure "p6" < "p11", change the placeId to number, for example "p11" to 11, "p6" to 6
        @param id1: the pt_id of the place
        @type id1: str
        '''
        num1 = int(id1[1:])
        num2 = int(id2[1:])
        return cmp(num1, num2)

    def get_state_id(self, places, petri_net):
        '''get the state_id from his marked places ids
        for example "<s1>" or "<s1,s2>" or "<s1,s2,s3>" sorted
        "<s2,s1>"--it is wrong!  it must be "<s1,s2>"
        @return: state_id
        @rtype: str
        '''

        places_dict = petri_net.places_dict

        state_id = ""
        places_ids = [place.pt_id for place in places]
        # "p6" < "p11"
        places_ids.sort(self.my_cmp)
        for pt_id in places_ids:
            place = places_dict[pt_id]
            if place.tokens > 1:
                temp = "," + pt_id + "(" + str(place.tokens) + ")"
            elif place.tokens == 1:
                temp = "," + pt_id
            else:
                log.show_error("no tokens in the place")
            state_id += temp
        # delete the first ","-----",s1,s2"-->"s1,s2"
        state_id = state_id[1:]
        state_id = "<" + state_id + ">"
        return state_id


    def final_in_places(self, places):
        ''' if the places have the final place, also place.final is True
        yes: return True
        no:  return False
        '''
        ret = False
        for place in places:
            if place.final is True:
                ret = True
                break
        return ret

    def get_next_state(self, places, transitions, petri_net, rg_graph, unreach_list, reach, probs):
        '''fire t and determine the marking m' after firing.
        1b).if 2 transitions t1,t2 can be enabled, so from the node < m > will create 2 arrows.
        fire t1,go to step2(until stop),then fire t2, go to step2.
        step2. fire t and determine the marking m' after firing. if m' is already a node in G,
        then add the new arrow(m,t,m') to G, stop.
        step3. if m' is not a node in G, add m' as a new node and (m,t,m')
        as a new arrow to G and go to step 1.
        get the next states, it can be more states.
        @param places: the current marked places,pre-places
        @type places: list
        '''

        places_dict = petri_net.places_dict
        arcs_dict = petri_net.arcs_dict
        states_dict = rg_graph.states_dict
        edges_dict = rg_graph.edges_dict

        # pre_state_id: '<s1,s2>'
        pre_state_id = self.get_state_id(places, petri_net)

        reset_tokens = False

        # parallel, or decision
        if len(transitions) > 1:

            reset_tokens = True
            tokens_list = [place.tokens for place in places]

        if pre_state_id not in states_dict:
            pre_state = Rg.State(pre_state_id, pre_state_id, [], [])
            states_dict[pre_state_id] = pre_state
            # it is for unreach diagram, show in color blue
            if not reach:
                pre_state.reachability = False
        else:
            pre_state = states_dict[pre_state_id]
        # every time just one transition can be enabled.
        index = -1
        for transition in transitions:
            index += 1
            # reset the places 's tokens
            if reset_tokens:
                self.reset_tokens(places, tokens_list, places_dict)

            # get the next state-places, change id, and get the state id
            next_places = self.determine_marking(places, transition, places_dict, arcs_dict)
            for place in next_places:
                if not place.id_changed:
                    self.change_pt_id(place, places_dict, arcs_dict, petri_net)
            next_state_id = self.get_state_id(next_places, petri_net)
            # "<p1,p2><p3>"
            # edge_id = "pre_state_id + next_state_id"
            # "edge0","edge1","edge2","edge3"...
            edge_id = "edge" + str(len(edges_dict))
            if edge_id not in edges_dict:
                # pre_state.outgoings is list, append the edge_id
                pre_state.outgoings.append(edge_id)
                edge = Rg.Edge(edge_id, edge_id, pre_state_id, next_state_id)
                # TODO
                edge.prob = probs[index]
                edge.label = transition.pt_id + "(" + str(edge.prob) + ")"
                edges_dict[edge_id] = edge
                #
                if not reach:
                    edge.reachability = False
            # multiedge, for example, p4-t5-p5,p4-t6-p5,p4-t7-p5
            else:
                log.show_error("edge id error in RG")
                # edge = edges_dict[edge_id]
                # edge.label = edge.label + " or " + transition.pt_id

            # step 3. if m' is not a node in G
            if next_state_id not in states_dict:
                next_state = Rg.State(next_state_id, next_state_id, [], [])
                # pre_state.incomings is list, append the edge_id
                next_state.incomings.append(edge_id)
                states_dict[next_state_id] = next_state
                #
                if not reach:
                    next_state.reachability = False
            # if m' is already a node in G,then add the new arrow(m,t,m') to G, stop.
            else:
                # next state exist, just incomings append the edge_id
                next_state = states_dict[next_state_id]
                if edge_id not in next_state.incomings:
                    next_state.incomings.append(edge_id)
                continue
            # step 3a) if m' has final node, stop
            if self.final_in_places(next_places):
                continue
            if len(next_places) > 0:
                # go to step 1
                self.find_enabled_transitions(next_places, petri_net, rg_graph, unreach_list, reach)

    def find_enabled_transitions(self, places, petri_net, rg_graph, unreach_list, reach):
        ''' first,get the next following transition from the current marked places,
        second, see if it can be enabled(see function-is_transition_enabled),
        and save the transitions in one list, for example [s1,s2]
        @param places: the current marked places,pre-places
        @type places: list
        @param reach: True, for the reachability_graph diagram.
        False, unreach_list=[],for the unreachability_graph.
        @type reach: Boolean
        @see: algorithm- step1
        '''
        # [t1,t2,t3...]
        transitions = []
        # [[t1],[t2,t3]...]
        # t1 fire from place1, t2,t3 fire from place2(decision)
        transitions_slices = []
        # the probs to fire the transition
        # [prob1,prob2,prob3...], the sum must be 1
        probs = []
        # [[prob1],[prob2,prob3]...]
        # prob1 is 1, sum of prob2 and prob3 is 1
        probs_slices = []
        # petri_net
        places_dict = petri_net.places_dict
        transitions_dict = petri_net.transitions_dict
        arcs_dict = petri_net.arcs_dict

        # get the next transition from the place, and see if it can be enabled
        for place in places:
            # [t1] or [t2,t3]
            transitions_slice = []
            # [1] or [0.3,0.7]
            probs_slice = []
            outgoings = place.outgoings
            for outgoing in outgoings:
                arc = arcs_dict[outgoing]
                target = arc.target
                transition = transitions_dict[target]
                # if the transition can be enabled
                if self.is_transition_enabled(transition, places, places_dict, arcs_dict):
                    # get the prob from the arc
                    prob = arc.prob
                    # put the transition in the transitions_slice
                    if transition not in transitions_slice:
                        transitions_slice.append(transition)
                        # put the prob in the probs_slice
                        probs_slice.append(prob)
                    else:
                        # show error
                        log.show_error("more than 1 arcs between the place and the transition:find_enabled_transitions()")
                    # put it in the transitions
                    if transition not in transitions:
                        transitions.append(transition)
                        probs.append(prob)
                    # change the id of transition,which can be enabled
                    if not transition.id_changed:
                        self.change_pt_id(transition, transitions_dict, arcs_dict, petri_net)
            # if it is not []
            if transitions_slice:
                transitions_slices.append(transitions_slice)
                probs_slices.append(probs_slice)
        if reach:
            # parallel find the min(delay), 
            # if just decision len(transitions) > 1 and len(transitions_slices)=1
            # if len(transitions_slices) > 1, but len(transitions) = 1-->join:
            # len(transitions_slices) >1 ,-->parallel
            if len(transitions) > 1 and len(transitions_slices) > 1:
                # delete the same type
                types_set = set([transition.transition_type for transition in transitions])
                types_list = list(types_set)
                # TODO
                if len(types_list) == 1:
                    # get the type of the transitions
                    transition_type = types_list[0]

                    # all are immediate transition
                    if transition_type == petri_net_element.TransitionTypes.IMMEDIATE_TRANSITION:
                        pass
                    # all are DeterministicTransition
                    elif transition_type == petri_net_element.TransitionTypes.DETERMINISTIC_TRANSITION:
                        execute_transition = self.get_execute_transition(transitions)

                        transitions.remove(execute_transition)
                        #
                        tokens_list = [place.tokens for place in places]
                        unreach_list.append(places)
                        unreach_list.append(tokens_list)
                        unreach_list.append(transitions)
                        #
                        transitions = [execute_transition]
                    # all are EXPONENTIAL_TRANSITION
                    elif transition_type == petri_net_element.TransitionTypes.EXPONENTIAL_TRANSITION:
                        if len(transitions_slices) == 2:
                            self._calculate_probability(transitions_slices, probs_slices, transitions, probs)
                        else:
                            log.show_error("the code can not analyse 3 parallel exp distribution process")
                    else:
                        log.show_error("the type of the transition is not defined")

                # all are ExponentialTransition
                else:
                    log.show_warn("the types of the enabled transitions are not the same")

        # see algorithm- step1a)
        if len(transitions) > 0:
            # fire t and determine the marking m' after firing.
            self.get_next_state(places, transitions, petri_net, rg_graph, unreach_list, reach, probs)

    def get_execute_transition(self, transitions):
        '''all are Deterministic Transitions,return the min(delay) transition
        '''
        execute_transition = None
        delays = [transition.delay for transition in transitions]
        # find the min_delay (time) in the delays_list
        min_delay = min(delays)
        # find the transition, which has the min_delay time
        for transition in transitions:
            if transition.delay == min_delay:
                execute_transition = transition
                break
        # the other transition.delay minus the min_delay time
        for transition in transitions:
            transition.delay -= min_delay
        # reset the execute_transitio
        execute_transition.delay = min_delay
        return execute_transition

    def _calculate_probability(self, transitions_slices, probs_slices, transitions, probs):
        '''transitions_slices: [[B,C],[G,H]],
        probs_slices: [[0.3,0.7],[0.4,0.6]]
        transitions: [B,C,G,H]
        probs: [0.3,0.7,0.4,0.6]-->[a,b,c,d].. sum(a+b+c+d)=1
        '''
        transitions_slice1 = transitions_slices[0]
        transitions_slice2 = transitions_slices[1]
        probs_slice1 = probs_slices[0]
        probs_slice2 = probs_slices[1]
        for index1 in range(len(transitions_slice1)):
            prob = 0
            transition1 = transitions_slice1[index1]
            prob1 = probs_slice1[index1]
            for index2 in range(len(transitions_slice2)):
                transition2 = transitions_slice2[index2]
                prob2 = probs_slice2[index2]
                prob += prob1 * prob2 * self._calculate_exp_probability(transition1, transition2)
            t_index = transitions.index(transition1)
            probs[t_index] = prob
        for index2 in range(len(transitions_slice2)):
            prob = 0
            transition2 = transitions_slice2[index2]
            prob2 = probs_slice2[index2]
            for index1 in range(len(transitions_slice1)):
                transition1 = transitions_slice1[index1]
                prob1 = probs_slice1[index1]
                prob += prob1 * prob2 * self._calculate_exp_probability(transition2, transition1)
            t_index = transitions.index(transition2)
            probs[t_index] = prob

    def _calculate_exp_probability(self, transition1, transition2):
        '''calculate the probability with 2 exponential distributions.
        '''
        # calculate with 2 exponential distributions
        delay1 = transition1.delay
        delay2 = transition2.delay
        prob = float(delay1) / (delay1 + delay2)  
        prob = round(prob, 3)
        return prob

    def get_reachability_graph(self, petri_net):
        ''' get the reachability_graph_element of the PT Net.
        initNodes is "uml:InitialNode", and just one InitialNode

        @see: Lunze jan Ereignisdiskrete systeme
        1.Bei einer Markierung s1 sind beiden Transitionen aktiviert,
        so dass im Erreichbarkeitdiagram vom Knoten {<s1>} zwei Kanten ausgehen.
        2.Bei der Bewegung des Petrinetzes darf nur jeweils eineder angegebenen Transition schalten.
        Das gleichzeitige Schalten mehrerer Transition wird
        durch einen Pfad im Erreichbarkeitsgrafen dargestellt.

        algorithm:
        step1. find the transition(s), which is(are) enabled in m .
            1a).if no transition can be enabled, stop.
            1b).if 2 transitions t1,t2 can be enabled, so from the node < m > will create 2 arrows.
            fire t1,go to step2(until stop),then fire t2, go to step2.
        step2. fire t and determine the marking m' after firing. if m' is already a node in G,
            then add the new arrow(m,t,m') to G, stop.
        step3. if m' is not a node in G, add m' as a new node and (m,t,m') as a new arrow to G
            and go to step 1.
        attention: for get_reachability_graph from activity transformed petri net.
            3a) if m' has final node, stop
            else go to step1
        @param places_dict: the place dict of the PT Net {place.id : place...},
        see petri_net_element.Place
        @type places_dict: dict
        @param transitions_dict: the transition dict of the PT Net {transition.id : transition...},
        see petri_net_element.Transition
        @type transitions_dict: dict
        @param arcs_dict: the arcs of the PT Net {arcs.id : arcs...}, see petri_net_element.Arc
        @type arcs_dict: dict
        '''

        places_dict = petri_net.places_dict
        arcs_dict = petri_net.arcs_dict

        # statesDict of the reachability_graph_element
        states_dict = {}
        # edgesDict of the reachability_graph_element
        edges_dict = {}
        # create the rg graph
        rg_graph = Rg.ReachabilityGraph(states_dict, edges_dict, petri_net.name)

        # [places,tokens_list,transitions,places,tokens_list,transitions...]
        unreach_list = []

        # here, in ActivityDiagram just one initPlace
        init_places = [place for place in places_dict.itervalues() if place.start]
        # p1,t1.....
        # initPlac - "p1"
        for place in init_places:
            self.change_pt_id(place, places_dict, arcs_dict, petri_net)
            # the initial place has one token.
            place.tokens = 1
        # get the next enabled transitions
        # see step1
        self.find_enabled_transitions(init_places, petri_net, rg_graph, unreach_list, True)

        num = len(unreach_list)
        for index in range(num / 3):
            places = unreach_list[index * 3]
            tokens_list = unreach_list[index * 3 + 1]
            self.reset_tokens(places, tokens_list, places_dict)

            transitions = unreach_list[index * 3 + 2]
            # TODO
            probs = []
            for x in transitions:
                probs.append(1)
            self.get_next_state(places, transitions, petri_net, rg_graph, [], False, probs)

        self._set_probs_label(petri_net)
        return rg_graph
    
    def _set_probs_label(self, petri_net):
        '''set the probability label in petri net
        '''
        arcs_dict = petri_net.arcs_dict
        for arc_id in arcs_dict:
            arc = arcs_dict[arc_id]
            source = arc.source
            target = arc.target
            if arc.prob != 1:
                prob_label = "%s->%s:\t%0.3f \l" % (source, target, arc.prob)
                petri_net.probs += prob_label

    def reset_tokens(self, places, tokens_list, places_dict):
        '''reset the tokens
        '''
        # all the tokens to 0
        for place in  places_dict.values():
            place.tokens = 0
        # reset
        place_num = len(places)
        for index in range(place_num):
            places[index].tokens = tokens_list[index]
