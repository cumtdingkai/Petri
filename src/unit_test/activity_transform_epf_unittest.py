'''
Created on 02.12.2015

@author: Kai
'''

import unittest
from ad_to_petri import activity_transform_epf
from bean import uml_activity_diagram_element as uml_element

class Mytest(unittest.TestCase):
    '''test class
    '''
    # initial
    def setUp(self):
        '''setup
        '''
        # new the to unit test class object
        self.tclass = activity_transform_epf.AdToEpfTransformer()

        # init->edge1->action1->edge2->action2->edge4->final
        # action2->edge3->action1
        # action1->edge5->object1->edge6->action2

        initial = uml_element.InitialNode("initial", uml_element.Types.INITIAL_NODE, \
                                          "initial", [], [uml_element.Outgoing("edge1")])
        edge1 = uml_element.ControlFlow("edge1", uml_element.Types.CONTROL_FLOW, \
                                        "edge1", "action1", "initial", None)
        action1 = uml_element.Action("action1", uml_element.Types.ACTION, "action1", [uml_element.Incoming("edge1"), uml_element.Incoming("edge3")], [uml_element.Outgoing("edge2"), uml_element.Outgoing("edge5")], None, None)
        edge2 = uml_element.ControlFlow("edge2", uml_element.Types.CONTROL_FLOW, "edge2", "action2", "action1", None)
        action2 = uml_element.Action("action2", uml_element.Types.ACTION, "action2", [uml_element.Incoming("edge2"), uml_element.Incoming("edge6")], [uml_element.Outgoing("edge3"), uml_element.Outgoing("edge4")], None, None)
        edge4 = uml_element.ControlFlow("edge4", uml_element.Types.CONTROL_FLOW, "edge4", "final", "action2", None)
        final = uml_element.ActivityFinal("final", uml_element.Types.ACTIVITY_FINAL_NODE, "final", [uml_element.Incoming("edge4")], [])

        edge3 = uml_element.ControlFlow("edge3", uml_element.Types.CONTROL_FLOW, "edge3", "action1", "action2", None)
        edge5 = uml_element.ControlFlow("edge5", uml_element.Types.OBJECT_FLOW, "edge5", "object1", "action1", None)
        edge6 = uml_element.ControlFlow("edge6", uml_element.Types.OBJECT_FLOW, "edge6", "action2", "object1", None)
        object1 = uml_element.ObjectNode("object1", uml_element.Types.OBJECT_NODE, "object1", [uml_element.Incoming("edge5")], [uml_element.Outgoing("edge6")])
        
        activity = uml_element.Activity(0, uml_element.Types.ACTIVITY, 0, {}, {}, {})

        activity.edges_dict["edge1"] = edge1
        activity.edges_dict["edge2"] = edge2
        activity.edges_dict["edge3"] = edge3
        activity.edges_dict["edge4"] = edge4
        activity.edges_dict["edge5"] = edge5
        activity.edges_dict["edge6"] = edge6

        activity.nodes_dict["initial"] = initial
        activity.nodes_dict["action1"] = action1
        activity.nodes_dict["action2"] = action2
        activity.nodes_dict["object1"] = object1
        activity.nodes_dict["final"] = final
        self.activity = activity

    # tear down
    def tearDown(self):
        '''tear down
        '''
        self.tclass = None
        self.activity = None
    
    def test_get_elements_datas(self):
        '''_get_elements_datas()
        '''
        activity = self.activity
        elements, datas = self.tclass._get_elements_datas([], [], activity)
        # action1, action2, init, final
        self.assertEqual(len(elements), 4, "_get_elements_datas() assertEqual1 failed")
        # object1
        self.assertEqual(len(datas), 1, "_get_elements_datas() assertEqual2 failed")
    
    def test_get_data_flow(self):
        '''_get_data_flow()
        '''
        activity = self.activity
        data_flows = self.tclass._get_data_flow(["object1"], ["initial","action1","action2","final"], activity)
        print data_flows
        self.assertEqual(len(data_flows), 2, "_get_data_flow() assertEqual failed")
        self.assertTrue(("action1","object1") in data_flows,  "_get_data_flow() assertTrue1 failed")
        self.assertTrue(("object1","action2") in data_flows,  "_get_data_flow() assertTrue2 failed")
        
    def test_get_control_flows(self):
        '''_get_control_flows()
        '''
        activity = self.activity
        control_flows = self.tclass._get_data_flow(["object1"], ["initial","action1","action2","final"], activity)
        