'''
Created on 04.11.2015

@author: Kai
'''

from bean import uml_activity_diagram_element as uml_element
import log

class ActivityDiagramAnalyser(object):
    ''' the analyzer for a activity diagram
    '''
    def show_activity_details(self, activity, show):
        '''show the details of the activity diagram
        '''
        if show:
            nodes_dict = activity.nodes_dict
            edges_dict = activity.edges_dict
            print "the number of nodesDict:" + str(len(nodes_dict))
            for node_id in nodes_dict:
                node = nodes_dict[node_id]
                print "Id:" + node.xmi_id
                print "xmi_type:" + node.xmi_type
                print "name:" + str(node.name)
                print "incomings:",
                for incoming in node.incomings:
                    print incoming.xmi_idref,
                print
                print "outgoings:",
                for outgoing in node.outgoings:
                    print outgoing.xmi_idref,
                print
                if isinstance(node, uml_element.Action):
                    print "results:",
                    for result in node.results:
                        print "Id:" + result.xmi_id,
                        print "name:" + result.name,
                    print
                    print "arguments:",
                    for argument in node.arguments:
                        print "Id:" + argument.xmi_id,
                        print "name:" + argument.name,
                    print
                print "--------------------"
            print "********************************"
            print "the number of edgesDict:" + str(len(edges_dict))
            for edge_id in edges_dict:
                edge = edges_dict[edge_id]
                print "Id:" + str(edge.xmi_id)
                print "name:" + str(edge.name)
                print "type:" + str(edge.xmi_type)
                print "source:" + str(edge.source)
                print "target:" + str(edge.target)
                if edge.parallel is True:
                    print "parallel:" + str(edge.parallel)
                    print "fork_num:" + str(edge.fork_num)
                    print "parallel_num:" + str(edge.parallel_num)
                print "--------------------"

    def _has_outgoing_control_flow(self, node, activity):
        '''if the node has control flow,
        yes return True , no return False
        @param node: action, and so on
        @type node: uml_activity_diagram_element.Node... here Action
        '''
        edges_dict = activity.edges_dict
        # has no control flow
        has_control_flow = False
        for outgoing in node.outgoings:
            idref = outgoing.xmi_idref
            edge = edges_dict[idref]
            # if action1 has a ControlFlow,
            # we can't accept it as the ControlFlow from action1 to action2
            if edge.xmi_type == uml_element.Types.CONTROL_FLOW:
                # one flow is control flow, also the node has control flow
                has_control_flow = True
                break
        if has_control_flow is False:
            # show a warn message
            log.show_warn("the node has no outgoing ControlFlow,name:%s,id:%s"
                          % (node.name, node.xmi_id))
        return has_control_flow

    '''
    def get_result_action_node(self, source, nodes_dict):
        #get the action node from his result, because the source is the result id
        #result.xmi_id == source
        #@return: action
        #@rtype: uml_activity_diagram_element.Action
        
        action = None
        for node_id in nodes_dict:
            node = nodes_dict[node_id]
            # just uml_activity_diagram_element.Action has attribute results and arguments
            # SendSignalAction can have pin. it is Subclass of uml_activity_diagram_element.Action
            # AcceptEventAction can have pout. it is Subclass of uml_activity_diagram_element.Action
            if isinstance(node, uml_element.Action):
                for result in node.results:
                    if result.xmi_id == source:
                        action = node
                        break
        return action
    '''
    '''
    def get_argument_action_node(self, target, nodes_dict):
        #get the action node from his argument, because the target is the argument id
        #argument.xmi_id == target
        #@return: action
        #@rtype: uml_activity_diagram_element.Action

        action = None
        for node_id in nodes_dict:
            node = nodes_dict[node_id]
            # just uml_activity_diagram_element.Action has attribute results and arguments
            # SendSignalAction can have pin. it is Subclass of uml_activity_diagram_element.Action
            # AcceptEventAction can have pout. it is Subclass of uml_activity_diagram_element.Action
            if isinstance(node, uml_element.Action):
                for argument in node.arguments:
                    if argument.xmi_id == target:
                        action = node
                        break
        return action
    '''
    def _get_object_next_node(self, object_node, activity):
        '''get the action or control node after the object node.
        '''
        nodes_dict = activity.nodes_dict
        edges_dict = activity.edges_dict
        node = None
        outgoings = object_node.outgoings
        num = len(outgoings)
        if num == 0:
            log.show_warn("the object node has no ougoings")
        elif num == 1:
            outgoing = outgoings[0]
            edge_id = outgoing.xmi_idref
            edge = edges_dict[edge_id]
            node_id = edge.target
            node = nodes_dict[node_id]
        elif num > 1:
            log.show_error("the object node has more ougoings")
        # if the node after the object node is also object node.show error
        if isinstance(node, uml_element.ObjectNode):
            log.show_error("the node after the object node:%s is object node"
                           % str(object_node.name))
        return node

    def _add_control_flow(self, node1, node2, activity):
        '''add one control flow from node1 to node2.
        '''
        edges_dict = activity.edges_dict
        # get the edge_id, and create a edge
        edge_id = self._get_new_id("edge", edges_dict)
        edge = uml_element.ControlFlow(edge_id, uml_element.Types.CONTROL_FLOW,
                                       edge_id, node2.xmi_id, node1.xmi_id, None)
        # node1.outgoings and node2.incomings
        outgoing = uml_element.Outgoing(edge_id)
        node1.outgoings.append(outgoing)
        incoming = uml_element.Incoming(edge_id)
        node2.incomings.append(incoming)
        # put the edge to the edge_dict
        edges_dict[edge_id] = edge
        # shwo info
        log.show_info("one control flow is created from %s to %s."
                      % (str(node1.name), str(node2.name)))

    def _get_nodes_from_edge(self, edge, activity):
        '''get the node1, node2 from the edge.
        also, node1-->edge-->node2
        @param edge: a edge instance in activity
        @type edge: a instance of edge, not the id of the edge
        '''
        nodes_dict = activity.nodes_dict
        pins_dict = activity.pins_dict
        # node1 and node2
        node1 = None
        node2 = None
        # the id of source and target
        source = edge.source
        target = edge.target
        # if source is node_id
        if source in nodes_dict:
            node1 = nodes_dict[source]
        else:
            # source is pout id
            pin = pins_dict[source]
            node1_id = pin.host
            node1 = nodes_dict[node1_id]
        # if target is node_id
        if target in nodes_dict:
            node2 = nodes_dict[target]
        else:
            # target is pin id
            pin = pins_dict[target]
            node2_id = pin.host
            node2 = nodes_dict[node2_id]
        # if node1 or node2 is None,it is error
        if node1 is None or node2 is None:
            log.show_error("the node1 or node2 is None")
        return node1, node2

    def _analyse_nodes(self, node1, node2, activity):
        '''for example:
        situation:
        1. action1(with(out) pout)-->action2 (with(out) pin)
        2. action1-->object-->action2(or control)
        3. action1 with pin-->control node #pass
        4. control node(fork,decision,merge)-->action2 with pin #pass
        5. control node(fork,decision,merge)-->object-->action2(or control)
        6. control node-->control node #pass
        7. object node-->... #pass
        if action1 has no control flow, add one control flow between action1 and action2.
        '''
        # if node1 and node2 are actions
        # 1.situation
        if (isinstance(node1, uml_element.ExecutableNode) and \
            isinstance(node2, uml_element.ExecutableNode)):
            log.show_info("1.situation: action to action")
            # if node1 has no control flow
            if not self._has_outgoing_control_flow(node1, activity):
                # add one control flow from action1 to action2
                self._add_control_flow(node1, node2, activity)
        # if node1 is a action, and node2 is a object_node
        # 2.situation
        elif (isinstance(node1, uml_element.ExecutableNode) and
              isinstance(node2, uml_element.ObjectNode)):
            log.show_info("2.situation: action to object node")
            # if node1 has no control flow
            if not self._has_outgoing_control_flow(node1, activity):
                node3 = self._get_object_next_node(node2, activity)
                # if node3 not None
                if node3:
                    self._add_control_flow(node1, node3, activity)
        # if node1 is a action with pout, and node2 is a control
        # 3.situation
        elif (isinstance(node1, uml_element.ExecutableNode) and
              isinstance(node2, uml_element.ControlNode)):
            log.show_info("3.situation: action to control node")
            # pass
        # if node1 is control_node, node2 is a action with pin
        # 4.situation
        elif (isinstance(node1, uml_element.ControlNode) and
              isinstance(node2, uml_element.ExecutableNode)):
            log.show_info("4.situation: control node to action")
            # pass
        # if node1 is control_node, node2 is object_node
        # 5.situation
        elif (isinstance(node1, uml_element.ControlNode) and
              isinstance(node2, uml_element.ObjectNode)):
            log.show_info("5.situation: control node to object node")
            node3 = self._get_object_next_node(node2, activity)
            if node3:
                # add one control flow from node1 to node3
                self._add_control_flow(node1, node3, activity)
        # if node1 is control_node, node2 is control_node
        # 6.situation
        elif (isinstance(node1, uml_element.ControlNode) and
              isinstance(node2, uml_element.ControlNode)):
            log.show_info("6.situation: control node to control node")
            # TODO
            # pass
        # if node1 is object node
        # 7.situation
        elif isinstance(node1, uml_element.ObjectNode):
            pass
        else:
            log.show_warn("a object flow from node1 to node2,"
                          "but the 2 nodes's situation are not defined")

    def analyze_object_flow(self, activity):
        '''analyze the object flow between node1 and node2.
        '''
        log.show_info("object flow analyze starts...")

        edges_dict = activity.edges_dict
        # object flow number
        num = 0
        # dictionary changed size during iteration
        for edge in edges_dict.values():
            # if it is object flow
            if edge.xmi_type == uml_element.Types.OBJECT_FLOW:
                num += 1
                # get the node1, node2 from the edge
                node1, node2 = self._get_nodes_from_edge(edge, activity)
                # anylyse the node1 and node2
                self._analyse_nodes(node1, node2, activity)
        # show the number of object edge
        log.show_info("the activity diagram has %d object flow" % num)
        log.show_info("object flow analyze completed.")

    def get_init_final_num(self, activity):
        ''' verify, if the uml activity diagram has just(genau)
        one Initial Node, and one or more ActivityFinal. if a node has no incoming or no outgoing,
        it is a error, except init node and final node and flow final.
        '''
        nodes_dict = activity.nodes_dict
        initial_num = 0
        final_num = 0
        for node_id in nodes_dict:
            node = nodes_dict[node_id]
            incomings = node.incomings
            outgoings = node.outgoings
            in_num = len(incomings)
            out_num = len(outgoings)
            # initial node, just one and it must have outgoing
            if node.xmi_type == uml_element.Types.INITIAL_NODE:
                initial_num += 1
                if out_num == 0:
                    log.show_error("the Initial Node has no outgoing." + \
                                   "name:" + str(node.name) + " id:" + node.xmi_id)
            # final node, one or more, and it must have incoming
            elif node.xmi_type == uml_element.Types.ACTIVITY_FINAL_NODE:
                final_num += 1
                if in_num == 0:
                    log.show_error("the final Node has no incoming." + \
                                   "name:" + str(node.name) + " id:" + node.xmi_id)
            # flow final, it must have incoming
            elif node.xmi_type == uml_element.Types.FLOW_FINAL_NODE:
                if len(incomings) == 0:
                    log.show_error("the final Node has no incoming." + \
                                   "name:" + str(node.name) + " id:" + node.xmi_id)
            elif isinstance(node, uml_element.ObjectNode):
                if not isinstance(node, uml_element.InstanceSpecification_node):
                    if len(incomings) == 0:
                        # @see example Order
                        # show warn info, not error info
                        log.show_warn("the object Node has no incoming.name:%s,id:%s"
                                      % (str(node.name), node.xmi_id))
                    if len(outgoings) == 0:
                        # @see example Order
                        # show warn info, not error info
                        log.show_warn("the object Node has no outgoins.name:%s,id:%s"
                                      % (str(node.name), node.xmi_id))
            # if the node has no incoming or no outgoing
            # it is a error(except initial,final,object node)
            else:
                # incoming and outgoing of a node
                if in_num == 0:
                    # action has no incoming, but it has argument, and the argument has incoming
                    if isinstance(node, uml_element.ExecutableNode):
                        arguments = node.arguments
                        for argument in arguments:
                            # if the argument has no incoming
                            if len(argument.incomings) == 0:
                                log.show_error("the action node's argument in " + \
                                                "uml activity diagram has no incoming." + \
                                                "name:" + str(node.name) + \
                                                " id:" + node.xmi_id)
                    # it is not a action
                    else:
                        log.show_error("the node in uml activity diagram has no incoming."\
                                       + "name:" + str(node.name) + " id:" + node.xmi_id)
                if out_num == 0:
                    # action has no outgoing, but it has result, and the result has outgoing
                    if isinstance(node, uml_element.ExecutableNode):
                        results = node.results
                        for result in results:
                            # if the result has no outgoing
                            if len(result.outgoings) == 0:
                                log.show_error("the action node's result in " + \
                                                "uml activity diagram has no incoming." + \
                                                + "name:" + str(node.name) + " id:" + node.xmi_id)
                    # it is not a action
                    else:
                        log.show_error("the node in uml activity diagram has no outgoing."\
                                       + "name:" + str(node.name) \
                                        + " id:" + node.xmi_id)
        # initial node just one
        if initial_num == 0:
            log.show_error("the uml activity diagram has no Initial Node")
        elif initial_num > 1:
            log.show_error("the uml activity diagram has " + str(initial_num) + " Initial Nodes")
        # final node one or more than one
        if final_num == 0:
            log.show_warn("the uml activity diagram has no final Node")

        return initial_num, final_num

    def __get_corrected_name(self, name):
        '''get the corrected name.
        delete " ", change "-","+" to "_"
        @param name: the name of the node
        @type name: string
        @return: the corrected name
        @rtype: string
        '''
        corrected_name = name.replace(" ", "_")
        corrected_name = corrected_name.replace("-", "_")
        corrected_name = corrected_name.replace("+", "_")
        return corrected_name

    def check_names(self, activity):
        '''check the name of action and object.
        1.if it is None or "",it will cause a error when it transforms to epf.
        set the name "node1","node2"
        2.if two nodes(action or object) have the same name, it will also cause a error
        when it transforms to epf. for example "get info" and "get_info"
        3.change the name to the corrected name
        # TODO check the name of pin
        @return: check_ok, if checks ok
        @rtype: boolean
        '''
        check_ok = True
        names = []
        nodes_dict = activity.nodes_dict
        pins_dict = activity.pins_dict

        # action, object, initial, final
        node_types = (uml_element.ExecutableNode, uml_element.ObjectNode,
                      uml_element.InitialNode, uml_element.FinalNode, uml_element.Fork, uml_element.Join)
        # for node
        num1 = 0
        # for pin,pout
        num2 = 0
        # it checks the name of pout, do not need to check the name of pin
        for pin_id in pins_dict:
            pin = pins_dict[pin_id]
            # if it is a pout(Result)
            if isinstance(pin, uml_element.Result):
                name = pin.name
                # if it has no name, see condition1
                if name is None or name.strip() == "":
                    # if the pin has no name, set the name "pin1","pin2"...
                    num2 += 1
                    pin.name = "pin" + str(num2)
                    log.show_warn("the pin has no name.id:%s" % pin.xmi_id)
                else:
                    corrected_name = self.__get_corrected_name(name)
                    # change the name of node to corrected name
                    pin.name = corrected_name
                    # see condition2
                    if corrected_name in names:
                        check_ok = False
                        log.show_error("the pin has the same name.name:%s" % name)
                    else:
                        names.append(corrected_name)

        for node_id in nodes_dict:
            node = nodes_dict[node_id]
            # if it is a action or object,initial,final
            # The form using a tuple, isinstance(x, (A, B, ...)), is a shortcut for
            # isinstance(x, A) or isinstance(x, B) or ... (etc.).
            if isinstance(node, node_types):
                name = node.name
                # if it has no name, see condition1
                if name is None or name.strip() == "":
                    # if the node has no name, set the name "node1","node2"...
                    num1 += 1
                    node.name = "node" + str(num1)
                    log.show_warn("the node has no name.id:%s" % node.xmi_id)
                else:
                    corrected_name = self.__get_corrected_name(name)
                    # change the name of node to corrected name
                    node.name = corrected_name
                    # see condition2
                    if corrected_name in names:
                        check_ok = False
                        log.show_error("the nodes has the same name.name:%s" % name)
                    else:
                        names.append(corrected_name)
        return check_ok

    def _get_new_id(self, element_type, element_dict):
        '''get one not exist id of element in element_dict,
        such as "edge_id1","edge_id2","edge_id3"...
        @param element_type: the type of the element, such as "merge", "edge","decision"
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

    def _create_merge(self, node_id, activity, flow_type):
        ''' create a merge before the action(fork), if the action(fork) has
        more than 2 incomings control flow
        1. change the 2 or more edges(control flow) target to the mergeId
        2. create a edge between merge and action(fork), at the same time,
        create a outgoing,incoming, their xmi_idref is the id of edge,
        and change the incomings of the action(fork), outgoings of the merge
        3. create a merge
        4. put the merge, edge to the dicts
        @attention: do not change the object flow edge
        @param node_id: the id of the node
        @type node_id: str
        @param flow_type: the type of the flow(edge).
        @type flow_type: 1.uml_element.Types.CONTROL_FLOW 2.uml_element.Types.OBJECT_FLOW
        '''

        nodes_dict = activity.nodes_dict
        edges_dict = activity.edges_dict
        # get the node
        node = nodes_dict[node_id]
        # get the merge id
        # merge_id1,merge_id2
        merge_xmi_id = self._get_new_id("merge", nodes_dict)
        # "uml:MergeNode"
        xmi_type = uml_element.Types.MERGE_NODE
        name = merge_xmi_id
        merge_incomings = []
        node_incomings = []
        # 1. change the 2 edges attribute target to the merge
        incomings = node.incomings
        for incoming in incomings:
            incoming_id = incoming.xmi_idref
            edge = edges_dict[incoming_id]
            if edge.xmi_type == uml_element.Types.CONTROL_FLOW:
                edge.target = merge_xmi_id
                merge_incomings.append(incoming)
            # object flow
            else:
                node_incomings.append(incoming)
        # 2. create a Outgoing instance for merge, a ActivityEdge instance,
        # and a Incoming instance for node
        # 2a. create a Outgoing instance. edge_id is the xmi_id in edge,
        # also the xmi_idref of the instance Outgoing

        # get the id of the edge
        edge_id = self._get_new_id("edge", edges_dict)
        edge_name = edge_id
        # create outgoing
        outgoing = uml_element.Outgoing(edge_id)
        outgoings = [outgoing]
        # 2b. create a ActivityEdge instance. target: node_id, source: merge_xmi_id
        new_edge = uml_element.ControlFlow(edge_id, flow_type, edge_name,
                                           node_id, merge_xmi_id, None)
        # 2c. the same time, create incoming
        # edge---incoming or outgoing
        incoming = uml_element.Incoming(edge_id)
        node_incomings.append(incoming)
        node.incomings = node_incomings
        # 3. create merge
        merge = uml_element.Merge(merge_xmi_id, xmi_type, name, merge_incomings, outgoings)
        # put into the dicts
        nodes_dict[merge_xmi_id] = merge
        edges_dict[edge_id] = new_edge

    def _create_decision(self, node_id, activity):
        ''' create a decision after the action, if the action has more than 2 outgoings
        1. change the 2 edges source to the decisionId
        2. create a edge between action and decision, at the same time,
        create a outgoing,incoming, their xmi_idref is the id of edge,
        and change the outgoings of the action, incomings of the decision
        3. create a decision
        4. put the decision, edge to the dicts
        @param node_id: the id of the node
        @type node_id: str
        '''
        nodes_dict = activity.nodes_dict
        edges_dict = activity.edges_dict
        # get the node
        node = nodes_dict[node_id]
        # get the decision id
        # decision_id1,decision_id2
        decision_xmi_id = self._get_new_id("decision", nodes_dict)
        # "uml:DecisionNode"
        xmi_type = uml_element.Types.DECISION_NODE
        name = decision_xmi_id
        decision_outgoings = []
        node_outgoings = []
        # 1. change the 2 edges attribute source to the decision
        outgoings = node.outgoings
        for outgoing in outgoings:
            outgoing_id = outgoing.xmi_idref
            edge = edges_dict[outgoing_id]
            if edge.xmi_type == uml_element.Types.CONTROL_FLOW:
                edge.source = decision_xmi_id
                decision_outgoings.append(outgoing)
            # object flow
            else:
                node_outgoings.append(outgoing)

        # 2. create a Incoming instance for merge, a ActivityEdge instance,
        # and a Outgoing instance for node
        # 2a. create a Incoming instance. edge_id is the xmi_id in edge,
        # also the xmi_idref of the instance Incoming
        # get the id of the edge
        edge_id = self._get_new_id("edge", edges_dict)
        edge_name = edge_id
        # create incoming
        incoming = uml_element.Incoming(edge_id)
        incomings = [incoming]
        # 2b. create a ActivityEdge instance. target: decision_xmi_id, source: node_id
        new_edge = uml_element.ControlFlow(edge_id, uml_element.Types.CONTROL_FLOW, \
                                           edge_name, decision_xmi_id, node_id, None)
        # 2c. the same time, create outgoing
        # edge---incoming or outgoing
        outgoing = uml_element.Outgoing(edge_id)
        node_outgoings.append(outgoing)
        node.outgoings = node_outgoings
        # 3. create decision
        decision = uml_element.Decision(decision_xmi_id, xmi_type,
                                        name, incomings, decision_outgoings)
        # put into the dicts
        nodes_dict[decision_xmi_id] = decision
        edges_dict[edge_id] = new_edge

    def action_has_more_incomings(self, activity):
        ''' if a action has more than one incoming control flow.
        if yes, create one merge before the action.
        yes: return True
        no:  return False
        '''
        nodes_dict = activity.nodes_dict
        edges_dict = activity.edges_dict
        # if are there one action has more incoming control flow
        ret = False
        ids = []
        for node_id in nodes_dict:
            node = nodes_dict[node_id]
            # if it is a action.
            if isinstance(node, uml_element.ExecutableNode):
                # the control flow number incomings
                control_flow_num = 0
                incomings = node.incomings
                # judge it is a control flow or a object flow
                for incoming in incomings:
                    edge_id = incoming.xmi_idref
                    edge = edges_dict[edge_id]
                    # it is control flow
                    if edge.xmi_type == uml_element.Types.CONTROL_FLOW:
                        control_flow_num += 1
                if  control_flow_num > 1:
                    log.show_info("the action name:%s,id:%s has %d control flow incomings"
                                  % (str(node.name), node.xmi_id, control_flow_num))
                    ids.append(node_id)
                    ret = True
        if ret:
            for node_id in ids:
                self._create_merge(node_id, activity, uml_element.Types.CONTROL_FLOW)
        return ids

    def action_has_more_outgoings(self, activity):
        ''' if a action has more than one outgoing. if yes, create one decision after the action.
        yes: return True
        no:  return False
        '''
        nodes_dict = activity.nodes_dict
        edges_dict = activity.edges_dict
        ret = False
        ids = []
        for node_id in nodes_dict:
            node = nodes_dict[node_id]
            if isinstance(node, uml_element.ExecutableNode):
                # the control flow number incomings
                control_flow_num = 0
                outgoings = node.outgoings
                # judge it is a control flow or a object flow
                for outgoing in outgoings:
                    edge_id = outgoing.xmi_idref
                    edge = edges_dict[edge_id]
                    # it is control flow
                    if edge.xmi_type == uml_element.Types.CONTROL_FLOW:
                        control_flow_num += 1
                if  control_flow_num > 1:
                    log.show_info("the action name:%s,id:%s has %d control flow outgoings"
                                  % (str(node.name), node.xmi_id, control_flow_num))
                    ids.append(node_id)
                    ret = True
        if ret:
            for node_id in ids:
                self._create_decision(node_id, activity)
        return ids

    def is_parallel(self, incomings, activity):
        '''if parallel
        '''

        edges_dict = activity.edges_dict
        ret = True

        first_incoming = incomings[0]
        first_edge_id = first_incoming.xmi_idref
        first_edge = edges_dict[first_edge_id]

        if first_edge.parallel:
            first_edge_fork_num = first_edge.fork_num
            for incoming in incomings:
                edge_id = incoming.xmi_idref
                edge = edges_dict[edge_id]
                if edge.parallel is False:
                    ret = False
                    break
                else:
                    fork_num = edge.fork_num
                    if fork_num != first_edge_fork_num:
                        ret = False
                        break
                    else:
                        # come from the same fork, but the same parallel_num, it is not parallel
                        pass
        else:
            ret = False
        return ret
    
    def check_probability(self, activity):
        '''check the probability of the control flow after a decision.
        if the sum of the probabilitys after the decision is more than 1, divide 
        '''
        nodes_dict = activity.nodes_dict
        edges_dict = activity.edges_dict
        for node_id in nodes_dict:
            node = nodes_dict[node_id]
            # it is a decision
            if node.xmi_type == uml_element.Types.DECISION_NODE:
                edges = []
                probs = []
                # the number of control flow outgoings
                cf_out_num = 0
                outgoings = node.outgoings
                for outgoing in outgoings:
                    edge_id = outgoing.xmi_idref
                    edge = edges_dict[edge_id]
                    if edge.xmi_type == uml_element.Types.CONTROL_FLOW:
                        cf_out_num += 1
                        edges.append(edge)
                        probs.append(edge.prob)
                # if the decision has more than one outgoing control flow
                if cf_out_num > 1:
                    if sum(probs) > 1:
                        prob = 1.0 / cf_out_num
                        for edge in edges:
                            edge.prob = prob

    def fork_has_more_incomings(self, activity):
        ''' if a fork has more than one incoming. if yes, create one merge before the fork.
        yes: return True
        no:  return False
        '''
        nodes_dict = activity.nodes_dict
        ret = False
        ids = []
        for node_id in nodes_dict:
            node = nodes_dict[node_id]
            if node.xmi_type == uml_element.Types.FORK_NODE:
                incomings = node.incomings
                num = len(incomings)
                if  num > 1:
                    # parallel = self.is_parallel(incomings, activity)
                    # if not parallel:
                    ids.append(node_id)
                    log.show_warn("the fork " + "name:" + str(node.name) + \
                                  " id:" + node.xmi_id + " has " + \
                                   str(num) + " incomings")
                    ret = True
        if ret:
            for node_id in ids:
                self._create_merge(node_id, activity, uml_element.Types.CONTROL_FLOW)

        return ids
    '''
    def find_next_place_nodes(self,node, activity,tokens_num):
    
        nodes_dict = activity.nodes_dict
        edges_dict = activity.edges_dict
        
        place_nodes =[uml_element.Types.DECISION_NODE,uml_element.Types.MERGE_NODE,uml_element.Types.FLOW_FINAL_NODE]
        warn_nodes = [uml_element.Types.FORK_NODE,uml_element.Types.JOIN_NODE]
        outgoings = node.outgoings
        for outgoing in outgoings:
            edge_id = outgoing.xmi_idref
            edge = edges_dict[edge_id]
            target = edge.target
            next_node_id = target
            next_node =nodes_dict[next_node_id]
            next_node_type =next_node.xmi_type
            if next_node_type in place_nodes:
                next_node.max_tokens = tokens_num
            elif next_node_type in warn_nodes:
                log.show_error("the merge in the fork connects to another fork or join.")
            else:
                self.find_next_place_nodes(next_node, activity, tokens_num)
    '''

    def set_tokens(self, merge, tokens_num):
        '''set_tokens
        '''
        merge.max_tokens = tokens_num
        # self.find_next_place_nodes(merge, activity,tokens_num)

    def get_tokens_num(self, merge, activity):
        '''first, judge if the incomings of the merge from the different parallel_num,
        if yes set the tokens to the number of the incomings.
        '''
        edges_dict = activity.edges_dict
        # the number of the place's tokens
        tokens_num = 1
        # the number of the parallel
        parallel_num = 0

        # for the edge, which edge.parallel is True
        edges = []
        for incoming in merge.incomings:
            edge_id = incoming.xmi_idref
            edge = edges_dict[edge_id]
            if edge.parallel:
                edges.append(edge)
            else:
                log.show_warn("the merge in the fork has a incoming," + \
                "but the incoming is not from the fork, the incoming comes from the outside")

        if len(edges) > 1:
            first_edge = edges[0]
            parallel_num = first_edge.parallel_num

        for edge in edges:
            # the edges come from the same fork, but different parallels
            if edge.parallel_num != parallel_num:
                tokens_num += 1

        if tokens_num > 1:
            self.set_tokens(merge, tokens_num)
            log.show_info("the merge has %d tokens. name:%s, id:%s"
                          % (tokens_num, str(merge.name), str(merge.xmi_id)))

    def get_next_nodes(self, node, fork_num, parallel_num, activity, merges):
        '''get the next activity nodes(s)
        @param fork_num: the number of the fork,from 1 to...
        @type fork_num: int
        @param parallel_num: the number of the parallel
        @type parallel_num: int
        '''

        nodes_dict = activity.nodes_dict
        edges_dict = activity.edges_dict

        # join, fork, activity final, flow final
        stop_types = [uml_element.Types.JOIN_NODE, uml_element.Types.FORK_NODE, \
                      uml_element.Types.ACTIVITY_FINAL_NODE, uml_element.Types.FLOW_FINAL_NODE]

        node_type = node.xmi_type

        if node_type in stop_types:
            return
        else:
            # if it is merge, put it in the merges list
            if node_type == uml_element.Types.MERGE_NODE:
                if node not in merges:
                    merges.append(node)
            else:
                outgoings = node.outgoings
                for outgoing in outgoings:
                    edge_id = outgoing.xmi_idref
                    edge = edges_dict[edge_id]
                    if edge.xmi_type == uml_element.Types.CONTROL_FLOW:
                        if edge.parallel is False:
                            edge.parallel = True
                            edge.fork_num = fork_num
                            edge.parallel_num = parallel_num
                            target = edge.target
                            next_node = nodes_dict[target]
                            self.get_next_nodes(next_node, fork_num, parallel_num, activity, merges)
                        else:
                            log.show_warn("the edge is Already in parallel")

    def _get_actions_objects(self, fork, num, activity, set_initial):
        '''get the actions objects in the parallel process(fork,join).
        '''
        nodes_dict = activity.nodes_dict
        edges_dict = activity.edges_dict
        # get the control flow from node to node2
        # actions save the node2
        actions = []
        objects = []
        for outgoing in fork.outgoings:
            found = set_initial
            edge_id = outgoing.xmi_idref
            edge = edges_dict[edge_id]
            node2_id = edge.target
            node2 = nodes_dict[node2_id]
            # if it is a join
            if node2.xmi_type == uml_element.Types.JOIN_NODE:
                # set the parallel_num of join
                node2.parallel_num = num
                # change the name of join, fork and join have the same name
                node2.name = "parallel" + str(num)
                continue
            # if it is a action
            elif isinstance(node2, uml_element.ExecutableNode):
                if node2 not in actions:
                    actions.append(node2)
                    if not found:
                        node2.initial = True
                        found = True
            elif isinstance(node2, uml_element.ObjectNode):
                if node2 not in objects:
                    objects.append(node2)
            # go on get the next_actions,objects
            next_actions, next_objects = self._get_actions_objects(node2, num, activity,found)
            # put the action to the actions
            for node in next_actions:
                if node not in actions:
                    actions.append(node)
            # put the objects to the objects
            for node in next_objects:
                if node not in objects:
                    objects.append(node)
        return actions, objects

    def get_parallel_process(self, activity):
        '''get the parallel process (action and object node) in the fork and join.
        '''
        nodes_dict = activity.nodes_dict
        num = 0
        for node_id in nodes_dict:
            node = nodes_dict[node_id]
            # if it is fork
            if node.xmi_type == uml_element.Types.FORK_NODE:
                num += 1
                # set the parallel_num of fork 
                node.parallel_num = num
                # change the name of fork
                node.name = "parallel" + str(num)
                actions, objects = self._get_actions_objects(node, num, activity, False)
                # set the parallel as True and the parallel_num
                for action in actions:
                    action.parallel = True
                    action.parallel_num = num
                    log.show_info("the action:%s is in parallel_num:%d process" % (action.name, num))
                for object_node in objects:
                    object_node.parallel = True
                    object_node.parallel_num = num
                    log.show_info("the object node:%s is in parallel_num:%d process" % (object_node.name, num))
       
    def get_parallel_edges(self, activity):
        '''get the parallel edges in the fork.
        for example, fork1 has 2 parallel edge, the first edge's fork_num =1, parallel_num =1
        the second edge's fork_num =1, parallel_num =2
        fork2 has 2 parallel edge, the first edge's fork_num =2, parallel_num =1
        the second edge's fork_num =2, parallel_num =2
        '''

        nodes_dict = activity.nodes_dict
        edges_dict = activity.edges_dict

        # the merges list
        # see the example payOrder
        merges = []
        # the number of the fork,from 1 to...
        fork_num = 0

        for node_id in nodes_dict:
            node = nodes_dict[node_id]
            # if it is fork
            if node.xmi_type == uml_element.Types.FORK_NODE:
                fork_num += 1
                # the number of the parallel
                parallel_num = 0
                outgoings = node.outgoings
                for outgoing in outgoings:
                    parallel_num += 1
                    edge_id = outgoing.xmi_idref
                    edge = edges_dict[edge_id]
                    if edge.xmi_type == uml_element.Types.CONTROL_FLOW:
                        if edge.parallel is False:
                            edge.parallel = True
                            edge.fork_num = fork_num
                            edge.parallel_num = parallel_num
                            target = edge.target
                            next_node = nodes_dict[target]
                            self.get_next_nodes(next_node, fork_num, parallel_num, activity, merges)
                        else:
                            log.show_warn("the edge is Already in parallel")
        for merge in merges:
            self.get_tokens_num(merge, activity)

    '''
    def connect_nodes(self,activity,node1_id, node2_id, node3_id):
        nodes_dict = activity.nodes_dict
        edges_dict = activity.edges_dict
        
        node1 = nodes_dict[node1_id]
        node2 = nodes_dict[node2_id]
        node3 = nodes_dict[node3_id]
        
        for outgoing in node1.outgoings:
            edge_id = outgoing.xmi_idref
            edge = edges_dict[edge_id]
            target = edge.target
            if target == node2.id:
                edge.target = node3.id
        
         
        for incoming in node3.incomings:
            edge_id = outgoing.xmi_idref
            edge = edges_dict[edge_id]
            source = edge.source
            if source == node2_id:
                node3.incomings.remove(source)
                
        print node1.name,node1.xmi_id
        print node2.name,node2.xmi_id
        print node3.name,node3.xmi_id
        
        
    def analyse_object_node(self,activity):
        nodes_dict = activity.nodes_dict
        edges_dict = activity.edges_dict
        
        for edge_Id in edges_dict:
            # get the source, target of the edge
            edge = edges_dict[edge_Id] 
            source = edge.source
            target = edge.target
            
            if source in nodes_dict:
                node1_id = source
                node1 = nodes_dict[node1_id]
            if target in nodes_dict:
                node2_id = target
                node2 = nodes_dict[node2_id]
                
            if node1.petri and not node2.petri:  
                outgoings = node2.outgoings
                if len(outgoings)==0:
                    log.show_warn("the object node has no outgoing."+"name:"+str(node2.nama)+"id:"+node2.xmi_id)
                elif len(outgoings)>1:
                    log.show_warn("the object node has more than 1 outgoings."+"name:"+str(node2.nama)+"id:"+node2.xmi_id)
                elif len(outgoings)==1:
                    outgoing = outgoings[0]
                    xmi_idref = outgoing.xmi_idref
                    edge = edges_dict[xmi_idref]
                    target = edge.target
                    if target in nodes_dict:
                        node3_id = target
                        node3 = nodes_dict[node3_id]
                        if node3.petri:
                            self.connect_nodes(activity,node1_id,node2_id,node3_id)
                        else:
                            log.show_warn("the node3 can not be transformed to petri net."+"name:"+str(node3.nama)+"id:"+node3.xmi_id)
     '''
