from pathlib import Path

# img_path = Path(__file__).parent.parent / 'resources' / 'imgs' / 'P25-experiments-labelled.jpeg'
img_path = Path(__file__).parent.parent / 'resources' / 'imgs' / 'p25_layout.png'

config = {
    'img': str(img_path),
    # 'size': (int(1280/1.2),int(720/1.2)),#(width, height)
    'size': (int(1531/1.),int(473/1.)),#(width, height)
}