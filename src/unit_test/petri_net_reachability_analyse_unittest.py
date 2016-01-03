'''
Created on 16.11.2015

@author: Kai
'''
import unittest
from ad_to_petri import petri_net_reachability_analyse
from bean import petri_net_element


class Mytest(unittest.TestCase):
    '''test
    '''
    # initial
    def setUp(self):
        '''set up
        '''
        # new the to unit test class object
        self.tclass = petri_net_reachability_analyse.PetriNetReachabilityAnalyser()

        # p1->arc1->t1->arc2->p2
        p1 = petri_net_element.Place("p1", "p1", [], ["arc1"])
        arc1 = petri_net_element.Arc("arc1", "arc1", "p1", "t1")
        t1 = petri_net_element.Transition("t1", "t1", ["arc1"], ["arc2"])
        arc2 = petri_net_element.Arc("arc2", "arc2", "t1", "p2")
        p2 = petri_net_element.Place("p2", "p2", ["arc2"], [])

        places_dict = {}
        transitions_dict = {}
        arcs_dict = {}

        places_dict["p1"] = p1
        places_dict["p2"] = p2
        transitions_dict["t1"] = t1
        arcs_dict["arc1"] = arc1
        arcs_dict["arc2"] = arc2

        petri_net = petri_net_element.PetriNet(places_dict, transitions_dict, arcs_dict, "petri_net")
        self.petri_net = petri_net

    # tear down
    def tearDown(self):
        '''tear down
        '''
        self.tclass = None
        self.petri_net = None

    def test_find_deadlock(self):
        '''find_deadlock()
        '''
        petri_net = self.petri_net
        p1 = petri_net.places_dict["p1"]
        t1 = petri_net.transitions_dict["t1"]
        p2 = petri_net.places_dict["p2"]

        p1.id_changed = True
        t1.id_changed = False
        p2.id_changed = False

        ids = self.tclass.find_deadlock(petri_net)

        self.assertTrue(p1.pt_id not in ids, "test_find_deadlock() assertTrue1 failed")
        self.assertTrue(t1.pt_id in ids, "test_find_deadlock() assertTrue2 failed")
        self.assertTrue(p2.pt_id in ids, "test_find_deadlock() assertTrue2 failed")

        self.assertEqual(len(ids), 2, "test_find_deadlock() assertEqual1 failed")

    def test_get_petri_type(self):
        '''get_petri_type
        '''
        petri_net = self.petri_net

        places_dict = petri_net.places_dict
        transitions_dict = petri_net.transitions_dict
        arcs_dict = petri_net.arcs_dict

        # p1->arc1->transition1->arc2->place2
        petri_type = self.tclass.get_petri_type(petri_net)

        self.assertTrue(petri_net_element.PetriNetTypes.MARKED_GRAPHS in petri_type, "test_get_petri_type() assertTrue1 failed")
        self.assertTrue(petri_net_element.PetriNetTypes.STATE_MACHINES in petri_type, "test_get_petri_type() assertTrue2 failed")
        self.assertTrue(len(petri_type) == 2, "test_get_petri_type() assertTrue3 failed")

        # p1->arc3->t2->arc4->p3
        p1 = petri_net.places_dict["p1"]
        p1.outgoings.append("arc3")

        arc3 = petri_net_element.Arc("arc3", "arc3", "p1", "t2")
        t2 = petri_net_element.Transition("t2", "t2", ["arc3"], ["arc4"])
        arc4 = petri_net_element.Arc("arc4", "arc4", "t2", "p3")
        p3 = petri_net_element.Place("p3", "p3", ["arc4"], [])

        places_dict["p3"] = p3
        transitions_dict["t2"] = t2
        arcs_dict["arc3"] = arc3
        arcs_dict["arc4"] = arc4

        petri_type = self.tclass.get_petri_type(petri_net)

        self.assertTrue(petri_net_element.PetriNetTypes.STATE_MACHINES in petri_type, "test_get_petri_type() assertTrue4 failed")
        self.assertTrue(len(petri_type) == 1, "test_get_petri_type() assertTrue5 failed")

        # t2->arc5->p4
        t2.outgoings.append("arc5")
        arc5 = petri_net_element.Arc("arc5", "arc5", "t2", "p4")
        p4 = petri_net_element.Place("p4", "p4", ["arc5"], [])

        places_dict["p4"] = p4
        arcs_dict["arc5"] = arc5

        petri_type = self.tclass.get_petri_type(petri_net)

        self.assertTrue(petri_net_element.PetriNetTypes.FREE_CHOICE in petri_type, "test_get_petri_type() assertTrue6 failed")
        self.assertTrue(len(petri_type) == 1, "test_get_petri_type() assertTrue7 failed")

        # p5->arc6->t2
        t2.incomings.append("arc6")
        arc6 = petri_net_element.Arc("arc6", "arc6", "p5", "t2")
        p5 = petri_net_element.Place("p5", "p5", [], ["arc6"])

        places_dict["p5"] = p5
        arcs_dict["arc6"] = arc6

        petri_type = self.tclass.get_petri_type(petri_net)

        self.assertTrue(petri_net_element.PetriNetTypes.NOT_FREE_CHOICE in petri_type, "test_get_petri_type() assertTrue8 failed")
        self.assertTrue(len(petri_type) == 1, "test_get_petri_type() assertTrue9 failed")

    def test_get_matrix(self):
        '''get_matrix()
        '''
        petri_net = self.petri_net
        matrix = self.tclass.get_matrix(petri_net)

        self.assertTrue(matrix[0, 0] == -1, "test_get_matrix() assertTrue1 failed")
        self.assertTrue(matrix[1, 0] == 1, "test_get_matrix() assertTrue1 failed")

if __name__ == '__main__':
    unittest.main()
