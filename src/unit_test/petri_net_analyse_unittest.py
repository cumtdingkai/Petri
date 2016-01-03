'''
Created on 16.11.2015

@author: Kai
'''
import unittest
from ad_to_petri import petri_net_analyse
from bean import petri_net_element


class Mytest(unittest.TestCase):
    '''test
    '''
    # initial
    def setUp(self):
        '''set up
        '''
        # new the to unit test class object
        self.tclass = petri_net_analyse.PetriNetAnalyser()

        # place->arc1->transition->arc2->place
        place = petri_net_element.Place("place", "place", ["arc2"], ["arc1"])
        arc1 = petri_net_element.Arc("arc1", "arc1", "place", "transition")
        transition = petri_net_element.Transition("transition", "transition", ["arc1"], ["arc2"])
        arc2 = petri_net_element.Arc("arc2", "arc2", "transition", "place")

        places_dict = {}
        transitions_dict = {}
        arcs_dict = {}

        places_dict["place"] = place
        transitions_dict["transition"] = transition
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

    def test_find_self_loop(self):
        '''find_self_loop()
        '''
        petri_net = self.petri_net
        num = self.tclass.find_self_loop(petri_net)
        self.assertEqual(num, 1, "test_find_self_loop() failed")

    def test_eliminate_self_loop(self):
        '''eliminate_self_loop()
        '''
        petri_net = self.petri_net

        places_dict = petri_net.places_dict
        transitions_dict = petri_net.transitions_dict
        arcs_dict = petri_net.arcs_dict

        num1 = len(places_dict)
        num2 = len(transitions_dict)
        num3 = len(arcs_dict)

        place = places_dict["place"]
        arc = arcs_dict["arc2"]

        self.tclass.eliminate_self_loop(place, arc, petri_net)
        # place->arc1->transition->arc2->place
        # place->arc1->transition->arc2(arc)->place_id1->arc_id1->transition_id1->arc_id2->place
        num4 = len(places_dict)
        num5 = len(transitions_dict)
        num6 = len(arcs_dict)

        self.assertEqual(num1 + 1, num4, "test_eliminate_self_loop() assertEqual1 failed")
        self.assertEqual(num2 + 1, num5, "test_eliminate_self_loop() assertEqual2 failed")
        self.assertEqual(num3 + 2, num6, "test_eliminate_self_loop() assertEqual3 failed")

        self.assertTrue("place_id1" in places_dict, "test_eliminate_self_loop() assertTrue1 failed")
        self.assertTrue("transition_id1" in transitions_dict, "test_eliminate_self_loop() assertTrue2 failed")
        self.assertTrue("arc_id1" in arcs_dict, "test_eliminate_self_loop() assertTrue3 failed")
        self.assertTrue("arc_id2" in arcs_dict, "test_eliminate_self_loop() assertTrue4 failed")

        place_id1 = places_dict["place_id1"]
        transition_id1 = transitions_dict["transition_id1"]
        arc_id1 = arcs_dict["arc_id1"]
        arc_id2 = arcs_dict["arc_id2"]

        self.assertEqual(arc.target, "place_id1", "test_eliminate_self_loop() assertEqual4 failed")
        self.assertEqual(place_id1.incomings, ["arc2"], "test_eliminate_self_loop() assertEqual5 failed")
        self.assertEqual(place_id1.outgoings, ["arc_id1"], "test_eliminate_self_loop() assertEqual6 failed")
        self.assertEqual(arc_id1.source, "place_id1", "test_eliminate_self_loop() assertEqual7 failed")
        self.assertEqual(arc_id1.target, "transition_id1", "test_eliminate_self_loop() assertEqual8 failed")
        self.assertEqual(transition_id1.incomings, ["arc_id1"], "test_eliminate_self_loop() assertEqual9 failed")
        self.assertEqual(transition_id1.outgoings, ["arc_id2"], "test_eliminate_self_loop() assertEqual10 failed")
        self.assertEqual(arc_id2.source, "transition_id1", "test_eliminate_self_loop() assertEqual11 failed")
        self.assertEqual(arc_id2.target, "place", "test_eliminate_self_loop() assertEqual12 failed")
        self.assertEqual(place.incomings, ["arc_id2"], "test_eliminate_self_loop() assertEqual13 failed")

    def test_get_new_id(self):
        '''_get_new_id()
        '''
        petri_net = self.petri_net
        places_dict = petri_net.places_dict
        transitions_dict = petri_net.transitions_dict
        arcs_dict = petri_net.arcs_dict

        new_id = self.tclass._get_new_id("place", places_dict)
        self.assertEqual(new_id, "place_id1", "test_get_new_id() assertEqual1 failed")

        new_id = self.tclass._get_new_id("transition", transitions_dict)
        self.assertEqual(new_id, "transition_id1", "test_get_new_id() assertEqual2 failed")

        new_id = self.tclass._get_new_id("arc", arcs_dict)
        self.assertEqual(new_id, "arc_id1", "test_get_new_id() assertEqual3 failed")

        test_dict = {"place_id1":1, "place_id2":2, "place_id3":3}
        new_id = self.tclass._get_new_id("place", test_dict)
        self.assertEqual(new_id, "place_id4", "test_get_new_id() assertEqual4 failed")

if __name__ == '__main__':
    unittest.main()
