'''
Created on 17.11.2015

@author: Kai
'''
import unittest
from ad_to_petri import get_reachability_graph
from bean import petri_net_element


class Mytest(unittest.TestCase):
    '''test
    '''
    # initial
    def setUp(self):
        '''setup
        '''
        # new the to unit test class object
        self.tclass = get_reachability_graph.PetriToReachabilityGraph()
        # place1->arc1->transition1->arc2->place2
        place1 = petri_net_element.Place("place1", "place1", [], ["arc1"])
        arc1 = petri_net_element.Arc("arc1", "arc1", "place1", "transition1")
        transition1 = petri_net_element.Transition("transition1", "transition1", ["arc1"], ["arc2"])
        arc2 = petri_net_element.Arc("arc2", "arc2", "transition1", "place2")
        place2 = petri_net_element.Place("place2", "place2", ["arc2"], [])

        places_dict = {}
        transitions_dict = {}
        arcs_dict = {}

        places_dict["place1"] = place1
        places_dict["place2"] = place2
        transitions_dict["transition1"] = transition1
        arcs_dict["arc1"] = arc1
        arcs_dict["arc2"] = arc2

        petri_net = petri_net_element.PetriNet(places_dict,\
                                    transitions_dict, arcs_dict, "petri_net")
        self.petri_net = petri_net


    def tearDown(self):
        '''tear down
        '''
        self.tclass = None
        self.petri_net = None

    def test_get_new_id(self):
        '''_get_new_id()
        '''

        petri_net = self.petri_net

        places_dict = petri_net.places_dict
        transitions_dict = petri_net.transitions_dict

        place1 = places_dict["place1"]
        place2 = places_dict["place2"]

        transition1 = transitions_dict["transition1"]

        new_id = self.tclass._get_new_id(place1, places_dict)
        self.assertEqual(new_id, "p1", "test_get_new_id() assertEqual1 failed")

        new_id = self.tclass._get_new_id(transition1, transitions_dict)
        self.assertEqual(new_id, "t1", "test_get_new_id() assertEqual2 failed")

        place1.id_changed = True
        new_id = self.tclass._get_new_id(place2, places_dict)
        self.assertEqual(new_id, "p2", "test_get_new_id() assertEqual3 failed")

if __name__ == '__main__':
    unittest.main()
