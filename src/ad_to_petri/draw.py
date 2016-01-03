'''
Created on 13.09.2015

@author: Kai
'''
import pygraphviz as pgv
import time
import log
from bean import petri_net_element


class DrawTool(object):
    '''draw tool
    '''
    def get_num_str(self, num):
        '''get the num_str from the num
        1 -> 01
        12 -> 12
        @param num: it is a int num>=0
        @type num: int
        @return: return a 2-stelle num_str, for example 5->"05",11->"11"
        @rtype: str
        '''
        if num < 10:
            num_str = "0" + str(num)
        else:
            num_str = str(num)
        return num_str

    def get_png_name(self):
        '''get the png_name from the current exact time in format --"MMDDHHMMSS"
        @return: png_name in format --"MMDDHHMMSS"
        @rtype: string
        '''
        # get the num of the time
        # year = str(time.localtime()[0])
        mon = time.localtime()[1]
        day = time.localtime()[2]
        hour = time.localtime()[3]
        minut = time.localtime()[4]
        sec = time.localtime()[5]
        # get the numStr of the time
        monstr = self.get_num_str(mon)
        daystr = self.get_num_str(day)
        hourstr = self.get_num_str(hour)
        minutstr = self.get_num_str(minut)
        secstr = self.get_num_str(sec)
        # get the png_name from the current exact time "MMDDHHMMSS"
        png_name = monstr + daystr + hourstr + minutstr + secstr
        return png_name

    def draw_petri_net(self, petri_net):
        '''draw Petri Net from the 3 dicts
        '''
        places_dict = petri_net.places_dict
        transitions_dict = petri_net.transitions_dict
        arcs_dict = petri_net.arcs_dict
        # G=pgv.AGraph(directed=True,strict=True,splines="polyline")
        # G = pgv.AGraph(directed=True, strict=True, splines=False)
        G = pgv.AGraph(directed=True, strict=True)
        G.graph_attr['label'] = petri_net.label + petri_net.probs

        for pt_id in places_dict:
            place = places_dict[pt_id]
            place_xlabel = place.xlabel
            G.add_node(pt_id, shape="circle", label="", xlabel=place_xlabel)
        for pt_id in transitions_dict:
            transition = transitions_dict[pt_id]
            # get the max number of the incomings and outgoings
            number = max(len(transition.incomings), len(transition.outgoings))
            transition_width = 0.5 * number
            transition_xlabel = transition.xlabel

            transition_type = transition.transition_type
            # Deterministic transitions are drawn as black filled rectangles.
            if transition_type == petri_net_element.TransitionTypes.DETERMINISTIC_TRANSITION:
                G.add_node(pt_id, shape="box", style="filled", label="", \
                            xlabel=transition_xlabel, height=0.3, \
                            width=transition_width, fillcolor="#000000")  # color:black
            # Exponential transitions are drawn as empty rectangles.
            elif transition_type == petri_net_element.TransitionTypes.EXPONENTIAL_TRANSITION:
                G.add_node(pt_id, shape="box", label="",
                           xlabel=transition_xlabel, height=0.3,
                           width=transition_width, fillcolor="#000000")  # color:black
            # Immediate transitions are drawn as thin bars.
            elif transition_type == petri_net_element.TransitionTypes.IMMEDIATE_TRANSITION:
                G.add_node(pt_id, shape="box", style="filled", label="",
                           xlabel=transition_xlabel, height=0.08,
                           width=transition_width, fillcolor="#000000")  # color:black
            else:
                log.show_error("the transition type is not defined")
        for pt_id in arcs_dict:
            arc = arcs_dict[pt_id]
            source = arc.source
            target = arc.target
            G.add_edge(source, target)
            # draw the arc with probability
            # if arc.prob == 1:
            #    G.add_edge(source, target)
            # else:
            #    G.add_edge(source, target, label=arc.prob)

        # print G.string()  # print dot file to standard output
        png_name = self.get_png_name()
        # G.write("Pt"+png_name + ".dot")
        G.layout('dot')  # layout with dot
        G.draw("Pt" + "_" + petri_net.name + png_name + ".png")  # write to file
        log.show_info("the Petri Net Diagram is created.name:%s" % petri_net.name)

    def draw_reachability_graph(self, rg_graph):
        '''draw the reachability graph
        '''
        states_dict = rg_graph.states_dict
        edges_dict = rg_graph.edges_dict

        G = pgv.AGraph(directed=True, strict=False)

        for state_id in states_dict:
            state = states_dict[state_id]
            if state.reachability:
                G.add_node(state_id, shape="circle")
            else:
                G.add_node(state_id, shape="circle", color='blue')
        for edge_id in edges_dict:
            edge = edges_dict[edge_id]
            source = edge.source
            target = edge.target
            edge_label = edge.label
            if edge.reachability:
                G.add_edge(source, target, label=edge_label)
            else:
                G.add_edge(source, target, label=edge_label, color='blue')
        # print G.string()  # print dot file to standard output
        png_name = self.get_png_name()
        # G.write("Rg"+png_name + ".dot")
        G.layout('dot')  # layout with dot
        G.draw("Rg" + "_" + rg_graph.name + png_name + ".png")  # write to file
        # G.draw("Rg" + png_name + ".bmp")  # write to file
        log.show_info("the Reachability Diagram is created." + " name:" + rg_graph.name)
