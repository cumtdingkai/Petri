'''
Created on 21.12.2015

@author: Kai
'''
from epf import epf_model


model = epf_model.Model()

#xml_path = "C:/Users/Kai/Desktop/ErrorPro3.4/epf/examples/abc.xml"
xml_path = "C:/Users/Kai/Desktop/test_parallel_epf.xml"
model.xml.load(xml_path)

model.cf_parallel.get_parallel_process()
#print model.elements  # key = element name
#print model.data  # key = data name
#print model.cf_probs  # key =  "(from,to)", value = prob
#print model.subsystems  # key = host, value = {intial_element, elements, data}
