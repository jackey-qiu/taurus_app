
__all__ = ['synoptic', 'prepare_config']

synoptic = {
            'widget_name':['widget_synopic'],
            'svg_file':['taurus_app/resources/svgs/synoptic_view_1.svg'],
            'model': [{
                      'ior1':'ioregister/iorctrl01/1/SimulationMode',
                      'ior2':'ioregister/iorctrl01/2/SimulationMode',
                      'ior3':'sys/tg_test/1/boolean_scalar',
                      'offset':'pm/slitctrl01/2/Position',
                      'gx':'motor/motctrl01/3/Position',
                      'gy':'motor/motctrl01/4/Position',
                      'mot1':'motor/motctrl01/1/Position',
                     }],
            'hover_style':['stroke:#FF0000'],
            }

def prepare_config(widget_name):
    which = synoptic['widget_name'].index(widget_name)
    return {'svg_file': synoptic['svg_file'][which],
              'model': synoptic['model'][which],
              'hover_style': synoptic['hover_style'][which]}