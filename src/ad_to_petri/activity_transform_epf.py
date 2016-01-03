'''
Created on 27.11.2015

@author: Kai
'''
from bean import uml_activity_diagram_element as uml_element
import log

class AdToEpfTransformer(object):
    '''transform the activity diagram to error model.
    '''
      
    def _get_next_actions(self, node, action_ids, activity, prob):
        '''get the actions from node.
        such as,
        node-->nodes
        node -->decision-->nodes,
        node-->fork
        join-->node
        '''
        nodes_dict = activity.nodes_dict
        edges_dict = activity.edges_dict
        # get the control flow from node to node2
        # nodes save the node2
        nodes = []
        #  save the cf_probs from node to node2
        cf_probs = []
        for outgoing in node.outgoings:
            edge_id = outgoing.xmi_idref
            edge = edges_dict[edge_id]
            # control flow
            if edge.xmi_type == uml_element.Types.CONTROL_FLOW:
                cf_prob = prob * edge.prob
                node2_id = edge.target
                node2 = nodes_dict[node2_id]
                if node2_id in action_ids:
                    if node2 not in nodes:
                        nodes.append(node2)
                        cf_probs.append(cf_prob)
                else:
                    next_nodes, probs = self._get_next_actions(node2, action_ids, activity, cf_prob)
                    for index in range(len(next_nodes)):
                        node = next_nodes[index]
                        _prob = probs[index]
                        if node not in nodes:
                            nodes.append(node)
                            cf_probs.append(_prob)
        return nodes, cf_probs

    def _get_data_flow(self, object_node_ids, action_ids, activity):
        '''get the data flow in activity diagram.
        also action1 to object, object to action2
        @type object_node_ids: list
        @type action_ids: list
        @return: data_flows,[(from,to),(from,to)...]
        @rtype: list
        '''
        # it is a list: [(from,to),(from,to)..]
        data_flows = []
        nodes_dict = activity.nodes_dict
        edges_dict = activity.edges_dict
        for node_id in object_node_ids:
            object_node = nodes_dict[node_id]
            incomings = object_node.incomings
            outgoings = object_node.outgoings
            # get name
            data_name = object_node.name
            # from element to object node(data)
            for incoming in incomings:
                edge_id = incoming.xmi_idref
                edge = edges_dict[edge_id]
                source = edge.source
                source_node = nodes_dict[source]
                if source in action_ids:
                    element_name = source_node.name
                    data_flows.append((element_name, data_name))
                else:
                    log.show_warn("the source of the object node is not a element")
            # from object node(data) to element
            for outgoing in outgoings:
                edge_id = outgoing.xmi_idref
                edge = edges_dict[edge_id]
                target = edge.target
                target_node = nodes_dict[target]
                if target in action_ids:
                    element_name = target_node.name
                    data_flows.append((data_name, element_name))
                else:
                    log.show_warn("the target of the object node is not a element")
        return data_flows

    def _get_control_flows(self, action_ids, activity):
        '''get the control flow in activity diagram.
        also action1 to action2
        @return: control_flows,[(from,to,prob),(from,to,prob)...]
        '''
        control_flows = []
        nodes_dict = activity.nodes_dict
        for node_id in action_ids:
            temp = False
            node1 = nodes_dict[node_id]
            # no control flow from fork, just control flow from join
            # no control flow to join, just control flow to fork
            if node1.xmi_type == uml_element.Types.FORK_NODE:
                pass
            else:
                # get the next nodes from node1, also node1-->nodes....
                nodes, probs = self._get_next_actions(node1, action_ids, activity, 1)
                # the probs is more than 1
                if sum(probs) > 1:
                    temp = True
                    log.show_warn("the sum of edge probabilitys after the node:%s is more than 1" % node1.name)
                for index in range(len(nodes)):
                    node2 = nodes[index]
                    # no control flow to join
                    if node2.xmi_type == uml_element.Types.JOIN_NODE:
                        pass
                    else:
                        # the prob
                        prob = probs[index]
                        if temp:
                            prob = 1.0 / len(nodes)
                        # get corrected name
                        name1 = node1.name
                        name2 = node2.name
                        control_flows.append((name1, name2, prob))

        return control_flows

    def _get_elements_datas(self, action_ids, object_node_ids, activity, model):
        '''get the elements, also the names of actions(initial,final) in activity diagram,
        for parallel process fork und join.
        and get the datas, also the name of object node
        #TODO the pin,pout
        @return: the name of actions(initial,final), but the first one is initial node name
        @rtype: list
        '''
        elements = []
        datas = []
        nodes_dict = activity.nodes_dict
        for node_id in nodes_dict:
            node = nodes_dict[node_id]
            name = node.name
            if isinstance(node, uml_element.Fork):
                action_ids.append(node_id)
                elements.append(name)
                model.add_element(name)
                model.set_subsystem_parallel(name)
        for node_id in nodes_dict:
            node = nodes_dict[node_id]
            name = node.name
            # if it is initial node
            if isinstance(node, uml_element.InitialNode):
                action_ids.append(node_id)
                model.add_element(name)
                model.set_initial_element(name)
            # if the node is action, initial, final
            elif isinstance(node, uml_element.ExecutableNode):
                action_ids.append(node_id)
                elements.append(name)
                if node.parallel:
                    host = 'parallel' + str(node.parallel_num)
                    model.add_element(name, host)
                    if node.initial:
                        model.set_initial_element(name)
                else:
                    model.add_element(name)
            elif isinstance(node, uml_element.FinalNode):
                action_ids.append(node_id)
                elements.append(name)
                model.add_element(name)
            # else the node is object node
            elif isinstance(node, uml_element.ObjectNode):
                object_node_ids.append(node_id)
                datas.append(name)
                if node.parallel:
                    host = 'parallel' + str(node.parallel_num)
                    model.add_data(name, host)
                else:
                    model.add_data(name)
            elif isinstance(node, uml_element.Join):
                action_ids.append(node_id)
                # attention: do not create a element, because fork and join together is a element
        return elements, datas

    def transform_to_epf(self, activity, model):
        '''transform the activity diagram to error model.
        return: model
        '''
        # clear the epf model
        model.clear()
        # get the name
        model.name = activity.name

        nodes_dict = activity.nodes_dict
        pins_dict = activity.pins_dict
        edges_dict = activity.edges_dict

        # save the id of actions
        action_ids = []
        # save the id of the object_node
        object_node_ids = []

        elements, datas = self._get_elements_datas(action_ids, object_node_ids, activity, model)
        control_flows = self._get_control_flows(action_ids, activity)
        data_flows = self._get_data_flow(object_node_ids, action_ids, activity)

        # add control flow
        for cf_from, cf_to, prob in control_flows:
            model.add_cf_arc(cf_from, cf_to, prob)

        # add data flow
        for df_from, df_to  in data_flows:
            model.add_df_arc(df_from, df_to)
        
        # pout--> pin, the two elements come in together
        for pin_id in pins_dict:
            # action with pout
            pout = pins_dict[pin_id]
            if isinstance(pout, uml_element.Result):
                name = pout.name
                node1_id = pout.host
                node1 = nodes_dict[node1_id]
                # add data, pout.name
                model.add_data(name)
                # add data flow from node1 to pout
                model.add_df_arc(node1.name, name)
                outgoings = pout.outgoings
                for outgoing in outgoings:
                    edge_id = outgoing.xmi_idref
                    edge = edges_dict[edge_id]
                    target = edge.target
                    if target in nodes_dict:
                        node2 = nodes_dict[target]
                        model.add_df_arc(name, node2.name)
                        log.show_warn("pout has a outgoing node")
                    elif target in pins_dict:
                        # action with pin
                        pin = pins_dict[target]
                        node2_id = pin.host
                        node2 = nodes_dict[node2_id]
                        model.add_df_arc(name, node2.name)
        
        '''
        print model.elements  # key = element name
        print model.data  # key = data name
        print model.cf_probs  # key =  "(from,to)", value = prob
        print model.subsystems  # key = host, value = {intial_element, elements, data}
        '''
        model.xml.save(activity.name + "_epf.xml")
        # model.checking.check()
        # model.acknowledge_all_conditions()
        #model.xml.load(activity.name + "_epf.xml")
        
        
        model.drawing.draw_system(activity.name + "_epf.png")

        return model
