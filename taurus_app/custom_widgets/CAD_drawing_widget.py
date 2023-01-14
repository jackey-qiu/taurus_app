from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QImage, QPainterPath, QColor, QBrush, QFont, QPen
from PyQt5.QtCore import Qt, QTimer
import sys
from pathlib import Path
import imageio, cv2
from taurus_app.config.cad_config import config

class cadWidget(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.img = None
        self.img_ratio_original = None
        self.run_init(config)

    def run_init(self, config):
        self.img = config['img']
        self.img_resize = config['size']

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self._draw_image(qp)
        qp.end()

    def _draw_image(self, pq):
        image = imageio.imread(self.img)
        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        if self.img_ratio_original==None:
            self.img_ratio_original = image.shape[1]/image.shape[0]
        image = cv2.resize(image, dsize=self.img_resize, interpolation=cv2.INTER_CUBIC)
        im = QImage(image,image.shape[1],image.shape[0], image.shape[1] * 3, QImage.Format_BGR888)
        pq.drawImage(0, 0, im)

    def _set_img_dim_upon_resize(self):
        #we would like to keep the img_ratio
        view_box_ratio = self.width()/self.height()
        if view_box_ratio >= self.img_ratio_original:
            self.img_resize = (int(self.img_ratio_original*self.height()),int(self.height()))
        else:
            self.img_resize = (int(self.width()),int(self.width()/self.img_ratio_original))

    def resizeEvent(self, e):
        if self.img_ratio_original==None:
            return
        self._set_img_dim_upon_resize()
        self.update()

    def _draw_rect(self, pq, dim, id):
        self.pq.drawRect(*dim)

    def mouseMoveEvent(self, event):
        pass

    def mousePressEvent(self, event):
        pass
