'''
Method     Checks that     New in
assertEqual('foo'.upper(), 'FOO')
assertTrue('FOO'.isupper())
assertFalse('Foo'.isupper())
assertEqual(s.split(), ['hello', 'world'])

assertAlmostEqual(a, b)     round(a-b, 7) == 0
assertNotAlmostEqual(a, b)     round(a-b, 7) != 0
assertGreater(a, b)     a > b     2.7
assertGreaterEqual(a, b)     a >= b     2.7
assertLess(a, b)     a < b     2.7
assertLessEqual(a, b)     a <= b     2.7
assertRegexpMatches(s, re)     regex.search(s)     2.7
assertNotRegexpMatches(s, re)     not regex.search(s)     2.7
assertItemsEqual(a, b)     sorted(a) == sorted(b) and works with unhashable objs     2.7
assertDictContainsSubset(a, b)     all the key/value pairs in a exist in b     2.7
assertMultiLineEqual(a, b)     strings     2.7
assertSequenceEqual(a, b)     sequences     2.7
assertListEqual(a, b)     lists     2.7
assertTupleEqual(a, b)     tuples     2.7
assertSetEqual(a, b)     sets or frozensets     2.7
assertDictEqual(a, b)     dicts     2.7
assertMultiLineEqual(a, b)     strings     2.7
assertSequenceEqual(a, b)     sequences     2.7
assertListEqual(a, b)     lists     2.7
assertTupleEqual(a, b)     tuples     2.7
assertSetEqual(a, b)     sets or frozensets     2.7
assertDictEqual(a, b)     dicts     2.7
'''

import unittest
from ad_to_petri import activity_diagram_analyse
from bean import uml_activity_diagram_element as uml_element

class Mytest(unittest.TestCase):
    '''test class
    '''
    # initial
    def setUp(self):
        '''setup
        '''
        # new the to unit test class object
        self.tclass = activity_diagram_analyse.ActivityDiagramAnalyser()

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

        # just test with final2
        final2 = uml_element.ActivityFinal("final2", uml_element.Types.ACTIVITY_FINAL_NODE, "4", ["in1"], [])
        
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
        activity.nodes_dict["final2"] = final2
        self.activity = activity

    # tear down
    def tearDown(self):
        '''tear down
        '''
        self.tclass = None
        self.activity = None

    def test_has_outgoing_control_flow(self):
        '''_has_outgoing_control_flow()
        '''
        activity = self.activity
        nodes_dict = activity.nodes_dict
        action1 = nodes_dict["action1"]
        ret1 = self.tclass._has_outgoing_control_flow(action1, activity)
        self.assertTrue(ret1, "_has_outgoing_control_flow() failed")
    
    def test_get_object_next_node(self):
        '''_get_object_next_node()
        '''
        activity = self.activity
        nodes_dict = activity.nodes_dict
        object1 = nodes_dict["object1"]
        ret_action = self.tclass._get_object_next_node(object1, activity)
        xmi_id = ret_action.xmi_id
        self.assertTrue(xmi_id=="action2", "_get_object_next_node() failed")

    def test_get_nodes_from_edge(self):
        '''_get_nodes_from_edge()
        '''
        activity = self.activity
        edges_dict = activity.edges_dict
        edge2 = edges_dict["edge2"]
        node1,node2 = self.tclass._get_nodes_from_edge(edge2, activity)
        xmi_id1 = node1.xmi_id
        xmi_id2 = node2.xmi_id
        self.assertTrue(xmi_id1=="action1", "_get_nodes_from_edge() assertTrue1 failed")
        self.assertTrue(xmi_id2=="action2", "_get_nodes_from_edge() assertTrue2 failed")

    # all the name with test...
    def test_get_init_final_num(self):
        '''get_init_final_num()
        '''
        activity = self.activity
        self.assertEqual(self.tclass.get_init_final_num(activity), (1, 2), "get_init_final_num() failed")

    def test_check_names(self):
        '''check_names()
        '''
        activity = self.activity
        ret1 = self.tclass.check_names(activity)
        self.assertTrue(ret1, "check_names() assertTrue1 failed")

        nodes_dict = activity.nodes_dict
        action2 =nodes_dict["action2"]
        action2.name ="action1"
        #ret2 = self.tclass.check_names(activity)
        #self.assertFalse(ret2, "check_names() assertTrue2 failed")

    def test_get_new_id(self):
        '''_get_new_id()
        '''
        edge_dict1 = {"edge_id1":1, "edge_id2":2}
        self.assertEqual(self.tclass._get_new_id("edge", edge_dict1), "edge_id3", "_get_new_id() failed")

        edge_dict2 = {"id1":1, "id2":2}
        self.assertEqual(self.tclass._get_new_id("edge", edge_dict2), "edge_id1", "_get_new_id() assertEqual1 failed")

        self.assertEqual(self.tclass._get_new_id("edge", self.activity.edges_dict), "edge_id1", "_get_new_id() assertEqual2 failed")

    def test_action_has_more_incomings(self):
        '''action_has_more_incomings()
        '''
        activity = self.activity
        self.assertEqual(self.tclass.action_has_more_incomings(activity), ["action1"], "action_has_more_incomings() failed")

    def test_action_has_more_outgoings(self):
        '''action_has_more_outgoings()
        '''
        activity = self.activity
        self.assertEqual(self.tclass.action_has_more_outgoings(activity), ["action2"], "action_has_more_outgoings() failed")

    def test_fork_has_more_incomings(self):
        '''fork_has_more_incomings()
        '''
        activity = self.activity
        self.assertEqual(self.tclass.fork_has_more_incomings(activity), [], "fork_has_more_incomings() assertEqual1 failed")
        # action1->edge1->fork
        # action2->edge2->fork

        action1 = uml_element.Action("action1", uml_element.Types.ACTION, "action1", ["1"], [uml_element.Outgoing("edge1")], None, None)
        edge1 = uml_element.ControlFlow("edge1", uml_element.Types.CONTROL_FLOW, "fork", "action1", "initial", None)

        action2 = uml_element.Action("action2", uml_element.Types.ACTION, "action2", ["2"], [uml_element.Outgoing("edge2")], None, None)
        edge2 = uml_element.ControlFlow("edge2", uml_element.Types.CONTROL_FLOW, "fork", "action2", "action1", None)

        fork = uml_element.FinalNode("fork", uml_element.Types.FORK_NODE, "fork", [uml_element.Incoming("edge1"), uml_element.Incoming("edge2")], ["3"])

        activity1 = uml_element.Activity(0, uml_element.Types.ACTIVITY, 0, {}, {}, {})

        activity1.edges_dict["edge1"] = edge1
        activity1.edges_dict["edge2"] = edge2
        activity1.nodes_dict["action1"] = action1
        activity1.nodes_dict["action2"] = action2
        activity1.nodes_dict["fork"] = fork
        self.assertEqual(self.tclass.fork_has_more_incomings(activity1), ["fork"], "fork_has_more_incomings() assertEqual2 failed")

    def test_create_merge(self):
        '''_create_merge()
        '''
        activity = self.activity
        nodes_dict = activity.nodes_dict
        edges_dict = activity.edges_dict

        num1 = len(nodes_dict)
        num2 = len(edges_dict)

        self.tclass._create_merge("action1", activity, uml_element.Types.CONTROL_FLOW)
        num3 = len(nodes_dict)
        num4 = len(edges_dict)

        edge1 = edges_dict["edge1"]
        edge3 = edges_dict["edge3"]
        action1 = nodes_dict["action1"]
        merge = nodes_dict["merge_id1"]
        edge = edges_dict["edge_id1"]

        self.assertEqual(num1 + 1, num3, "_create_merge() assertEqual1 failed")
        self.assertEqual(num2 + 1, num4, "_create_merge() assertEqual2 failed")

        self.assertEqual(edge1.target, "merge_id1", "_create_merge() assertEqual3 failed")
        self.assertEqual(edge3.target, "merge_id1", "_create_merge() assertEqual4 failed")
        self.assertEqual(edge.source, "merge_id1", "_create_merge() assertEqual5 failed")
        self.assertEqual(edge.target, "action1", "_create_merge() assertEqual6 failed")

        self.assertEqual(len(action1.incomings), 1, "_create_merge() assertEqual7 failed")
        self.assertEqual(action1.incomings[0].xmi_idref, "edge_id1", "_create_merge() assertEqual8 failed")
        self.assertEqual(len(merge.outgoings), 1, "_create_merge() assertEqual9 failed")
        self.assertEqual(merge.outgoings[0].xmi_idref, "edge_id1", "_create_merge() assertEqual10 failed")
        self.assertEqual(len(merge.incomings), 2, "_create_merge() assertEqual11 failed")

        self.assertTrue("merge_id1" in nodes_dict, "_create_merge() assertTrue failed")
        self.assertTrue("edge_id1" in edges_dict, "_create_merge() assertTrue failed")

    def test_create_decision(self):
        '''_create_decision()
        '''
        activity = self.activity
        nodes_dict = activity.nodes_dict
        edges_dict = activity.edges_dict

        num1 = len(nodes_dict)
        num2 = len(edges_dict)

        self.tclass._create_decision("action2", activity)
        num3 = len(nodes_dict)
        num4 = len(edges_dict)

        edge4 = edges_dict["edge4"]
        edge3 = edges_dict["edge3"]
        final = nodes_dict["final"]
        action2 = nodes_dict["action2"]
        decision = nodes_dict["decision_id1"]
        edge = edges_dict["edge_id1"]

        self.assertEqual(num1 + 1, num3, "_create_decision() assertEqual1 failed")
        self.assertEqual(num2 + 1, num4, "_create_decision() assertEqual2 failed")

        self.assertEqual(edge4.source, "decision_id1", "_create_decision() assertEqual3 failed")
        self.assertEqual(edge3.source, "decision_id1", "_create_decision() assertEqual4 failed")
        self.assertEqual(edge.source, "action2", "_create_decision() assertEqual5 failed")
        self.assertEqual(edge.target, "decision_id1", "_create_decision() assertEqual6 failed")

        self.assertEqual(len(final.incomings), 1, "_create_decision() assertEqual7 failed")
        self.assertEqual(final.incomings[0].xmi_idref, "edge4", "_create_decision() assertEqual8 failed")
        self.assertEqual(len(decision.outgoings), 2, "_create_decision() assertEqual9 failed")
        self.assertEqual(decision.incomings[0].xmi_idref, "edge_id1", "_create_decision() assertEqual10 failed")
        self.assertEqual(len(decision.incomings), 1, "_create_decision() assertEqual11 failed")
        self.assertEqual(len(action2.outgoings), 1, "_create_decision() assertEqual12 failed")
        self.assertEqual(action2.outgoings[0].xmi_idref, "edge_id1", "_create_decision() assertEqual12 failed")

        self.assertTrue("decision_id1" in nodes_dict, "_create_decision() assertTrue failed")
        self.assertTrue("edge_id1" in edges_dict, "_create_decision() assertTrue failed")

if __name__ == '__main__':
    unittest.main()
