model_graph = '''
dmot1:motor/dummy_mot_ctrl/1
dmot2:motor/dummy_mot_ctrl/2
ior1:ioregister/sis3610in_eh/1
ior2:ioregister/sis3610in_eh/2
ior3:ioregister/sis3610in_eh/3
ior4:ioregister/sis3610in_eh/4
omot1:motor/omsvme58_motor_eh/1
omot2:motor/omsvme58_motor_eh/2
omot3:motor/omsvme58_motor_eh/3
'''

def _model():
    result = {}
    for each in model_graph.strip().rsplit('\n'):
        key, model = each.replace(' ','').rsplit(':')
        result[key] = model
    return result

model_dict = _model()

#key is the key for the archived model
#extended_tag is the attribute name to be appended at the end
def get_model(key, extended_tag=''):
    if model_dict[key]:
        if extended_tag:
            return model_dict[key]+'/'+extended_tag
        else:
            return model_dict[key]



