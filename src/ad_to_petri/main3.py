'''
Created on 21.12.2015

@author: Kai
'''
from epf import epf_model
from ad_to_petri import draw
from ad_to_petri import get_reachability_graph

model = epf_model.Model()

# xml_path = "C:/Users/Kai/Desktop/ErrorPro3.4/epf/examples/abc.xml"
xml_path = "C:/Users/Kai/Desktop/test_exp_epf.xml"
model.xml.load(xml_path)

parallels = model.cf_parallel.get_parallel_process()    
index = 0 
draw_tool = draw.DrawTool()
rg_tool = get_reachability_graph.PetriToReachabilityGraph()
for parallel in parallels:
    index += 1
    petri_net = model.cf_parallel.get_petri_net(parallel, "parallel" + str(index))
    rg =rg_tool.get_reachability_graph(petri_net)
    draw_tool.draw_petri_net(petri_net)
    draw_tool.draw_reachability_graph(rg)