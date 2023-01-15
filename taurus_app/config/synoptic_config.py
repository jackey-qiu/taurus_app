
__all__ = ['synoptic', 'prepare_config']

synoptic = {
            'frame':['OH','CC', 'PD', 'XFI','IM'],
            'svg_file':['taurus_app/resources/svgs/synoptic_view_1.svg',
                        'taurus_app/resources/svgs/synoptic_view_2_funny.svg',
                        'taurus_app/resources/svgs/synoptic_view_3_funny.svg',
                        'taurus_app/resources/svgs/synoptic_view_4_funny.svg',
                        'taurus_app/resources/svgs/synoptic_view_5_funny.svg'],
            'model': [{
                      'ior1':'ioregister/iorctrl01/1/SimulationMode',
                      'ior2':'ioregister/iorctrl01/2/SimulationMode',
                      'ior3':'sys/tg_test/1/boolean_scalar',
                      'offset':'pm/slitctrl01/2/Position',
                      'gx':'motor/motctrl01/3/Position',
                      'gy':'motor/motctrl01/4/Position',
                      'mot1':'motor/motctrl01/1/Position',
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
    return all_keys