from epf import epf_model


model = epf_model.Model()

# xml_path = "C:/Users/Kai/Desktop/ErrorPro3.4/epf/examples/abc.xml"
# model.xml.load(xml_path)
    
'''
model.add_element("A")
model.set_initial_element("A")
model.add_element("parallel")
# set the element parallel
model.add_element("B", "parallel")
model.set_subsystem_parallel("parallel")
model.set_initial_element("B")
model.add_element("C", "parallel")
model.set_initial_element("C")
model.add_element("D", "parallel")
model.add_element("E")
model.add_element("F", "parallel")



model.add_cf_arc("A", "parallel", 1)
model.add_cf_arc("parallel", "parallel", 0.5)
model.add_cf_arc("parallel", "E", 0.5)

model.add_cf_arc("C", "D", 1)
model.add_cf_arc("B", "F", 1)

model.add_data("data1", "parallel")
model.add_data("data2", "parallel")

model.add_df_arc("B", "data1")
model.add_df_arc("data1","D")
model.add_df_arc("D","data2")

'''
model.xml.load("test.xml")
print model.elements  # key = element name
print model.data  # key = data name
print model.cf_probs  # key =  "(from,to)", value = prob
print model.subsystems  # key = host, value = {intial_element, elements, data}

model.drawing.draw_system()

#model.xml.save("test.xml")