'''
Created on 12.09.2015

@author: Kai
'''

class Model(object):
    '''
    xmi_type = "uml:Model"
    '''
    def __init__(self, xmi_id, xmi_type, name, activitys_dict):
        '''
        @param activitys_dict: save all the activitys in the model.
        @type activitys_dict: dict
        '''
        self.xmi_id = xmi_id
        self.xmi_type = xmi_type
        self.name = name
        self.activitys_dict = activitys_dict

class Activity(object):
    '''An activity is the specification of a parameterized sequence of behavior.
    An activity is shown as a round-cornered rectangle enclosing all the actions,
    control flows and other elements that make up the activity.
    @attention: 1.In the called sub-activity diagram, the Initial Node indicates
    where control starts when the called behavior is invoked,
    The Activity Final Node shows where control should return to the parent activity.
    2.Set the Is Synchronous property of the action to indicate whether your activity
    waits for the called activity to complete.
    xmi_type = "uml:Activity"
    '''
    def __init__(self, xmi_id, xmi_type, name, nodes_dict, edges_dict, pins_dict):
        '''
        @param nodes_dict: activity_node_dict, save all the activity nodes in the activity.
        @type nodes_dict: dictionary
        @param edge_dict: activity_edge_dict, save all the activity edges in the activity.
        @type edge_dict: dictionary
        @param pins_dict: activity_pins_dict, save all the pin, pout in the activity
        @type pins_dict: dictionary
        '''
        self.xmi_id = xmi_id
        self.xmi_type = xmi_type
        self.name = name
        self.nodes_dict = nodes_dict
        self.edges_dict = edges_dict
        self.pins_dict = pins_dict


class ActivityEdge(object):
    ''' super class ActivityEdge of ControlFlow and ObjectFlow in UML Activity draw.
    <edge xmi:id="_18_4298" xmi:type="uml:ControlFlow" target="_4248" source="_4235">
    </edge>
    or with guard-
    <edge xmi:id="_18_4622" xmi:type="uml:ControlFlow" target="_4602" source="_4433">
        <guard xmi:id="_18_4629" xmi:type="uml:OpaqueExpression">
            <body>Invalid</body>
            <language>English</language>
        </guard>
    </edge>
    '''
    def __init__(self, xmi_id, xmi_type, name, target, source, guard):
        '''
        @param target: the id of a node or pin,pout
        @type target: string
        @param source: the id of a node or pin,pout
        @type source: string
        @param guard: guard of the edge
        @type guard: instance of Guard
        @attention: edge has just one target and one source
        '''
        self.xmi_id = xmi_id
        self.xmi_type = xmi_type
        self.name = name
        self.target = target
        self.source = source
        self.guard = guard
        # parallel edge after the fork, before the join
        self.parallel = False
        self.fork_num = 0
        self.parallel_num = 0
########################################################################################

class ControlFlow(ActivityEdge):
    '''it is an edge that starts an activity node after the previous one is finished.
    Objects and data cannot pass along the control flow edge.
    xmi_type = "uml:ControlFlow"
    '''
    def __init__(self, xmi_id, xmi_type, name, target, source, guard):
        ActivityEdge.__init__(self, xmi_id, xmi_type, name, target, source, guard)
        # the cf_prob in EPF
        self.prob = 1

class ObjectFlow(ActivityEdge):
    '''it is an activity edge that can have objects or data passing along it.
    An object flow must have an object on at least one of its ends.
    xmi_type = "uml:ObjectFlow"
    '''
    def __init__(self, xmi_id, xmi_type, name, target, source, guard):
        ActivityEdge.__init__(self, xmi_id, xmi_type, name, target, source, guard)

########################################################################################


class ActivityNode(object):
    '''super class ActivityNode in UML Activity draw
    <node xmi:id="_18_4355" xmi:type="uml:ForkNode" visibility="public">
        <incoming xmi:idref="_18_4370"/>
        <outgoing xmi:idref="_18_4502"/>
        <outgoing xmi:idref="_18_4507"/>
    </node>
    '''
    def __init__(self, xmi_id, xmi_type, name, incomings, outgoings):
        '''
        @param incomings: the incomings list of the node
        @type incomings: list, [instance1 of Incoming,instance2 of Incoming,...]
        @param outgoings: the outgoings list of the node
        @type outgoings: list, [instance1 of Outgoings,instance2 of Outgoings,...]
        '''
        self.xmi_id = xmi_id
        self.xmi_type = xmi_type
        self.name = name
        self.incomings = incomings
        self.outgoings = outgoings


########################################################################################

class ControlNode(ActivityNode):
    '''it is the super class of merge,decision,join,fork...
    the control node can be transformed to a place or a transition element in Petri-Net,
    also self.petri = True
    '''
    def __init__(self, xmi_id, xmi_type, name, incomings, outgoings):
        ActivityNode.__init__(self, xmi_id, xmi_type, name, incomings, outgoings)
        self.petri = True

class ExecutableNode(ActivityNode):
    '''it is the super class of action. It can be transformed to a transition element in Petri-Net.
    it has inputs(arguments) and outputs(results).
    the time is execute time. the time can be transformed to timed Petri-Net.
    '''
    def __init__(self, xmi_id, xmi_type, name, incomings, outgoings, results, arguments):
        '''
        @param results: Inputs Pin, [instance1 of Result,instance2 of Result...]
        @type results: list
        @param arguments: Outputs Pin, [instance1 of Argument,instance2 of Argument...]
        @type arguments: list
        @param time: execute time, unit "s", default 0s
        @type time: float
        '''
        ActivityNode.__init__(self, xmi_id, xmi_type, name, incomings, outgoings)
        self.petri = True
        self.place = False
        self.transition = True
        self.results = results
        self.arguments = arguments
        # action is default immediate, and time = 0
        self.immediate = True
        # action is deterministic
        self.deterministic = False
        # action is Exponential
        self.exponential = False
        # time --delay
        self.time = 0
        # if it is in a parallel process(fork,join)
        self.parallel = False
        self.parallel_num = -1
        self.initial = False

class ObjectNode(ActivityNode):
    '''The Activity nodes are introduced to provide a general class
    for the nodes connected by activity edges.
    it can be transformed to Place or Transition in Petri-Net
    @attention: object node has no pin,pout. the flow (passing it) is object flow
    xmi_type = "uml:CentralBufferNode"
    '''
    def __init__(self, xmi_id, xmi_type, name, incomings, outgoings):
        ActivityNode.__init__(self, xmi_id, xmi_type, name, incomings, outgoings)
        self.petri = False
        # if it is in a parallel process(fork,join)
        self.parallel = False
        self.parallel_num = -1

########################################################################################

class Action(ExecutableNode):
    '''An action is a named element that is the fundamental unit of an executable functionality. The
    execution of an action represents some transformations or processing in the modeled system.
    xmi_type ="uml:Action"
    xmi_type = "uml:CallBehaviorAction"
    <node name="Mail Order" xmi:id="_18_4274" xmi:type="uml:CallBehaviorAction" visibility="public">
        <incoming xmi:idref="_18_4308"/>
            <result name="Order" xmi:id="_18_4328" xmi:type="uml:OutputPin" visibility="public">
                <outgoing xmi:idref="_18_4326"/>
            </result>
    </node>
    '''
    def __init__(self, xmi_id, xmi_type, name, incomings, outgoings, results, arguments):
        '''
        '''
        ExecutableNode.__init__(self, xmi_id, xmi_type, name,
                                incomings, outgoings, results, arguments)
        self.behavior = None
    def add_behavior(self, behavior):
        '''
        @param behavior: it is the id of the subActivity
        @type behavior: string
        '''
        self.behavior = behavior

class InitialNode(ControlNode):
    '''An initial node is a starting point for executing an activity. It has no
    incoming edges.
    it has no incomings, just outgoings. incomings =[].
    it can be transformed to a Place in Petri-Net
    <node xmi:id="_18_4229" xmi:type="uml:InitialNode" visibility="public">
        <outgoing xmi:idref="_18_4386"/>
    </node>
    xmi_type = "uml:InitialNode"
    '''
    def __init__(self, xmi_id, xmi_type, name, incomings, outgoings):
        ControlNode.__init__(self, xmi_id, xmi_type, name, incomings, outgoings)
        self.place = True
        self.transition = False

class FinalNode(ControlNode):
    '''super class of Activity Final and Flow Final
    it can be transformed to a Place in Petri-Net
    it has no outgoings, just incomings. outgoings =[].
    '''
    def __init__(self, xmi_id, xmi_type, name, incomings, outgoings):
        ControlNode.__init__(self, xmi_id, xmi_type, name, incomings, outgoings)
        self.place = True
        self.transition = False

class ActivityFinal(FinalNode):
    '''An activity final node is a final node that stops all flows in an activity.
    it has no outgoings, just incomings. outgoings =[].
    xmi_type = "uml:ActivityFinalNode"
    <node xmi:id="_18_4581" xmi:type="uml:ActivityFinalNode" visibility="public">
        <incoming xmi:idref="_18_4599"/>
    </node>
    '''
    def __init__(self, xmi_id, xmi_type, name, incomings, outgoings):
        FinalNode.__init__(self, xmi_id, xmi_type, name, incomings, outgoings)

class FlowFinal(FinalNode):
    '''The Final node that terminates a flow and destroys all tokens that arrive at it.
    It has no impact on other flows in the activity.
    @attention: The difference between the two node types is that the flow final node
    denotes the end of a single control flow;
    the activity final node denotes the end of all control flows within the activity.
    it has no outgoings, just incomings. outgoings =[].
    xmi_type = "uml:FlowFinalNode"
    '''
    def __init__(self, xmi_id, xmi_type, name, incomings, outgoings):
        FinalNode.__init__(self, xmi_id, xmi_type, name, incomings, outgoings)
        # tokens
        # self.tokens =1

class Fork(ControlNode):
    '''Helps to control parallel actions.
    it can be transformed to a Transition in Petri-Net
    default:one incoming, more outgoing
    xmi_type = "uml:ForkNode"
    '''
    def __init__(self, xmi_id, xmi_type, name, incomings, outgoings, horizontal=True):
        ControlNode.__init__(self, xmi_id, xmi_type, name, incomings, outgoings)
        self.place = False
        self.transition = True
        # fork is immediate
        self.immediate = True
        self.horizontal = horizontal  # default is Horizontal-True
        # parallel process number
        self.parallel_num = -1


class Join(ControlNode):
    '''Helps to control parallel actions.
    it can be transformed to a Transition in Petri-Net
    default:more incoming, one outgoing
    xmi_type = "uml:JoinNode"
    @attention: Magic draw a Join can have just one outgoing, if you need two incomings,
    and two outgoings, please use a fork in magic draw.
    <node xmi:id="_18_4563" xmi:type="uml:JoinNode" visibility="public">
        <incoming xmi:idref="_18_4573"/>
        <incoming xmi:idref="_18_4578"/>
        <outgoing xmi:idref="_18_4599"/>
    </node>
    '''
    def __init__(self, xmi_id, xmi_type, name, incomings, outgoings, horizontal=True):
        ControlNode.__init__(self, xmi_id, xmi_type, name, incomings, outgoings)
        self.place = False
        self.transition = True
        # join is immediate
        self.immediate = True
        self.horizontal = horizontal  # default is Horizontal
        # parallel process number
        self.parallel_num = -1

class Decision(ControlNode):
    '''Decision is a control node that chooses between outgoing flows.
    A decision node has one incoming edge and multiple outgoing activity edges.
    it can be transformed to a Place in Petri-Net
    xmi_type = "uml:DecisionNode"
    '''
    def __init__(self, xmi_id, xmi_type, name, incomings, outgoings):
        ControlNode.__init__(self, xmi_id, xmi_type, name, incomings, outgoings)
        self.place = True
        self.transition = False
        # tokens
        # self.tokens =1

class Merge(ControlNode):
    '''A merge node is a control node that brings together multiple alternate flows.
    It is not used to synchronize concurrent flows but it is used to accept one among several
    alternate flows.
    it can be transformed to a Place in Petri-Net
    xmi_type = "uml:MergeNode"
    @attention: in Magic draw a merge can have just one outgoing, if you need two incomings,
    and two outgoings, please use a decision in magic draw.
    <node xmi:id="_18_4433" xmi:type="uml:MergeNode" visibility="public">
        <incoming xmi:idref="_18_4441"/>
        <incoming xmi:idref="_18_4456"/>
        <outgoing xmi:idref="_18_4622"/>
    </node>
    '''
    def __init__(self, xmi_id, xmi_type, name, incomings, outgoings):
        ControlNode.__init__(self, xmi_id, xmi_type, name, incomings, outgoings)
        self.place = True
        self.transition = False
        # max_tokens
        self.max_tokens = 1


########################################################################################

class SendSignalAction(ExecutableNode):
    '''it is an action that creates a signal instance from its inputs,
    and transmits it to the target object,where it may trigger
    the state machine transition or the execution of an activity.
    <target />
    <argument />
    @param arguments: Inputs Pin, [instance1 of Argument,instance2 of Argument...]
    @type arguments: list
    @attention: it has pin(target,argument), no pout(result).cf:acceptEventAction results=[]
    xmi_type = "uml:SendSignalAction"
    '''
    def __init__(self, xmi_id, xmi_type, name, incomings, outgoings, results, arguments):
        ExecutableNode.__init__(self, xmi_id, xmi_type, name,
                                incomings, outgoings, results, arguments)

class AcceptEventAction(ExecutableNode):
    '''it is an action that waits for the occurrence of
    an event that meets the specified conditions.
    The Accept event actions handle event occurrences detected by the object owning the behavior.
    @param results: Outputs Pin, [instance1 of Result,instance2 of Result...]
    @type results: list
    @attention: it has pout(result), no pin(argument).cf:sendSignalAction  arguments=[]
    xmi_type = "uml:AcceptEventAction"
    '''
    def __init__(self, xmi_id, xmi_type, name, incomings, outgoings, results, arguments):
        ExecutableNode.__init__(self, xmi_id, xmi_type, name,
                                incomings, outgoings, results, arguments)

# "uml:DataStoreNode"
class DataStore(ObjectNode):
    '''A data store is shown as an object with the  data store  keyword.
    '''
    def __init__(self, xmi_id, xmi_type, name, incomings, outgoings):
        ObjectNode.__init__(self, xmi_id, xmi_type, name, incomings, outgoings)

class InstanceSpecification_node(ObjectNode):
    '''InstanceSpecification_node
    '''
    def __init__(self, xmi_id, xmi_type, name, incomings, outgoings):
        ObjectNode.__init__(self, xmi_id, xmi_type, name, incomings, outgoings)

class ActivityParameterNode(ObjectNode):
    '''It is an object node for inputs and outputs to the activities.
    The Activity parameters are object nodes at the beginning and end of the flows,
    to accept inputs to an activity and provide outputs from it.
    "uml:ActivityParameterNode"
    @attention: pass
    '''
    def __init__(self, xmi_id, xmi_type, name, incomings, outgoings, parameter=None):
        ObjectNode.__init__(self, xmi_id, xmi_type, name, incomings, outgoings)
        self.parameter = parameter
        # self.place = True

########################################################################################

# "uml:OpaqueExpression"
class Guard(object):
    '''
    <guard xmi:id="_18_4629" xmi:type="uml:OpaqueExpression">
        <body>Invalid</body>
        <language>English</language>
    </guard>
    '''
    def __init__(self, xmi_id, xmi_type, name, body, language):
        self.xmi_id = xmi_id
        self.xmi_type = xmi_type
        self.name = name
        self.body = body
        self.language = language

class Result(object):
    ''' result is OutputPin, it has just outgoing Tag.
    <result name="Order" xmi:id="_18_4328" xmi:type="uml:OutputPin" visibility="public">
            <outgoing xmi:idref="_18_4326"/>
    </result>
    '''
    # "uml:OutputPin"
    def __init__(self, xmi_id, xmi_type, name, outgoings, host):
        '''
        @param outgoings: the outgoings list of the Result
        @type outgoings: list, [instance1 of Outgoings,instance2 of Outgoings,...]
        @param host: the id of the node, which node has the Result(pout)
        @type host: string
        '''
        self.xmi_id = xmi_id
        self.xmi_type = xmi_type
        self.name = name
        self.outgoings = outgoings
        self.host = host

class Argument(object):
    ''' argument is InputPin, it has just incoming Tag.
    <argument name="Order" xmi:id="_18_4339" xmi:type="uml:InputPin" visibility="public">
        <incoming xmi:idref="_18_4326"/>
    </argument>
    '''
    # "uml:InputPin"
    def __init__(self, xmi_id, xmi_type, name, incomings, host):
        '''
        @param incomings: the ingoings list of the Result
        @type incomings: list, [instance1 of Incoming,instance2 of Incoming,...]
        @param host: the id of the node, which node has the Argument(pin)
        @type host: string
        '''
        self.xmi_id = xmi_id
        self.xmi_type = xmi_type
        self.name = name
        self.incomings = incomings
        self.host = host

class Incoming(object):
    ''' the incoming of one node, one result or one argument.
    <incoming xmi:idref="_18_4303"/>
    '''
    def __init__(self, xmi_idref):
        '''
        @param xmi_idref: it is a id of the instance of ActivityEdge
        @type xmi_idref: str
        '''
        self.xmi_idref = xmi_idref

class Outgoing(object):
    ''' the outgoing of one node, one result or one argument
    '''
    def __init__(self, xmi_idref):
        '''
        @param xmi_idref: the id of the edge
        @type xmi_idref: str
        '''
        self.xmi_idref = xmi_idref

class Types(object):
    '''Class giving the ActivityNodeType constants."""
    '''
    CONTROL_FLOW = "uml:ControlFlow"
    OBJECT_FLOW = "uml:ObjectFlow"
    ACTION = "uml:Action"
    CALLBEHAVIOR_ACTION = "uml:CallBehaviorAction"
    INITIAL_NODE = "uml:InitialNode"
    ACTIVITY_FINAL_NODE = "uml:ActivityFinalNode"
    FLOW_FINAL_NODE = "uml:FlowFinalNode"
    FORK_NODE = "uml:ForkNode"
    JOIN_NODE = "uml:JoinNode"
    DECISION_NODE = "uml:DecisionNode"
    MERGE_NODE = "uml:MergeNode"
    SEND_SIGNAL_ACTION = "uml:SendSignalAction"
    ACCEPT_EVENT_ACTION = "uml:AcceptEventAction"
    OBJECT_NODE = "uml:CentralBufferNode"
    DATA_STORE_NODE = "uml:DataStoreNode"
    ACTIVITY = "uml:Activity"

########################################################################################

class Partition(object):
    ''' partition (swim lanes) in activity diagram.
    <group name="Passenger" xmi:id="_18_4477" xmi:type="uml:ActivityPartition" visibility="public">
        <edge xmi:idref="_18_4616"/>
        <edge xmi:idref="_18_4671"/>
        <node xmi:idref="_18_4423"/>
        <node xmi:idref="_18_4575"/>
        <node xmi:idref="_18_4417"/>
    </group>

    <node xmi:id="_18_4417" xmi:type="uml:InitialNode" visibility="public">
        <inPartition xmi:idref="_18_4477"/>
        <outgoing xmi:idref="_18_4616"/>
    </node>

    <partition xmi:idref="_18_4477"/>
    <partition xmi:idref="_18_4480"/>
    '''
    def __init__(self, xmi_id, xmi_type, name):
        '''
        '''
        self.xmi_id = xmi_id
        self.xmi_type = xmi_type
        self.name = name
