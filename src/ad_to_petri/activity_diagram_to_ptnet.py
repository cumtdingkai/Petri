'''
Created on 03.10.2015

@author: Kai
'''


from xml_dom_parser import XmlParser
from activity_diagram_analyse import ActivityDiagramAnalyser
from petri_net_analyse import PetriNetAnalyser
from petri_net_reachability_analyse import PetriNetReachabilityAnalyser
from reachability_graph_analyse import RgAnalyser
from get_reachability_graph import PetriToReachabilityGraph
from activity_transform_pt import TransformerToPt
from activity_transform_epf import AdToEpfTransformer
from draw import DrawTool
import log
from epf import epf_model


class ActivityDiagramToPetriNet(object):
    '''ActivityDiagramToPetriNet
    '''
    def __init__(self):
        self.model = None
        self.petri_nets = []
        self.rg_graphs = []

    def load_xml(self, xml_path):
        '''load the xml
        '''
        xml_parser = XmlParser()
        self.model = xml_parser.xml_parse(xml_path)

    def activity_analyse(self):
        '''start analyze
        '''
        activity_analyser = ActivityDiagramAnalyser()
        activitys_dict = self.model.activitys_dict
        num = len(activitys_dict)
        log.show_info("the model has %d activities" % num)
        for activity in  activitys_dict.values():
            activity_analyser.show_activity_details(activity, show=False)
            activity_analyser.get_init_final_num(activity)
            activity_analyser.check_names(activity)
            activity_analyser.analyze_object_flow(activity)
            activity_analyser.action_has_more_incomings(activity)
            activity_analyser.action_has_more_outgoings(activity)
            activity_analyser.get_parallel_edges(activity)
            activity_analyser.fork_has_more_incomings(activity)
            activity_analyser.check_probability(activity)
            activity_analyser.get_parallel_process(activity)
            activity_analyser.show_activity_details(activity, show=False)

    def transform_to_pt(self):
        '''activity diagram to petri net
        '''
        activitys_dict = self.model.activitys_dict
        transformer = TransformerToPt()
        for activity in  activitys_dict.values():
            petri_net = transformer.transform_to_petri_net(activity)
            self.petri_nets.append(petri_net)

    def transform_to_epf(self):
        '''activity diagram to error model
        '''
        activitys_dict = self.model.activitys_dict
        transformer = AdToEpfTransformer()
        for activity in  activitys_dict.values():
            # create a model
            model = epf_model.Model()
            transformer.transform_to_epf(activity, model)
            
    def petri_net_analyse(self):
        '''start petri net analyzes
        '''
        petri_net_analyser = PetriNetAnalyser()
        for petri_net in self.petri_nets:
            petri_net_analyser.find_self_loop(petri_net)
            petri_net_analyser.set_place_tokens(petri_net)

    def get_reachability_graph(self):
        '''get reachability graph of the petri net
        '''
        pt_to_rg = PetriToReachabilityGraph()
        for petri_net in self.petri_nets:
            rg_graph = pt_to_rg.get_reachability_graph(petri_net)
            self.rg_graphs.append(rg_graph)

    def petri_net_reachability_analyse(self):
        '''start petri net reachability analyze
        '''
        petri_net_reachability_analyser = PetriNetReachabilityAnalyser()
        for petri_net in self.petri_nets:
            petri_net_reachability_analyser.show_pt_net_details(petri_net, show=False)
            petri_net_reachability_analyser.find_deadlock(petri_net)
            petri_net_reachability_analyser.get_petri_type(petri_net)
            petri_net_reachability_analyser.get_matrix(petri_net)

    def reachability_graph_analyse(self):
        '''start reachability graph analyze
        '''
        rg_analyser = RgAnalyser()
        for rg_graph in self.rg_graphs:
            rg_analyser.show_rg_details(rg_graph, show=False)

    def create_diagram(self):
        '''create and draw the petri net and Reachability Graph.
        '''
        draw_tool = DrawTool()
        for petri_net in self.petri_nets:
            draw_tool.draw_petri_net(petri_net)
        for rg_graph in self.rg_graphs:
            draw_tool.draw_reachability_graph(rg_graph)

    def show_summary(self, show):
        '''show the summary
        '''
        if show:
            num_petri_net = len(self.petri_nets)
            for index in range(num_petri_net):
                petri_net = self.petri_nets[index]
                rg_graph = self.rg_graphs[index]

                num_places = len(petri_net.places_dict)
                num_transitions = len(petri_net.transitions_dict)
                num_arcs = len(petri_net.arcs_dict)

                num_states = len(rg_graph.states_dict)
                num_edges = len(rg_graph.edges_dict)

                log.show_summary("the petri net:" + petri_net.name + " has "\
                                  + str(num_places) + " places," + str(num_transitions)\
                                  + " transitions," + str(num_arcs) + " arcs.")
                log.show_summary("the rg graph:" + rg_graph.name + " has "\
                                 + str(num_states) + " states," + str(num_edges) + " edges.")
