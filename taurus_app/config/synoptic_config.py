from pathlib import Path
from .tango_model_manager import get_model

__all__ = ['synoptic', 'prepare_config']

#svg_root = 'taurus_app/resources/svgs/'
svg_root = Path(__file__).parent.parent / "resources" / "svgs"
synoptic = {
            'frame':['OH','CC', 'PD', 'XFI','IM'],
            'svg_file':list(map(lambda each: str(svg_root / each),['synoptic_view_1.svg',
                        'synoptic_view_2_funny.svg',
                        'synoptic_view_3_funny.svg',
                        'synoptic_view_4_funny.svg',
                        'synoptic_view_5_funny.svg'])),
            'model': [{
                      'ior1':get_model('ior1','SimulationMode'),
                      'ior2':get_model('ior2','SimulationMode'),
                      'ior3':get_model('ior3','SimulationMode'),
                      'offset':get_model('omot1','Position'),
                      'gx':get_model('omot2','Position'),
                      'gy':get_model('omot3','Position'),
                      'mot1':get_model('dmot1','Position'),
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