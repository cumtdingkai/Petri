'''
Created on 27.11.2015

@author: Kai
'''
from activity_diagram_to_ptnet import ActivityDiagramToPetriNet
import log
import examples
import time

start = time.clock()
# the path of the xml
xml_path = examples.get_xml_path()
# create the main object
act_to_pt = ActivityDiagramToPetriNet()
# load xml and parsing
act_to_pt.load_xml(xml_path)
# start activity_analyse
act_to_pt.activity_analyse()
# transform_to_pt to Petri net
act_to_pt.transform_to_epf()

end = time.clock()
log.show_info("completed in " + str(end - start) + "s")
