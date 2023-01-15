from pathlib import Path
from PyQt5.QtCore import Qt

# img_path = Path(__file__).parent.parent / 'resources' / 'imgs' / 'P25-experiments-labelled.jpeg'
img_path = Path(__file__).parent.parent / 'resources' / 'imgs' / 'p25_layout.png'

config = {
    'img': str(img_path),
    # 'size': (int(1280/1.2),int(720/1.2)),#(width, height)
    'size': (int(1531/1.),int(473/1.)),#(width, height)
    'rect_frames':{#[dim(x,y,width,height), pen_color, pen_style, brush_color]
                   'OH':[(6,184,479,290),(0,255,0), Qt.SolidLine, (0,255,255,50)],
                   'CC':[(493,185,322,290),(0,255,0), Qt.SolidLine, (0,255,255,50)],
                   'PD':[(820,187,192,286),(0,255,0), Qt.SolidLine, (0,255,255,50)],
                   'XFI':[(1013,183,98,293),(0,255,0), Qt.SolidLine, (0,255,255,50)],
                   'IM':[(1117,183,324,286),(0,255,0), Qt.SolidLine, (0,255,255,50)],
                  },
    'hover_style':[(255, 0, 0), Qt.DotLine, (100,0,255,50)],
    'non_hover_style':[(0, 255, 0), Qt.SolidLine, (0,255,255,50)],
}