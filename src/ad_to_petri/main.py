'''
Created on 14.09.2015

@author: Kai
@contact: cumtdingkai@gmail.com

Graphviz
python2.7
pip

pygraphviz  pip install pygraphviz
numpy pip install numpy
'''

from activity_diagram_to_ptnet import ActivityDiagramToPetriNet
import log
import examples
import time

start_time = time.clock()
# the path of the xml
xml_path = examples.get_xml_path()
# create the main object
act_to_pt = ActivityDiagramToPetriNet()
# load xml and parsing
act_to_pt.load_xml(xml_path)
# start activity_analyse
act_to_pt.activity_analyse()
# transform_to_pt to Petri net
act_to_pt.transform_to_pt()

act_to_pt.petri_net_analyse()
# draw PT net and reachability_graph_element
act_to_pt.create_diagram()

# control, getReachabilityGraph
act_to_pt.get_reachability_graph()
# start petri_net_reachability_analyse
act_to_pt.petri_net_reachability_analyse()
# show .reachability_graph details
act_to_pt.reachability_graph_analyse()
# draw PT net and reachability_graph_element
act_to_pt.create_diagram()

act_to_pt.show_summary(True)

end_time = time.clock()
log.show_info("completed in " + str(end_time - start_time) + "s")
