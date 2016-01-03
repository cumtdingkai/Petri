'''
Created on 02.12.2015

@author: Kai
'''
from bean import uml_activity_diagram_element as uml_element
import log

def object_node_has_more_incomings(self, activity):
        ''' if a object node has more than one incoming.
        if yes, create one merge before the object node.
        yes: return True
        no:  return False
        @see: example/document
        '''
        nodes_dict = activity.nodes_dict
        ret = False
        ids = []
        for node_id in nodes_dict:
            node = nodes_dict[node_id]
            if isinstance(node, uml_element.ObjectNode):
                incomings = node.incomings
                num = len(incomings)
                if  num > 1:
                    ids.append(node_id)
                    log.show_warn("the object node " + "name:" + str(node.name) + \
                                  " id:" + node.xmi_id + " has " + str(num) + " incomings")
                    ret = True
        if ret:
            for node_id in ids:
                self._create_merge(node_id, activity, uml_element.Types.OBJECT_FLOW)

        return ret