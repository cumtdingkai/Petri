'''all the petri_net elements
'''
class PetriNet(object):
    '''the class of Petri Net
    '''
    def __init__(self, places_dict, transitions_dict, arcs_dict, name):
        '''
        @type places_dict: dict
        @type transitions_dict: dict
        @type arcs_dict: dict
        '''
        self.places_dict = places_dict
        self.transitions_dict = transitions_dict
        self.arcs_dict = arcs_dict
        self.name = name
        self.matrix = None
        self.label = "label : \l"
        self.probs ="probs : \l"

class PetriNode(object):
    '''the super class of Place and Transition
    '''
    def __init__(self, pt_id, name, incomings, outgoings):
        self.pt_id = pt_id
        self.name = name
        self.incomings = incomings
        self.outgoings = outgoings
        self.xlabel = ""
        self.id_changed = False

class Place(PetriNode):
    '''It is Place in Petri Net.
    default: a place with one token. also selsf.max_tokens =1
    incomings and outgoings are list
    '''
    def __init__(self, pt_id, name, incomings, outgoings):
        PetriNode.__init__(self, pt_id, name, incomings, outgoings)
        self.start = False
        self.final = False
        # max_tokens
        self.max_tokens = 1
        self.tokens = 0

class Transition(PetriNode):
    '''
    incomings and outgoings are list
    enabled
    '''
    def __init__(self, pt_id, name, incomings, outgoings):
        PetriNode.__init__(self, pt_id, name, incomings, outgoings)

class ExponentialTransition(Transition):
    '''Exponential transitions are drawn as empty rectangles.
    Their firing Delay is exponentially distributed. Its default value
    (i.e., the expectation of the exponentially distributed firing time) is 1.
    @see: www.tu-ilmenau.de/sse/timenet/general-information/petri-nets/
    @see: http://www2.tu-ilmenau.de/sse_file/timenet/ManualHTML3/node16.html
    '''
    def __init__(self, pt_id, name, incomings, outgoings):
        Transition.__init__(self, pt_id, name, incomings, outgoings)
        # type
        self.transition_type = TransitionTypes.EXPONENTIAL_TRANSITION
        # delay = property time
        self.delay = 1

class ImmediateTransition(Transition):
    '''Immediate transitions are drawn as thin bars.
    The weight is a real value (default: 1), specifying the relative firing probability
    of the transition with respect to other simultaneously enabled immediate transitions
    that are in conflict.
    The priority is a natural number (default: 1), that defines a precedence among
    simultaneously enabled immediate transition firings.
    The default priority is 1, higher numbers mean higher priority.
    The enabling function (also called guard) is a marking-dependent expression1,
    which must be true in order to allow the transition to be enabled.
    Its default empty state means that the transition is allowed to fire.
    @see: www.tu-ilmenau.de/sse/timenet/general-information/petri-nets/
    '''
    def __init__(self, pt_id, name, incomings, outgoings):
        Transition.__init__(self, pt_id, name, incomings, outgoings)
        # type
        self.transition_type = TransitionTypes.IMMEDIATE_TRANSITION

        # dalay = 0
        self.delay = 0
        # weight, priority
        self.weight = 1
        self.priority = 1

class DeterministicTransition(Transition):
    '''Deterministic transitions are drawn as black filled rectangles.
    The fixed firing delay of this transition type is initially 1.
    @see: www.tu-ilmenau.de/sse/timenet/general-information/petri-nets/
    '''
    def __init__(self, pt_id, name, incomings, outgoings):
        Transition.__init__(self, pt_id, name, incomings, outgoings)
        # type
        self.transition_type = TransitionTypes.DETERMINISTIC_TRANSITION
        # delay  = property time
        self.delay = 0

class Arc(object):
    '''
    arc has one source, one target
    source and target are P or T
    '''
    def __init__(self, pt_id, name, source, target):
        self.pt_id = pt_id
        self.name = name
        self.source = source
        self.target = target
        self.label = ""
        self.prob = 1

class TransitionTypes(object):
    '''the 3 types of a transition
    '''
    EXPONENTIAL_TRANSITION = "Exponential_transition"
    IMMEDIATE_TRANSITION = "Immediate_transition"
    DETERMINISTIC_TRANSITION = "Deterministic_transition"

class PetriNetTypes(object):
    '''the types of a petri net
    '''
    STATE_MACHINES = "State Machines"
    MARKED_GRAPHS = "Marked Graphs"
    FREE_CHOICE = "Free Choice"
    NOT_FREE_CHOICE = "Not Free Choice"
