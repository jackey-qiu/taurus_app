
__all__ = ['synoptic', 'prepare_config']

synoptic = {
            'frame':['OH','CC', 'PD', 'XFI','IM'],
            'svg_file':['taurus_app/resources/svgs/synoptic_view_1.svg',
                        'taurus_app/resources/svgs/synoptic_view_2_funny.svg',
                        'taurus_app/resources/svgs/synoptic_view_3_funny.svg',
                        'taurus_app/resources/svgs/synoptic_view_4_funny.svg',
                        'taurus_app/resources/svgs/synoptic_view_5_funny.svg'],
            'model': [{
                      'ior1':'ioregister/sis3610in_eh/1/SimulationMode',
                      'ior2':'ioregister/sis3610in_eh/2/SimulationMode',
                      'ior3':'ioregister/sis3610in_eh/3/SimulationMode',
                      'offset':'motor/omsvme58_motor_eh/1/Position',
                      'gx':'motor/omsvme58_motor_eh/1/Position',
                      'gy':'motor/omsvme58_motor_eh/1/Position',
                      'mot1':'motor/omsvme58_motor_eh/1/Position',
                     }]*5,
            'hover_style':['stroke:#FF0000']*5,
            }

def prepare_config(frame_name):
    which = synoptic['frame'].index(frame_name)
    return {'svg_file': synoptic['svg_file'][which],
              'model': synoptic['model'][which],
              'hover_style': synoptic['hover_style'][which]}

def extract_all_model_keys():
    temp_ = [list(each.keys()) for each in synoptic['model']]
    all_keys = []
    for each in temp_:
        all_keys = all_keys + each
    return list(set(all_keys))