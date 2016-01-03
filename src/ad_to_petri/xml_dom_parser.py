'''
Created on 13.09.2015

@author: Kai
'''
import sys
sys.path.insert(0, '..\\..\\src')
from xml.dom import minidom, Node
from bean import uml_activity_diagram_element as uml_element
import log
class XmlParser(object):
    '''xml parser for parsing
    '''
    def get_child_nodes(self, node, tag_name):
        '''childNodes is just for the first level child nodes
        cf: node.getElementsByTagName(tag_name) returns all levels child nodes
        see https://docs.python.org/2/library/xml.dom.html
        All of the components of an XML document are subclasses of Node.
        Element is a subclass of Node, so inherits all the attributes of that class.
        ELEMENT_NODE                = 1     element can has child nodes , nodeName
        ATTRIBUTE_NODE              = 2
        TEXT_NODE                   = 3     text has no child nodes,
                nodeValue is just for TEXT_NODE, .data
        @param node: xml node
        @type node: xml.dom.Node (attention: it is not a instance of
            uml_activity_diagram_element.Node)
        @param tag_name: the tag_name in xml
        @type tag_name: str
        @return: the childNodes, which tag_name = tag_name
        @rtype: Nodelist
        '''
        nodes = []
        for child_node in node.childNodes:
            # if it is ELEMENT_NODE and its tageName==tag_name
            if child_node.nodeType == Node.ELEMENT_NODE and child_node.tagName == tag_name:
                nodes.append(child_node)
        return nodes

    def get_exporter_version(self, documentation):
        '''1.exporter:MagicDraw UML.exportVersion:18.2
        <xmi:Documentation>
            <xmi:exporter>MagicDraw UML</xmi:exporter>
            <xmi:exporterVersion>18.2</xmi:exporterVersion>
        </xmi:Documentation>
        2. exporter:Enterprise Architect.exportVersion:6.5
        <xmi:Documentation exporterVersion="6.5" exporter="Enterprise Architect"/>
        '''
        exporter = None
        export_version = None
        # EA
        if documentation.hasAttribute("exporter"):
            # Return the value of the attribute named by name as a string.
            # If no such attribute exists, an empty string is returned,
            # as if the attribute had no value.
            exporter = documentation.getAttribute("exporter")
        # Magic Draw
        else:
            child_node = self.get_child_nodes(documentation, "xmi:exporter")[0]
            for child in child_node.childNodes:
                # get the exporter
                if child.nodeType == Node.TEXT_NODE:
                    exporter = child.data
        # EA
        if documentation.hasAttribute("exporterVersion"):
            # Return the value of the attribute named by name as a string.
            # If no such attribute exists, an empty string is returned,
            # as if the attribute had no value.
            export_version = documentation.getAttribute("exporterVersion")
        # Magic Draw
        else:
            child_node = self.get_child_nodes(documentation, "xmi:exporterVersion")[0]
            for child in child_node.childNodes:
                # exporterVersion
                if child.nodeType == Node.TEXT_NODE:
                    export_version = child.data
        return exporter, export_version

    def get_id_name_type(self, node):
        '''get the attribute--xmi:id, name,xmi:type
        @param node: xml node
        @type node: xml.dom.Node (attention: it is not a instance of
            uml_activity_diagram_element.ActivityNode)
        @return: xmi_id,name,xmi_type
        @rtype: xmi_id--str, name--str, xmi_type--str
        '''
        xmi_id = None
        name = None
        xmi_type = None
        if node.hasAttribute("xmi:id"):
            # Return the value of the attribute named by name as a string.
            # If no such attribute exists, an empty string is returned,
            # as if the attribute had no value.
            xmi_id = node.getAttribute("xmi:id")
        # it is a error, if node has no xmi:id
        else:
            if node.nodeName == "edge":
                log.show_warn("edge has no xmi:id attribute")
            else:
                log.show_warn("node has no xmi:id attribute")
        # get the name of the node
        if node.hasAttribute("name"):
            name = node.getAttribute("name")
        # get the type of the node
        if node.hasAttribute("xmi:type"):
            xmi_type = node.getAttribute("xmi:type")
        # it is a error, if node has no xmi:type
        else:
            if node.nodeName == "edge":
                log.show_warn("edge has no xmi:type attribute")
            else:
                log.show_warn("node has no xmi:type attribute")
        return xmi_id, name, xmi_type

    def get_behavior(self, node):
        '''get the behavior of a call behavior action
        action has no behavior, also behavior is None
        '''
        behavior = None
        if node.hasAttribute("behavior"):
            # Return the value of the attribute named by name as a string.
            # If no such attribute exists, an empty string is returned,
            # as if the attribute had no value.
            behavior = node.getAttribute("behavior")
        return behavior

    def get_time_base_element(self, node):
        '''get the attribute time, base_Element
        <Data:Time xmi:id="_18_4353" time="20s" base_Element="_18_4248"/>

        <thecustomprofile:Time Time="50s" base_CallBehaviorAction="EAID_647FB"/>
        <thecustomprofile:time time="25s" base_Action="EAID_46FBB"/>
        @param node: xml node
        @type node: xml.dom.Node (attention: it is not a instance of
            uml_activity_diagram_element.ActivityNode)
        '''
        time = None
        base_element = None
        if node.hasAttribute("time"):
            # Return the value of the attribute named by name as a string.
            # If no such attribute exists, an empty string is returned,
            # as if the attribute had no value.
            time = node.getAttribute("time")
        # "exp" or "const"
        if node.hasAttribute("type"):
            time_type = node.getAttribute("type")
        else:
            time_type = "const"
        # get the name of the node
        if node.hasAttribute("base_Element"):
            base_element = node.getAttribute("base_Element")
        elif node.hasAttribute("base_Action"):
            base_element = node.getAttribute("base_Action")
        return time, base_element, time_type

    def get_incomings(self, node):
        '''get the incomings list of the xml-node.
        create instances of uml_activity_diagram_element.Incoming
        incoming = uml_activity_diagram_element.Incoming(xmi_idref)
        and put them in the incoming list
        @param node: xml node
        @type node: xml.dom.Node (attention: it is not a instance of
            uml_activity_diagram_element.ActivityNode)
        @return: incomings
        @rtype: list [instance1 of uml_activity_diagram_element.Incoming,
            instance2 of uml_activity_diagram_element.Incoming...]
        '''
        incomings = []
        # get the incomings of the node
        node_incomings = self.get_child_nodes(node, 'incoming')
        # incomingsTag = node.getElementsByTagName('incoming')
        for node_incoming in node_incomings:
            if node_incoming.hasAttribute("xmi:idref"):
                xmi_idref = node_incoming.getAttribute("xmi:idref")
                incoming = uml_element.Incoming(xmi_idref)
                if incoming not in incomings:
                    incomings.append(incoming)
            else:
                log.show_error("node's incoming has no id")
        return incomings

    def get_outgoings(self, node):
        '''get the outgoings list of the xml-node.
        create instances of uml_activity_diagram_element.Outgoing
        outgoing = uml_activity_diagram_element.Outgoing(xmi_idref)
        and put them in the outgoings list
        @param node: xml node
        @type node: xml.dom.Node (attention: it is not a instance of
            uml_activity_diagram_element.ActivityNode)
        @return: outgoings
        @rtype: list [instance1 of uml_activity_diagram_element.Outgoing,
            instance2 of uml_activity_diagram_element.Outgoing...]
        '''
        outgoings = []
        # get the outgoings of the node
        node_outgoings = self.get_child_nodes(node, 'outgoing')
        # outgoingsTag = node.getElementsByTagName('outgoing')
        for node_outgoing in node_outgoings:
            if node_outgoing.hasAttribute("xmi:idref"):
                xmi_idref = node_outgoing.getAttribute("xmi:idref")
                outgoing = uml_element.Outgoing(xmi_idref)
                if outgoing not in outgoings:
                    outgoings.append(outgoing)
            else:
                log.show_error("node's outgoing has no id")
        return outgoings

    def get_results(self, node, xmi_id):
        '''get the results list of the xml-node.
        creat instances of uml_activity_diagram_element.Result
        result = uml_activity_diagram_element.Result(xmi_id, xmi_type, name, outgoings)
        and put them in the results list
        @param node: xml node
        @type node: xml.dom.Node (attention: it is not a instance of
            uml_activity_diagram_element.ActivityNode)
        @return: results
        @rtype: list [instance1 of uml_activity_diagram_element.Result,
            instance2 of uml_activity_diagram_element.Result...]
        '''
        # the id of the activity node
        node_id = xmi_id
        results = []
        node_results = self.get_child_nodes(node, "result")
        for node_result in node_results:
            xmi_id, name, xmi_type = self.get_id_name_type(node_result)
            # get outgoings
            outgoings = self.get_outgoings(node_result)
            result = uml_element.Result(xmi_id, xmi_type, name, outgoings, node_id)
            results.append(result)
        return results

    def get_arguments(self, node, xmi_id):
        '''get the arguments list of the xml-node.
        creat instances of uml_activity_diagram_element.Argument
        argument = uml_activity_diagram_element.Argument(xmi_id, xmi_type, name, incomings)
        and put them in the arguments list
        @param node: xml node
        @type node: xml.dom.Node (attention: it is not a instance of
            uml_activity_diagram_element.ActivityNode)
        @return: arguments
        @rtype: list [instance1 of uml_activity_diagram_element.Argument,
            instance2 of uml_activity_diagram_element.Argument...]
        '''
        # the id of the activity node
        node_id = xmi_id
        arguments = []
        node_arguments = self.get_child_nodes(node, "argument")
        for node_argument in node_arguments:
            xmi_id, name, xmi_type = self.get_id_name_type(node_argument)
            # get incomings
            incomings = self.get_incomings(node_argument)
            argument = uml_element.Argument(xmi_id, xmi_type, name, incomings, node_id)
            arguments.append(argument)
        # TODO <target /> just one target tag in receive node
        node_targets = self.get_child_nodes(node, "target")
        for node_target in node_targets:
            xmi_id, name, xmi_type = self.get_id_name_type(node_target)
            # get incomings
            incomings = self.get_incomings(node_target)
            argument = uml_element.Argument(xmi_id, xmi_type, name, incomings, node_id)
            arguments.append(argument)
        return arguments

    def get_target_source(self, edge):
        '''get the target, source of the edge (xml.dom.Node)
        @param edge: xml.dom.Node---<edge...../>
        @type edge: (xml.dom.Node)
        @return: target,source
        @rtype: str
        '''
        target = None
        source = None
        # get the target of the edge
        if edge.hasAttribute("target"):
            target = edge.getAttribute("target")
        else:
            log.show_warn("edge has no target....")
        # get the target of the edge
        if edge.hasAttribute("source"):
            source = edge.getAttribute("source")
        else:
            log.show_warn("edge has no source....")
        return target, source

    def get_guard(self, edge):
        '''get the guard instance of the edge (xml.dom.Node)
        create guard = uml_activity_diagram_element.Guard(xmi_id, xmi_type,name, body, language)
        @param edge: xml.dom.Node---<edge...../>
        @type edge: (xml.dom.Node)
        @return: guard
        @rtype: instance of uml_activity_diagram_element.Guard
        1.
        <edge xmi:type="uml:ControlFlow" xmi:id="EAID_34E5" target="EAID_5AC48" source="EAID_7892">
            <guard xmi:type="uml:OpaqueExpression" xmi:id="EAID_34E5" body="yes"/>
        </edge>
        2.
        <edge xmi:id="_18_4292" xmi:type="uml:ControlFlow" target="_18_4262" source="_18_4235">
            <guard xmi:id="_18_4415" xmi:type="uml:OpaqueExpression">
                <body>incorrect</body>
                <language>English</language>
            </guard>
        </edge>
        '''
        guard = None
        for child_node in edge.childNodes:
            # if it has child node "guard"
            if child_node.nodeType == Node.ELEMENT_NODE and child_node.tagName == "guard":
                # get the id, name, type of the guard(child_node)
                xmi_id, name, xmi_type = self.get_id_name_type(child_node)
                body = None
                language = None
                # it is for EA
                if child_node.hasAttribute("body"):
                    body = child_node.getAttribute("body")
                # it is for Magic Draw
                else:
                    for child in child_node.childNodes:
                        # get the body
                        if child.nodeType == Node.ELEMENT_NODE and child.tagName == "body":
                            if len(child.childNodes) > 0:  # <body/>
                                body = child.childNodes[0].data
                        # get the language
                        elif child.nodeType == Node.ELEMENT_NODE and child.tagName == "language":
                            if len(child.childNodes) > 0:
                                language = child.childNodes[0].data
                guard = uml_element.Guard(xmi_id, xmi_type, name, body, language)
        return guard

    def create_node_object(self, nodes_dict, xmi_id, xmi_type, name, \
                          incomings, outgoings, results, arguments, behavior):
        '''create instance of uml_activity_diagram_element.ActivityNode
        from the xmi_type
        '''
        if xmi_type == uml_element.Types.INITIAL_NODE:
            initial_node = uml_element.InitialNode(xmi_id, xmi_type, name, incomings, outgoings)
            nodes_dict[xmi_id] = initial_node
        elif xmi_type == uml_element.Types.CALLBEHAVIOR_ACTION:
            action_node = uml_element.Action(xmi_id, xmi_type, name, \
                                             incomings, outgoings, results, arguments)
            action_node.behavior = behavior
            nodes_dict[xmi_id] = action_node
        elif xmi_type == uml_element.Types.ACTION:
            action_node = uml_element.Action(xmi_id, xmi_type, name, \
                                             incomings, outgoings, results, arguments)
            action_node.behavior = None
            nodes_dict[xmi_id] = action_node
        elif xmi_type == uml_element.Types.SEND_SIGNAL_ACTION:
            send_signal_action = uml_element.SendSignalAction(xmi_id, xmi_type, name, \
                                                    incomings, outgoings, results, arguments)
            nodes_dict[xmi_id] = send_signal_action
        elif xmi_type == uml_element.Types.ACCEPT_EVENT_ACTION:
            accept_event_action = uml_element.AcceptEventAction(xmi_id, xmi_type, name, \
                                                    incomings, outgoings, results, arguments)
            nodes_dict[xmi_id] = accept_event_action
        elif xmi_type == uml_element.Types.FORK_NODE:
            # for EA
            if len(outgoings) == 1 and len(incomings) > 1:
                join_node = uml_element.Join(xmi_id, uml_element.Types.JOIN_NODE, name, \
                                             incomings, outgoings)
                nodes_dict[xmi_id] = join_node
            else:
                fork_node = uml_element.Fork(xmi_id, xmi_type, name, incomings, outgoings)
                nodes_dict[xmi_id] = fork_node
        elif xmi_type == uml_element.Types.JOIN_NODE:
            join_node = uml_element.Join(xmi_id, xmi_type, name, incomings, outgoings)
            nodes_dict[xmi_id] = join_node
        elif xmi_type == uml_element.Types.ACTIVITY_FINAL_NODE:
            final_node = uml_element.ActivityFinal(xmi_id, xmi_type, name, incomings, outgoings)
            nodes_dict[xmi_id] = final_node
        elif xmi_type == uml_element.Types.FLOW_FINAL_NODE:
            flow_final_node = uml_element.FlowFinal(xmi_id, xmi_type, name, incomings, outgoings)
            nodes_dict[xmi_id] = flow_final_node
        elif xmi_type == uml_element.Types.MERGE_NODE:
            merge = uml_element.Merge(xmi_id, xmi_type, name, incomings, outgoings)
            nodes_dict[xmi_id] = merge
        elif xmi_type == uml_element.Types.DECISION_NODE:
            decision = uml_element.Decision(xmi_id, xmi_type, name, incomings, outgoings)
            nodes_dict[xmi_id] = decision
        # ObjectNode
        elif xmi_type == uml_element.Types.OBJECT_NODE:
            object_node = uml_element.ObjectNode(xmi_id, xmi_type, name, incomings, outgoings)
            nodes_dict[xmi_id] = object_node
        elif xmi_type == uml_element.Types.DATA_STORE_NODE:
            data_store_node = uml_element.DataStore(xmi_id, xmi_type, name, incomings, outgoings)
            nodes_dict[xmi_id] = data_store_node
        else:
            log.show_warn("the type of the node is not defined " + xmi_type)

    def create_edge_object(self, edges_dict, xmi_id, xmi_type, name, target, source, guard):
        '''create instance of uml_activity_diagram_element.ActivityEdge
        from the xmi_type
        '''
        if xmi_type == uml_element.Types.CONTROL_FLOW:
            edge = uml_element.ControlFlow(xmi_id, xmi_type, name, target, source, guard)
            edges_dict[xmi_id] = edge
            # get the probability from the guard of the control flow(edge)
            cf_prob = self._get_cf_prob_from_text(guard)
            edge.prob = cf_prob

        elif xmi_type == uml_element.Types.OBJECT_FLOW:
            edge = uml_element.ObjectFlow(xmi_id, xmi_type, name, target, source, guard)
            edges_dict[xmi_id] = edge
        else:
            log.show_warn("the edge is not control flow, neither object flow")

    def get_time(self, str_time):
        '''get the real time.
        @param str_time: the time str, such as "20ms","25s"
        @type str_time: str
        @return: time
        @rtype: float
        '''
        if str_time is None:
            return
        original_str = str_time
        time = None
        unit = None
        # factor: ms-->0.01, s-->1, min-->60
        # default is "s"
        factor = None
        # delete all ' ', for example " 20 m s"-->"20ms"
        str_time = str_time.replace(' ', '')
        # if it is ""
        if len(str_time) == 0:
            log.show_error("the time is empty string,Please modify it ")
        elif str_time.endswith('ms'):
            unit = "ms"
            factor = 0.001
        elif str_time.endswith('s'):
            unit = "s"
            factor = 1
        elif str_time.endswith('min'):
            unit = "min"
            factor = 60
        elif str_time.endswith('h'):
            unit = "h"
            factor = 60 * 60
        elif str_time.endswith('d'):
            unit = "d"
            factor = 60 * 60 * 24
        elif str_time.endswith('mon'):
            unit = "mon"
            factor = 60 * 60 * 24 * 30
        elif str_time.endswith('y'):
            unit = "y"
            factor = 60 * 60 * 24 * 30 * 12
        else:
            log.show_error("the unit of the time is invalid,Please modify it " + original_str)
            exit(0)
        # delete the unit from the right end of the str_time
        str_time = str_time.rstrip(unit)
        try:
            # str to float
            time = float(str_time)
        except ValueError:
            log.show_error("the time is invalid,Please modify it " + original_str)
        time = time * factor
        return time

    def set_time(self, str_time, base_element, time_type, model):
        '''set the time property of action
        '''
        for activity_id in model.activitys_dict:
            activity = model.activitys_dict[activity_id]
            nodes_dict = activity.nodes_dict
            if base_element in nodes_dict:
                node = nodes_dict[base_element]
                time = self.get_time(str_time)
                # it is not immediate
                node.immediate = False
                if time_type == "const":
                    node.deterministic = True
                elif time_type == "exp":
                    node.exponential = True
                else:
                    log.show_warn("the type of the time is not defined.type:%s" % time_type)
                    # set it to default deterministic
                    node.deterministic = True
                node.time = time
                log.show_info("the action has time property.name:%s,id:%s,time:%s" % 
                              (str(node.name), node.xmi_id, str_time))
                break
            # else:
            #    log.show_warn("the base_Element "+base_element+" is not in the nodes_dict")
    
    def _get_cf_prob_from_text(self, guard):
        '''get the cf_prob from text of guard.
        for example: 
        [...prob:0.25]
        [...prob=0.25]
        [...pro:0.25]
        [...pro=0.25]
        [...pr:0.25]
        [...pr=0.25]
        '''
        prob = 1
        if guard is None:
            # cf_prob is default 1, also edge.prob =1
            return 1
        # delete the " "
        guard_body = guard.body.replace(' ', '')
        possibles = ["prob:", "prob=", "pro:", "pro=", "pr:", "pr="]
        index = -1
        for possible_str in possibles:
            # find it from right
            index = guard_body.rfind(possible_str)
            if index != -1:
                # the length
                num = len(possible_str)
                break

        if index != -1:
            # find the number_str, such as "0.5"
            prob_str = guard_body[(index + num):]
            try:
            # str to float
                prob = float(prob_str)
            except ValueError:
                log.show_error("the prob is invalid,Please modify it " + prob_str)
            # if it is less than 0 or more than one
            if (prob <= 0.0) or (prob > 1.0):
                log.show_error("the prob should be a number between 0 and 1")
            # if it is not default one
            if prob != 1:
                # show info
                log.show_info("the guard:%s, has cf_prob:%f" % (guard_body, prob))
        return prob

    def __set_pins_dict(self, pins_dict, results, arguments):
        '''put all the results and arguments in the pins_dict
        '''
        for result in results:
            xmi_id = result.xmi_id
            pins_dict[xmi_id] = result
        for argument in arguments:
            xmi_id = argument.xmi_id
            pins_dict[xmi_id] = argument

    def xml_parse(self, xml_path):
        '''start the parsing
        @param xml_path: the path of the xml
        @attention: the different between windows and Linux
        '''
        # use minidom to open the xml
        try:
            DOMTree = minidom.parse(xml_path)
            # collection = DOMTree.documentElement
        except IOError:
            log.show_error("the xml is wrong")

        # get the root tag of the xml
        root = DOMTree.documentElement

        # get the tag: <xmi:Documentation>
        # get the exporter(Magic Draw or EA) and exporterVersion
        documentation = self.get_child_nodes(root, "xmi:Documentation")[0]
        exporter, export_version = self.get_exporter_version(documentation)

        log.show_info("exporter:" + exporter + ".exportVersion:" + export_version)

        # get <uml:Model  />
        model_node = self.get_child_nodes(root, "uml:Model")[0]
        # the 4 parameters: xmi_id, xmi_type, name, activitys_dict
        xmi_id, name, xmi_type = self.get_id_name_type(model_node)

        activitys_dict = {}
        # create the model
        model = uml_element.Model(xmi_id, xmi_type, name, activitys_dict)
        # get <packagedElement>
        # packaged_elements = self.get_child_nodes(model_node, "packagedElement")
        packaged_elements = model_node.getElementsByTagName("packagedElement")


        InstanceSpecification_nodes = []
        activity_id = None
        for packaged_element in packaged_elements:
            xmi_id, name, xmi_type = self.get_id_name_type(packaged_element)
            # get the activity diagram "uml:Activity"
            if xmi_type == uml_element.Types.ACTIVITY:
                # xmi_id:ActivityNode (class UmlActivityDiagramElement.ActivityNode)
                nodes_dict = {}
                # xmi_id:ActivityEdge (class uml_activity_diagram_element.ActivityEdge)
                edges_dict = {}
                # Result and Argument
                pins_dict = {}
                # create activity
                activity = uml_element.Activity(xmi_id, xmi_type, name,
                                                nodes_dict, edges_dict, pins_dict)
                # put it in the activitys_dict
                activitys_dict[xmi_id] = activity
                # activity_id
                activity_id = xmi_id
                # get all the nodes
                nodes = self.get_child_nodes(packaged_element, "node")
                # get every node
                for node in nodes:
                    # get the id, name, type of the node
                    xmi_id, name, xmi_type = self.get_id_name_type(node)
                    # get behavior
                    behavior = self.get_behavior(node)
                    # get incomings of the node
                    incomings = self.get_incomings(node)
                    # get outgoings of the node
                    outgoings = self.get_outgoings(node)
                    # get the results of the node
                    results = self.get_results(node, xmi_id)
                    # get the arguments of the node
                    arguments = self.get_arguments(node, xmi_id)
                    # create node object
                    self.create_node_object(nodes_dict, xmi_id, xmi_type, name, \
                                           incomings, outgoings, results, arguments, behavior)
                    # put all the results and arguments in the pins_dict
                    # if not all empty
                    if (results or arguments):
                        self.__set_pins_dict(pins_dict, results, arguments)
                # get all the edges
                edges = self.get_child_nodes(packaged_element, "edge")
                # get every node
                for edge in edges:
                    # get the id,name,type of the edge
                    xmi_id, name, xmi_type = self.get_id_name_type(edge)
                    # get the target, source of the edge
                    target, source = self.get_target_source(edge)
                    # get the guard of the edge
                    guard = self.get_guard(edge)
                    # create edge object
                    self.create_edge_object(edges_dict, xmi_id, xmi_type, name, \
                                           target, source, guard)
            # <packagedElement name="UserData" xmi:type="uml:InstanceSpecification" xmi:id="EAID_C3D4C"/>
            elif xmi_type == "uml:InstanceSpecification":
                InstanceSpecification_node = uml_element.InstanceSpecification_node(xmi_id, xmi_type, name, [], [])
                InstanceSpecification_nodes.append(InstanceSpecification_node)
        
        for InstanceSpecification_node in InstanceSpecification_nodes:
            model.activitys_dict[activity_id].nodes_dict[InstanceSpecification_node.xmi_id] = InstanceSpecification_node
        
        if exporter == "MagicDraw UML":
            # time parser
            data_times = self.get_child_nodes(root, "Data:Time")
            for data_time in data_times:
                str_time, base_element , time_type = self.get_time_base_element(data_time)
                self.set_time(str_time, base_element, time_type, model)

            # for from EA imported xml
            thecustomprofile_times = self.get_child_nodes(root, "thecustomprofile:time")
            for thecustomprofile_time in thecustomprofile_times:
                str_time, base_element, time_type = self.get_time_base_element(thecustomprofile_time)
                self.set_time(str_time, base_element, time_type, model)

        elif exporter == "Enterprise Architect":
            # get the tag "time" for EA
            extension = self.get_child_nodes(root, "xmi:Extension")[0]
            elements = self.get_child_nodes(extension, "elements")[0]
            element_tags = self.get_child_nodes(elements, "element")
            for element in element_tags:
                tags = self.get_child_nodes(element, "tags")
                if len(tags) > 0:
                    tags = tags[0]
                    tag_elements = self.get_child_nodes(tags, "tag")
                    for tag in tag_elements:
                        if tag.hasAttribute("name"):
                            name = tag.getAttribute("name")
                            if name == "time":
                                if tag.hasAttribute("value"):
                                    str_time = tag.getAttribute("value")
                                    base_element = element.getAttribute("xmi:idref")
                                    # TODO 
                                    self.set_time(str_time, base_element, "exp", model)
        else:
            log.show_error("the exporter is not supported in the code")

        return model
